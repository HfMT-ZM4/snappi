import subprocess
from pathlib import Path
from typing import List, Annotated

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.exception_handlers import http_exception_handler

from pydantic import BaseModel


ETC_DIR = Path('/etc')
BIN_DIR = Path('/usr/bin')

NM_CONFIG_DIR = ETC_DIR / 'NetworkManager/system-connections'
NM_CONNECTION_FILENAME = 'wifi.nmconnection'

SNAPPI_CONFIG_FILE = ETC_DIR / 'snappi.json'
JACKTRIP_CONFIG_FILE = ETC_DIR / 'default/jacktrip'
JACKD_CONFIG_FILE = ETC_DIR / 'default/jackd'
SNAPSERVER_CONFIG_FILE = ETC_DIR / 'snapserver.conf'
HOSTS_FILE = ETC_DIR / 'hosts'
HOSTNAME_FILE = ETC_DIR / 'hostname'

SYSTEMCTL_CMD = BIN_DIR / 'systemctl'
JOURNALCTL_CMD = BIN_DIR / 'journalctl'

FRONTEND_FILES_DIR = '/usr/share/snappi-server-config/frontend'

DEFAULT_CONFIG = {
    'hostname': 'snappi-server',
    'channels': 8,
    'samplerate': 48000,
    'bits': 16,
    'periodsize': 512,
    'latency': 600,
    'wifi': {
        'ssid': 'Snappi',
        'password': '12345678',
        'mode': 'ap',
        'band': 'auto',
    },
    'streams': [
        {'name': 'Mono-1', 'channels': [1]},
        {'name': 'Mono-2', 'channels': [2]},
        {'name': 'Mono-3', 'channels': [3]},
        {'name': 'Mono-4', 'channels': [4]},
        {'name': 'Mono-5', 'channels': [5]},
        {'name': 'Mono-6', 'channels': [6]},
        {'name': 'Mono-7', 'channels': [7]},
        {'name': 'Mono-8', 'channels': [8]},
        {'name': 'Stereo-1', 'channels': [1,2]},
        {'name': 'Stereo-2', 'channels': [3,4]},
        {'name': 'Stereo-3', 'channels': [5,6]},
        {'name': 'Stereo-4', 'channels': [7,8]},
    ],
}


class StreamConfig(BaseModel):
    name: str
    channels: List[int]


class WifiConfig(BaseModel):
    ssid: str
    password: str
    mode: str
    band: str


class Config(BaseModel):
    hostname: str
    channels: int
    samplerate: int
    bits: int
    periodsize: int
    latency: int
    wifi: WifiConfig
    streams: List[StreamConfig]


def load_config() -> Config:
    json_data = Path(SNAPPI_CONFIG_FILE).read_text()
    return Config.model_validate_json(json_data)


def store_config(config: Config):
    value = config.model_dump_json(indent=2)
    return write_file_if_changed(SNAPPI_CONFIG_FILE, value)


def _snapserver_source_url(**kwargs):
    params = []
    for key, val in kwargs.items():
        if isinstance(val, (list, tuple)):
            params.extend(f'{key}={el}' for el in val)
        else:
            params.append(f'{key}={val}')
    url = '&'.join(params)
    return f'source = jack:///?{url}'


def update_snapserver_config(config: Config):
    sources = []
    for stream in config.streams:
        sources.append(_snapserver_source_url(
            name=stream.name,
            sampleformat=f'{config.samplerate}:{config.bits}:{len(stream.channels)}',
            idle_threshold=5000,
            jack_time='true',
            autoconnect=[f'^JackTrip:receive_{num}$' for num in stream.channels],
        ))

    sources = '\n'.join(sources)

    value = striplines(f'''
        [server]
        user = snappi
        group = audio

        [http]
        doc_root = /usr/share/snapserver/snapweb

        [stream]
        codec = pcm
        buffer = {config.latency}

        {sources}
    ''')

    return write_file_if_changed(SNAPSERVER_CONFIG_FILE, value)


def update_hostname(config: Config):
    hosts_changed = False

    hosts_file = Path(HOSTS_FILE)
    hosts = hosts_file.read_text()
    entry = f'127.0.0.1 {config.hostname}'
    if entry not in hosts:
        hosts = hosts.strip() + f'\n{entry}\n'
        hosts_file.write_text(hosts)
        hosts_changed = True

    hostname_changed = write_file_if_changed(HOSTNAME_FILE, config.hostname)

    return hosts_changed or hostname_changed


def update_wifi_config(config: Config):
    if config.wifi.mode == 'ap':
        wifi_config = generate_wifi_ap_config(config)
    elif config.wifi.mode == 'client':
        wifi_config = generate_wifi_client_config(config)
    else:
        raise RuntimeError(f'Invalid wifi mode: {config.wifi.mode}')

    config_file = Path(NM_CONFIG_DIR) / NM_CONNECTION_FILENAME
    config_changed = write_file_if_changed(config_file, wifi_config, mode=0o600)

    file_deleted = False
    for conf in Path(NM_CONFIG_DIR).glob('*.nmconnection'):
        if conf.name == NM_CONNECTION_FILENAME:
            continue
        conf.unlink()
        file_deleted = True

    return config_changed or file_deleted


