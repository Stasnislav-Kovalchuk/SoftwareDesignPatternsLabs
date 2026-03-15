"""
Точка входу. 3 рівні: presentation → business → data_access.

  python main.py              — CLI імпорт CSV
  uvicorn main:app --reload   — API + Swagger http://127.0.0.1:8000/docs
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from presentation.controllers import run_import_from_data_folder
from presentation.api import app


def main():
    result = run_import_from_data_folder()
    print("Dental Clinic — CSV Import")
    print("=" * 50)
    print(f"Processed: {result['processed']}, Failed: {result['failed']}, Total: {result['total_rows']}")
    if result["errors"]:
        for e in result["errors"][:20]:
            print(f"  - {e}")
        if len(result["errors"]) > 20:
            print(f"  ... +{len(result['errors']) - 20} more")
    else:
        print("OK.")
    print("=" * 50)


if __name__ == "__main__":
    main()
