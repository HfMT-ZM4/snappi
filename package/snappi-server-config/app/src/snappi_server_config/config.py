import hashlib
from pathlib import Path
from typing import List, Any

from yaml import safe_load
from pydantic import BaseModel

from .settings import settings


SNAPPI_CONFIG_FILE = 'etc/snappi.json'
JACKTRIP_ENV_FILE = 'etc/default/jacktrip'
UAC2_ENV_FILE = 'etc/default/uac2'
SNAPSERVER_ENV_FILE = 'etc/default/snapserver'
SNAPSERVER_CONFIG_FILE = 'etc/snapserver.conf'
HOSTS_FILE = 'etc/hosts'
HOSTNAME_FILE = 'etc/hostname'
CLOUD_INIT_USER_DATA_FILE = 'boot/user-data'
CLOUD_INIT_NETWORK_CONFIG_FILE = 'boot/network-.con'
NM_CONFIG_DIR = 'etc/NetworkManager/system-connections'
NM_CONNECTION_FILENAME = 'wifi.nmconnection'



class StreamInputPort(BaseModel):
    port: str
    channel: str


class StreamConfig(BaseModel):
    name: str
    channels: int
    inputs: List[StreamInputPort] = []


class WifiConfig(BaseModel):
    ssid: str
    password: str
    mode: str
    band: str


class UAC2Config(BaseModel):
    enable: bool
    name: str
    channels: int


class Config(BaseModel):
    hostname: str
    channels: int
    samplerate: int
    bits: int
    periodsize: int
    latency: int
    wifi: WifiConfig
    streams: List[StreamConfig]
    uac2: UAC2Config | None

    def model_post_init(self, __context: Any) -> None:
        """Clean and sort the stream inputs"""
        for stream in self.streams:
            valid_channels = [f'input_{idx}' for idx in range(stream.channels)]
            valid_inputs = [inp for inp in stream.inputs
                            if inp.channel in valid_channels]
            stream.inputs = sorted(valid_inputs, key=lambda x: (x.channel, x.port))


class ServerConfig:
    def __init__(self):
        self.load()

    def load(self):
        json_data = (settings.root_path / SNAPPI_CONFIG_FILE).read_text()
        self.config = Config.model_validate_json(json_data)

    def store(self, config: Config) -> bool:
        old_value = self.config.model_dump_json(indent=2)
        new_value = config.model_dump_json(indent=2)
        if old_value == new_value:
            return False
        self.config = config
        return write_file_if_changed(settings.root_path / SNAPPI_CONFIG_FILE, new_value)

    def activate(self):
        required_restarts = set()

        for method, services in (
            (update_hostname, ['system']),
            (update_wifi_config, ['system']),
            (update_jacktrip_config, ['jacktrip']),
            (update_uac2_config, ['uac2']),
            (update_snapserver_config, ['snapserver']),
        ):
            if method(self.config):
                required_restarts.update(services)

        return list(required_restarts)

    def apply_cloud_init_data(self):
        user_data_path = settings.root_path / CLOUD_INIT_USER_DATA_FILE
        network_config_path = settings.root_path / CLOUD_INIT_USER_DATA_FILE

        ci_user = read_yaml(user_data_path)
        ci_network = read_yaml(network_config_path)

        if not ci_user and not ci_network:
            return

        ci_hostname = ci_user.get('hostname', '')
        if ci_hostname:
            self.config.hostname = ci_hostname

        ap_conf = ci_network.get('wifis', {}).get('wlan0', {}).get('access-points', {})
        try:
            ssid, args = list(ap_conf.items())[0]
            psk = args.get('password')
        except Exception:
            ssid = psk = None
        if ssid and psk:
            self.config.wifi.ssid = ssid
            self.config.wifi.password = psk
            self.config.wifi.mode = 'client'
            self.config.wifi.band = 'auto'

        if user_data_path.exists():
            user_data_path.unlink()

        if network_config_path.exists():
            network_config_path.unlink()

        add_ssh_keys(ci_user)


    def get_pipewire_links(self) -> list[tuple[str, str]]:
        links = []
        for stream in self.config.streams:
            for entry in stream.inputs:
                source_port = f'{stream.name}:::{entry.channel}'
                links.append((entry.port, source_port))
        return links


def _snapserver_source_url(source, **kwargs):
    params = []
    for key, val in kwargs.items():
        if isinstance(val, (list, tuple)):
            params.extend(f'{key}={el}' for el in val)
        else:
            params.append(f'{key}={val}')
    url = '&'.join(params)
    return f'source = {source}:///?{url}'


