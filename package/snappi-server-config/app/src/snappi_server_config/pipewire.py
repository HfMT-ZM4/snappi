from collections import defaultdict
from dataclasses import dataclass

import asyncio
import logging
import json
import subprocess

from .settings import settings
from .utils import check_call


@dataclass
class Port:
    id: int
    port_path: str
    name: str
    direction: str
    node_id: int
    node_name: str
    node_description: str
    physical: bool
    terminal: bool
    monitor: bool
    link_ids: set

    def __str__(self):
        return f'{self.port_path} ({self.direction})'


class Pipewire:
    def __init__(self):
        self.ports_by_id : dict[int, Port] = {}
        self.ports_by_path : dict[str, Port] = {}

    def get_terminal_output_ports(self):
        return [
            port for port in self.ports_by_id.values()
            if port.terminal and port.direction == 'out'
        ]

    def get_port_by_path(self, path):
        return self.ports_by_path.get(path)

    async def refresh_ports(self):
        self.ports_by_id = await self._get_ports()
        self.ports_by_path = {
            port.port_path : port
            for port in self.ports_by_id.values()
        }

    async def setup_links(self, links : list[tuple[str, str]]):
        """
        `links` is a list of tuples (source port_path, destination port_path)
        """
        # turn "soft" link descriptions into actual port ids
        port_links = defaultdict(list)
        for src_path, dst_path in links:
            src_port = self.get_port_by_path(src_path)
            dst_port = self.get_port_by_path(dst_path)
            if not src_port or not dst_port:
                continue
            port_links[src_port.id].append(dst_port.id)

        # go through all ports and note which ports to connect and which to disconnect
        to_connect = []
        to_disconnect = []
        for port in self.ports_by_id.values():
            current_links = port.link_ids
            wanted_links = set(port_links[port.id])
            for dst_id in current_links - wanted_links:
                to_disconnect.append([port.id, dst_id])
            for dst_id in wanted_links - current_links:
                to_connect.append([port.id, dst_id])

        pw_link_cmd = settings.bin_path / 'pw-link'
        pw_cli_cmd = settings.bin_path / 'pw-cli'

        for src_id, dst_id in to_disconnect:
            try:
                await check_call(f'{pw_link_cmd} -d {src_id} {dst_id}')
                port = self.ports_by_id.get(src_id)
                if port:
                    port.link_ids.remove(dst_id)
            except subprocess.CalledProcessError:
                logging.error(f'Failed to disconnect {src_id} {dst_id}')

        for src_id, dst_id in to_connect:
            src_port = self.ports_by_id[src_id]
            dst_port = self.ports_by_id[dst_id]
            try:
                await check_call(f'{pw_cli_cmd} cl {src_port.node_id} {src_port.id} {dst_port.node_id} {dst_port.id} object.linger=true')
                port = self.ports_by_id.get(src_id)
                if port:
                    port.link_ids.add(dst_id)
            except subprocess.CalledProcessError:
                logging.error(f'Failed to connect {src_id} {dst_id}')


    async def _get_ports(self):
        proc = await asyncio.create_subprocess_exec(
                settings.bin_path / 'pw-dump',
                stdout=asyncio.subprocess.PIPE)
        stdin, _ = await proc.communicate()
        raw = json_loads_all_arrays(stdin.decode('utf-8'))
        if not raw:
            logging.error('get_ports returned empty result!')
            return {}

        objs = {obj['id']: obj for obj in raw}

        pw_ports = {}

        for port_id, port in objs.items():
            if port.get('type', '') != 'PipeWire:Interface:Port':
                continue

            port_info = port.get('info', {})
            port_props = port_info.get('props', {})
            port_params = port_info.get('params', {})

            formats = port_params.get('EnumFormat', [])
            if not formats or formats[0].get('mediaType') != 'audio':
                continue

            node_id = port_props.get('node.id')
            node = objs.get(node_id)
            if not node:
                continue
            node_info = node.get('info', {})
            node_props = node_info.get('props', {})

            port_name = port_props.get('port.name', '')
            node_description = node_props.get('node.description', '')
            port_path = f'{node_description}:::{port_name}'

            pw_ports[port_id] = Port(
                id=port_id,
                port_path=port_path,
                name=port_name,
                node_id=node_id,
                node_name=node_props.get('node.name', ''),
                node_description=node_description,
                direction=port_props.get('port.direction', ''),
                physical=port_props.get('port.physical', False),
                terminal=port_props.get('port.terminal', False),
                monitor=port_props.get('port.monitor', False),
                link_ids=set(),
            )

        for link in objs.values():
            if link.get('type', '') != 'PipeWire:Interface:Link':
                continue

            link_info = link.get('info', {})

            input_port_id = link_info.get('input-port-id')
            if input_port_id not in pw_ports:
                continue

            output_port = pw_ports.get(link_info.get('output-port-id'))
            if not output_port:
                continue

            output_port.link_ids.add(input_port_id)

        return pw_ports

    async def _monitor(self, callback, timeout=2.0):
        """Monitor PipeWire for changed ports"""
        pw_link_cmd = settings.bin_path / 'pw-link'
        proc = await asyncio.create_subprocess_shell(
            f'{pw_link_cmd} --input --output --id --monitor',
            stdout=asyncio.subprocess.PIPE,
        )
        if proc.stdout is None:
            raise RuntimeError('Unable to run pw-link monitor')

        handle = None
        loop = asyncio.get_event_loop()

        # we assume that any output by the pw-link monitor is
        # an interesting change. But we wait for `timeout`
        # to pass before executing the callback
        async for line in proc.stdout:
            if handle:
                handle.cancel()

            handle = loop.call_later(timeout, lambda: asyncio.create_task(callback()))

        logging.error('Monitor stopped!!')

    async def monitor(self, callback, timeout=2.0):
        while True:
            try:
                await self._monitor(callback, timeout)
            except Exception:
                logging.error('Monitor stopped, retrying in 2 seconds...')
            await asyncio.sleep(2)


def json_loads_all_arrays(raw):
    """
    Parses a stream of concatenated JSON array structures
    and returns them as a single list of objects. Is is
    required because pw-dump sometimes outputs more than
    one array in a single stream.
    """
    pos = 0
    result = []
    decoder = json.JSONDecoder()
    while True:
        try:
            ary, pos = decoder.raw_decode(raw, pos)
            result.extend(ary)
            pos += 1
        except json.JSONDecodeError:
            break
    return result


if __name__ == '__main__':
    from dataclasses import asdict

    pw = Pipewire()

    async def dump_ports(changes):
        print(json.dumps([
            asdict(p) for p in pw.get_terminal_output_ports()
        ], indent=2))
        print(f'changes: {changes}')

    asyncio.run(pw.monitor(callback=dump_ports))

