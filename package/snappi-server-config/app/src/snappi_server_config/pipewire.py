from collections import defaultdict
from dataclasses import dataclass

import asyncio
import json
import subprocess

from .settings import settings


@dataclass
class Port:
    id: int
    port_path: str
    name: str
    direction: str
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

    def get_port_id_by_path(self, path):
        port = self.ports_by_path.get(path)
        return port.id if port else None

    async def refresh_ports(self):
        print('refresh ports')
        self.ports_by_id = await self._get_ports()
        self.ports_by_path = {
            port.port_path : port
            for port in self.ports_by_id.values()
        }

    async def setup_links(self, links : list[tuple[str, str]]):
        """
        `links` is a list of tuples (source port_path, destination port_path)
        """
        print('setup links', links)
        # turn "soft" link descriptions into actual port ids
        port_links = defaultdict(list)
        for src_path, dst_path in links:
            src_port_id = self.get_port_id_by_path(src_path)
            dst_port_id = self.get_port_id_by_path(dst_path)
            if not src_port_id or not dst_port_id:
                continue
            port_links[src_port_id].append(dst_port_id)

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

        for src_id, dst_id in to_disconnect:
            try:
                subprocess.check_call([settings.bin_path / 'pw-link', '-d', str(src_id), str(dst_id)])
                port = self.ports_by_id.get(src_id)
                if port:
                    port.link_ids.remove(dst_id)
            except subprocess.CalledProcessError:
                print(f'Failed to disconnect {src_id} {dst_id}')

        for src_id, dst_id in to_connect:
            try:
                subprocess.check_call([settings.bin_path / 'pw-link', str(src_id), str(dst_id)])
                port = self.ports_by_id.get(src_id)
                if port:
                    port.link_ids.add(dst_id)
            except subprocess.CalledProcessError:
                print(f'Failed to connect {src_id} {dst_id}')


    async def _get_ports(self):
        proc = await asyncio.create_subprocess_exec(
                settings.bin_path / 'pw-dump',
                stdout=asyncio.subprocess.PIPE)
        stdin, _ = await proc.communicate()
        raw = json_loads_all_arrays(stdin.decode('utf-8'))
        if not raw:
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

            node = objs.get(port_props.get('node.id'))
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

    async def monitor(self, callback=None):
        """Monitor PipeWire for changes"""
        changed_types = set()
        first_run = True

        interesting_types = [
            'PipeWire:Interface:Port',
        ]

        object_types = {}
        event = None
        obj_id = None
        obj_type = None

        pw_mon_cmd = settings.bin_path / 'pw-mon'
        proc = await asyncio.create_subprocess_shell(
            f'{pw_mon_cmd} --no-colors --print-separator --hide-params --hide-props',
            stdout=asyncio.subprocess.PIPE,
        )
        if proc.stdout is None:
            raise RuntimeError('Unable to run pw-mon')

        while proc.returncode is None:
            try:
                line = await asyncio.wait_for(proc.stdout.readline(), timeout=1.0)
                line = line.decode('utf-8').strip()

                if line == '':
                    if event == 'added:' and obj_type and obj_id:
                        object_types[obj_id] = obj_type
                    elif event == 'removed:' and obj_id:
                        obj_type = object_types.pop(obj_id, None)
                    elif event == 'changed:':
                        obj_type = None  # prevent handling of change events

                    if obj_type in interesting_types:
                        changed_types.add(obj_type)

                    event = None
                    obj_id = None
                    obj_type = None
                elif event is None:
                    event = line
                elif obj_id is None and line.startswith('id: '):
                    obj_id = line.split(' ')[1]
                elif obj_type is None and line.startswith('type: '):
                    obj_type = line.split(' ')[1]

            except asyncio.TimeoutError:
                if changed_types and not first_run:
                    await self.refresh_ports()
                    if callback:
                        try:
                            await callback()
                        except Exception as e:
                            print('Error in callback!', e)
                changed_types = set()
                first_run = False


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