def generate_wifi_ap_config(config: Config):
    return striplines(f'''
        [connection]
        id=Hotspot
        uuid=177fde1d-bead-4f0d-a1f1-0bc3530b94f7
        type=wifi
        autoconnect=true
        interface-name=wlan0

        [wifi]
        band=bg
        hidden=false
        mode=ap
        ssid={config.wifi.ssid}

        [wifi-security]
        group=ccmp;
        key-mgmt=wpa-psk
        pairwise=ccmp;
        proto=wpa;rsn;
        psk={config.wifi.password}

        [ipv4]
        method=shared
        address1=10.10.10.1/24,10.10.10.1

        [ipv6]
        addr-gen-mode=default
        method=ignore
    ''')


def generate_wifi_client_config(config: Config):
    return striplines(f'''
        [connection]
        id=wifi
        uuid=4c47ec9c-481d-47be-8ad7-b85f29767335
        type=wifi
        interface-name=wlan0
        autoconnect=true

        [wifi]
        mode=infrastructure
        ssid={config.wifi.ssid}

        [wifi-security]
        auth-alg=open
        key-mgmt=wpa-psk
        psk={config.wifi.password}

        [ipv4]
        method=auto

        [ipv6]
        addr-gen-mode=default
        method=auto
    ''')


def update_jacktrip_config(config: Config):
    value = striplines(f'''
        JACKTRIP_OPTS="-s --receivechannels {config.channels} --sendchannels 1 --udprt"
    ''')
    return write_file_if_changed(JACKTRIP_CONFIG_FILE, value)


def update_jackd_config(config: Config):
    value = striplines(f'''
        JACKD_OPTS="-R -P75 -ddummy -p{config.periodsize} -r{config.samplerate}"
    ''')
    return write_file_if_changed(JACKD_CONFIG_FILE, value)


def write_file_if_changed(filename, value, mode=None):
    file = Path(filename)
    try:
        original = file.read_text()
    except FileNotFoundError:
        original = None
    if original == value:
        print(f'FILE {filename} unchanged')
        return False
    print(f'==== FILE {filename} changed, original/new:')
    print(file.read_text())
    print('-------------------------------')
    print(value)
    file.write_text(value)
    if mode is not None:
        file.chmod(mode)
    return True


def update_config(config: Config) -> List[str]:
    restart_services = set()

    for method, services in (
        (update_hostname, 'system'),
        (update_wifi_config, 'system'),
        (update_jackd_config, 'jackd'),
        (update_jacktrip_config, 'jacktrip'),
        (update_snapserver_config, 'snapserver'),
    ):
        if method(config):
            restart_services.add(services)

    return list(restart_services)


def systemctl(*args):
    cmd = [SYSTEMCTL_CMD, *args]
    print(f'EXEC {cmd}')
    return subprocess.run(cmd)


def restart_services(services: List[str]):
    if 'system' in services:
        systemctl('reboot')
        return

    if 'jackd' in services:
        systemctl('stop', 'snapserver')
        systemctl('stop', 'jacktrip')
        systemctl('restart', 'jackd')
        systemctl('start', 'jacktrip')
        systemctl('start', 'snapserver')
    elif 'jacktrip' in services:
        systemctl('restart', 'jacktrip')
    elif 'snapserver' in services:
        systemctl('restart', 'snapserver')


def get_service_status(services: List[str]):
    cmd = [SYSTEMCTL_CMD, 'is-active', *services]
    proc = subprocess.run(cmd, capture_output=True)
    result = {service: 'unknown' for service in services}
    status = list(proc.stdout.decode('utf-8').splitlines())
    result.update(zip(services, status))
    return result


def get_service_logs(services: List[str], num_lines=1000):
    cmd = [JOURNALCTL_CMD, '-n', str(num_lines), '--no-pager']
    for service in services:
        cmd.append('-u')
        cmd.append(service)
    proc = subprocess.run(cmd, capture_output=True)
    return proc.stdout.decode('utf-8').strip()



def striplines(text: str):
    return '\n'.join(line.strip() for line in text.splitlines())


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/config')
async def get_config():
    return load_config()


@app.post('/api/config')
async def post_config(config: Config):
    if not store_config(config):
        return []
    return update_config(config)


@app.post('/api/restart')
async def post_restart(services: List[str]):
    restart_services(services)


@app.get('/api/status')
async def get_status():
    return get_service_status([
        'jackd',
        'jacktrip',
        'snapserver',
    ])


@app.get('/api/logs')
async def get_logs(services: Annotated[List[str], Query()] = [], num_lines=1000):
    return get_service_logs(services, num_lines)


app.mount('/', StaticFiles(directory=FRONTEND_FILES_DIR, html=True), name='static')


@app.exception_handler(404)
async def custom_404_handler(request, exc):
    if '/api/' not in str(request.url):
        return RedirectResponse('/')
    return await http_exception_handler(request, exc)


if __name__ == '__main__':
    update_config(load_config())
