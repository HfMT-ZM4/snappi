from pathlib import Path
import subprocess

from .settings import settings


def systemctl(*args):
    cmd = [settings.bin_path / 'systemctl', *args]
    return subprocess.run(cmd)


def restart_services(services: list[str]):
    if 'system' in services:
        systemctl('reboot')
        return

    if 'uac2' in services:
        systemctl('restart', 'uac2')

    if 'jacktrip' in services:
        systemctl('restart', 'jacktrip')

    if 'snapserver' in services:
        systemctl('restart', 'snapserver')


def get_service_status(services: list[str]):
    cmd = [settings.bin_path / 'systemctl', 'is-active', *services]
    proc = subprocess.run(cmd, capture_output=True)
    result = {service: 'unknown' for service in services}
    status = list(proc.stdout.decode('utf-8').splitlines())
    result.update(zip(services, status))
    return result


def get_service_logs(services: list[str], num_lines=1000):
    cmd = [settings.bin_path / 'journalctl', '-n', str(num_lines), '--no-pager']
    for service in services:
        cmd.append('-u')
        cmd.append(service)
    proc = subprocess.run(cmd, capture_output=True)
    return proc.stdout.decode('utf-8').strip()
