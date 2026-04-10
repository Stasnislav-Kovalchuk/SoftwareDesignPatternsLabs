"""Presentation Layer (рівень 3) — приймає запит, викликає business, повертає відповідь."""
from pathlib import Path

from business.services import run_import, run_reset_and_import


def import_csv_controller(csv_path: str) -> dict:
    """Отримує шлях до CSV, викликає імпорт з business-шару, повертає результат."""
    return run_import(Path(csv_path))


def run_import_from_data_folder() -> dict:
    """Імпорт з data/dental_data.csv."""
    base = Path(__file__).resolve().parent.parent
    return import_csv_controller(str(base / "data" / "dental_data.csv"))


def run_reset_import_from_data_folder() -> dict:
    """Очистити БД і імпортувати з data/dental_data.csv (demo)."""
    base = Path(__file__).resolve().parent.parent
    return run_reset_and_import(base / "data" / "dental_data.csv")
