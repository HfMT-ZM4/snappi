from collections import defaultdict
import json
import subprocess
import asyncio
from dataclasses import dataclass


def prop(obj, name, default=None):
    return obj.get('info', {}).get('props', {}).get(name, default)


def info(obj, name, default=None):
    return obj.get('info', {}).get(name, default)


def params(obj, name, default=None):
    return obj.get('info', {}).get('params', {}).get(name, default)


@dataclass
class Port:
    id: int
    port_id: tuple[str, str]
    port_path: str
    name: str
    direction: str
    node_name: str
    node_description: str
    node_nick: str
    physical: bool
    terminal: bool
    monitor: bool
    link_ids: list

    def __str__(self):
        return f'{self.node_description}:{self.name} ({self.direction})'


def get_pw_dump_output(retries=5):
    while True:
        try:
            result = subprocess.check_output('/usr/bin/pw-dump')
            return json.loads(result)
        except Exception:
            retries -= 1
            if retries <= 0:
                return



def get_pw_ports():
    raw = get_pw_dump_output()
    if raw is None:
        return {}

    objs = {obj['id']: obj for obj in raw}

    ports = {}

    for raw_port in objs.values():
        if raw_port['type'] != 'PipeWire:Interface:Port':
            continue

        raw_node = objs.get(prop(raw_port, 'node.id'))
        if not raw_node:
            continue

        formats = params(raw_port, 'EnumFormat', [])
        if not formats or formats[0].get('mediaType') != 'audio':
            continue

        port_name = prop(raw_port, 'port.name', '')
        node_description = prop(raw_node, 'node.description', '')
        port_id = (node_description, port_name)
        port_path = ':::'.join(port_id)

        port = Port(
            id=raw_port['id'],
            port_id=port_id,
            port_path=port_path,
            name=port_name,
            direction=prop(raw_port, 'port.direction'),
            node_name=prop(raw_node, 'node.name', ''),
            node_description=node_description,
            node_nick=prop(raw_node, 'node.nick', ''),
            physical=prop(raw_port, 'port.physical', False),
            terminal=prop(raw_port, 'port.terminal', False),
            monitor=prop(raw_port, 'port.monitor', False),
            link_ids=[]
        )

        ports[port.id] = port

    for raw_link in objs.values():
        if raw_link['type'] != 'PipeWire:Interface:Link':
            continue
        input_port_id = info(raw_link, 'input-port-id')
        if input_port_id not in ports:
            continue

        output_port = ports.get(info(raw_link, 'output-port-id'))
        if not output_port:
            continue

        output_port.link_ids.append(input_port_id)

    return ports


async def pw_monitor(pw_types, queue):
    """Monitor PipeWire for changes"""
    changed_types = set()
    first_run = False

    interesting_types = [
        f'PipeWire:Interface:{pw_type}' for pw_type in pw_types
    ]

    object_types = {}
    event = None
    obj_id = None
    obj_type = None

    proc = await asyncio.create_subprocess_shell('/usr/bin/pw-mon -p -a -o', stdout=asyncio.subprocess.PIPE)
    if proc.stdout is None:
        return

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
                await queue.put(f'PipeWire:{",".join(changed_types)}')
            changed_types = set()
            first_run = False


def _find_port_id_by_path(ports, port_path):
    for port in ports.values():
        if port.port_path == port_path:
            return port.id


def setup_pw_links(links: list[tuple[str, str]]):
    """
    `links` is a list of tuples (source port_path, destination port_path)
    """
    # turn "soft" link descriptions into actual port ids
    ports = get_pw_ports()
    port_links = defaultdict(list)
    for src_path, dst_path in links:
        src_port_id = _find_port_id_by_path(ports, src_path)
        dst_port_id = _find_port_id_by_path(ports, dst_path)
        if not src_port_id or not dst_port_id:
            continue
        port_links[src_port_id].append(dst_port_id)

    # go through all ports and note which ports to connect and which to disconnect
    to_connect = []
    to_disconnect = []
    for port in ports.values():
        current_links = set(port.link_ids)
        wanted_links = set(port_links[port.id])
        for dst_id in current_links - wanted_links:
            to_disconnect.append([port.id, dst_id])
        for dst_id in wanted_links - current_links:
            to_connect.append([port.id, dst_id])

    for src_id, dst_id in to_disconnect:
        subprocess.check_call(['/usr/bin/pw-link', '-d', str(src_id), str(dst_id)])

    for src_id, dst_id in to_connect:
        subprocess.check_call(['/usr/bin/pw-link', str(src_id), str(dst_id)])


if __name__ == '__main__':
    from dataclasses import asdict
    print(json.dumps([asdict(p) for p in get_pw_ports().values()], indent=2))
