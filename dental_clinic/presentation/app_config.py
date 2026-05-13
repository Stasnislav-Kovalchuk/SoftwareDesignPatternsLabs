import json
import os
from pathlib import Path
from typing import Any, Mapping


def load_app_config(default_path: Path) -> Mapping[str, Any]:
    """
    Завантажує конфіг застосунку з JSON.

    Перемикання output (console/kafka) робиться лише через конфіг-файл.
    Можна перевизначити шлях через env `DENTAL_CLINIC_CONFIG`.
    """
    env_path = os.getenv("DENTAL_CLINIC_CONFIG")
    path = Path(env_path) if env_path else default_path
    return json.loads(path.read_text(encoding="utf-8"))

