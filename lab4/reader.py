import csv
from pathlib import Path
from typing import Any


class CsvFileReader:
    """
    Вичитка даних з CSV-файлу (окремо від виводу).
    Повертає список dict (рядки CSV).
    """

    def __init__(
        self,
        file_path: str,
        max_rows: int = 100,
        encoding: str = "utf-8",
        delimiter: str = ";",
    ) -> None:
        self._file_path = Path(file_path)
        self._max_rows = max_rows
        self._encoding = encoding
        self._delimiter = delimiter

    def read(self):
        if not self._file_path.exists():
            raise FileNotFoundError(f"Input file not found: {self._file_path}")

        with self._file_path.open("r", encoding=self._encoding, newline="") as f:
            reader = csv.DictReader(f, delimiter=self._delimiter)
            items = []
            for row in reader:
                items.append(row)
                if len(items) >= self._max_rows:
                    break
            return items


class ApiReader:
    """
    Вичитка даних з HTTP API (окремо від виводу).
    Повертає список dict (елементи JSON).
    """

    def __init__(self, url: str, timeout_seconds: int = 20, max_items: int = 100) -> None:
        self._url = url
        self._timeout_seconds = timeout_seconds
        self._max_items = max_items

    def read(self):
        try:
            import requests
        except ImportError as exc:
            raise RuntimeError("Missing package 'requests'.") from exc

        response = requests.get(self._url, timeout=self._timeout_seconds)
        response.raise_for_status()
        data: Any = response.json()

        if isinstance(data, list):
            items = [item for item in data if isinstance(item, dict)]
            return items[: self._max_items]
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], list):
                items = [item for item in data["data"] if isinstance(item, dict)]
                return items[: self._max_items]
            return [data]
        raise ValueError("API response must be a JSON object or array.")
