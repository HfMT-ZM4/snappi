from pathlib import Path
from dataclasses import dataclass


@dataclass
class Settings:
    root_path: Path = Path('/')
    static_path: Path = Path('/usr/share/snappi-server-config-ui')
    bin_path: Path = Path('/usr/bin')
    host: str = '127.0.0.1'
    port: int = 8000


settings = Settings()
