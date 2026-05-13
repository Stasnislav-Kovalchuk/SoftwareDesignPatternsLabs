"""
Точка входу. 3 рівні: presentation → business → data_access.

  python main.py              — CLI імпорт CSV
  uvicorn main:app --reload   — API + Swagger http://127.0.0.1:8000/docs
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from presentation.controllers import run_import_from_data_folder
from presentation.app_config import load_app_config
from presentation.api import app
from presentation.import_report import format_import_report
from presentation.output_strategies import build_output_strategy


def main():
    cfg = load_app_config(Path(__file__).resolve().parent / "config.json")
    result = run_import_from_data_folder()
    lines = format_import_report(result)

    strategy = build_output_strategy(cfg)
    try:
        strategy.write_lines(lines)
    finally:
        strategy.close()


if __name__ == "__main__":
    main()
