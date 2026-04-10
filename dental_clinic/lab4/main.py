"""
Лабораторна 4: Strategy для виводу рядків.
Вичитка з файлу — окремо; вивід — через стратегію з config.json.

Запуск з каталогу dental_clinic:
  python -m lab4.main

Запуск з каталогу lab4:
  python main.py

Перемикання на Kafka: у config.json встанови "output": {"type": "kafka"}
(або скопіюй config.kafka.json у config.json).
"""
import sys
from pathlib import Path

# Підтримка запуску і як модуля (python -m lab4.main), і з папки lab4 (python main.py)
_LAB4_ROOT = Path(__file__).resolve().parent
_CLINIC_ROOT = _LAB4_ROOT.parent
if str(_CLINIC_ROOT) not in sys.path:
    sys.path.insert(0, str(_CLINIC_ROOT))

from lab4.file_reader import read_text_lines
from lab4.output_strategies import load_config, build_strategy_from_config


def main() -> None:
    config_path = _LAB4_ROOT / "config.json"
    cfg = load_config(config_path)

    input_rel = Path(cfg["input"]["file"])
    input_path = (_LAB4_ROOT / input_rel).resolve() if not input_rel.is_absolute() else input_rel

    lines = read_text_lines(input_path)
    strategy = build_strategy_from_config(cfg)
    try:
        strategy.write_lines(lines)
    finally:
        strategy.close()


if __name__ == "__main__":
    main()