def update_snapserver_config(config: Config):
    value = striplines(f'''
        SNAPSERVER_OPTS="-c /etc/snapserver.conf --server.datadir=/var/lib/snapserver"
        PIPEWIRE_LATENCY={config.periodsize}/{config.samplerate}
    ''')
    env_changed = write_file_if_changed(settings.root_path / SNAPSERVER_ENV_FILE, value)

    sources = []
    for stream in config.streams:
        sources.append(_snapserver_source_url(
            source='jack',
            name=stream.name,
            sampleformat=f'{config.samplerate}:{config.bits}:{stream.channels}',
            idle_threshold=5000,
            jack_time='true',
        ))

    sources = '\n'.join(sources)

    value = striplines(f'''
        [server]
        user = snappi
        group = audio

        [http]
        doc_root = /usr/share/snapserver/snapweb

        [logging]
        filter = *:trace

        [stream]
        codec = pcm
        buffer = {config.latency}

        {sources}
    ''')

    config_changed = write_file_if_changed(settings.root_path / SNAPSERVER_CONFIG_FILE, value)

    return env_changed or config_changed


def update_hostname(config: Config):
    hosts_changed = False

    hosts_file = settings.root_path / Path(HOSTS_FILE)
    hosts = hosts_file.read_text()
    entry = f'127.0.0.1 {config.hostname}'
    if entry not in hosts:
        hosts = hosts.strip() + f'\n{entry}\n'
        hosts_file.write_text(hosts)
        hosts_changed = True

    hostname_changed = write_file_if_changed(settings.root_path / HOSTNAME_FILE, config.hostname)

    return hosts_changed or hostname_changed


def update_wifi_config(config: Config):
    if config.wifi.mode == 'ap':
        wifi_config = generate_wifi_ap_config(config)
    elif config.wifi.mode == 'client':
        wifi_config = generate_wifi_client_config(config)
    else:
        raise RuntimeError(f'Invalid wifi mode: {config.wifi.mode}')

    config_file = settings.root_path / Path(NM_CONFIG_DIR) / NM_CONNECTION_FILENAME
    config_changed = write_file_if_changed(config_file, wifi_config, mode=0o600)

    file_deleted = False
    for conf in (settings.root_path / Path(NM_CONFIG_DIR)).glob('*.nmconnection'):
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
        JACKTRIP_OPTS="-s --receivechannels {config.channels} --sendchannels 1 --nojackportsconnect --udprt"
        PIPEWIRE_LATENCY={config.periodsize}/{config.samplerate}
    ''')
    return write_file_if_changed(settings.root_path / JACKTRIP_ENV_FILE, value)


def update_uac2_config(config: Config):
    uac2 = config.uac2
    if uac2:
        channel_mask = int('1' * uac2.channels, 2)
        sample_size = config.bits // 8
        enable = 'yes' if uac2.enable else 'no'
        serial = str(hashlib.md5(
            '-'.join([
                uac2.name,
                str(config.samplerate),
                str(config.bits),
                str(uac2.channels),
            ]).encode()
        ).hexdigest())
        value = striplines(f'''
            UAC2_ENABLE="{enable}"
            UAC2_NAME="{uac2.name} ({config.hostname})"
            UAC2_SERIAL="{serial}"
            UAC2_CHANNEL_MASK={channel_mask}
            UAC2_SAMPLE_RATE={config.samplerate}
            UAC2_SAMPLE_SIZE={sample_size}
        ''')
    else:
        value = 'UAC2_ENABLE="no"'
    return write_file_if_changed(settings.root_path / UAC2_ENV_FILE, value)


def write_file_if_changed(filename, value, mode=None):
    file = Path(filename)
    try:
        original = file.read_text()
    except FileNotFoundError:
        original = None
    if original == value:
        return False
    file.write_text(value)
    if mode is not None:
        file.chmod(mode)
    return True


def read_yaml(filename):
    try:
        with Path(filename).open() as f:
            return safe_load(f)
    except:
        return {}


def striplines(text: str):
    return '\n'.join(line.strip() for line in text.splitlines())


def add_ssh_keys(conf):
    keys = []

    for user in conf.get('users', []):
        for key in user.get('ssh_authorized_keys', []):
            keys.append(key)

    if not keys:
        return

    ssh_dir = Path('/root/.ssh')
    if not ssh_dir.exists():
        ssh_dir.mkdir(mode=0o700)

    pubkeys = '\n'.join(keys)

    authfile = ssh_dir / 'authorized_keys'
    authfile.write_text(pubkeys)
    authfile.chmod(0o600)
