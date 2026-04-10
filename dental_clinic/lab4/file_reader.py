"""
Вичитка даних з файлу.
Окремо від виводу (Strategy) — Single Responsibility.
"""
from pathlib import Path
from typing import List


def read_text_lines(file_path: Path, encoding: str = "utf-8") -> List[str]:
    """Повертає рядки файлу (без зміни вмісту)."""
    text = file_path.read_text(encoding=encoding)
    return text.splitlines()
