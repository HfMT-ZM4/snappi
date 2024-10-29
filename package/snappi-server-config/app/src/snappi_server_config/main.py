from pathlib import Path
from argparse import ArgumentParser

from .settings import settings


def main():
    parser = ArgumentParser()
    parser.add_argument('cmd', choices=('update', 'serve'))
    parser.add_argument('-r', '--root-path', type=Path)
    parser.add_argument('-b', '--bin-path', type=Path)
    parser.add_argument('-s', '--static-path', type=Path)
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument('-H', '--host')
    args = parser.parse_args()

    for name in ('root_path', 'bin_path', 'static_path',
                 'port', 'host'):
        val = getattr(args, name)
        if val is None:
            continue
        setattr(settings, name, val)

    if args.cmd == 'serve':
        from .server import serve
        serve()
    else:
        from .config import ServerConfig
        config = ServerConfig()
        config.apply_cloud_init_data()
        config.activate()

