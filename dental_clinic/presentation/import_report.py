from typing import Any, Mapping, List


def format_import_report(result: Mapping[str, Any]) -> List[str]:
    """
    Перетворює результат імпорту у список рядків для виводу.
    Не робить I/O: лише форматування.
    """
    processed = int(result.get("processed", 0))
    failed = int(result.get("failed", 0))
    total_rows = int(result.get("total_rows", 0))
    errors = list(result.get("errors") or [])

    lines: List[str] = []
    lines.append("Dental Clinic — CSV Import")
    lines.append("=" * 50)
    lines.append(f"Processed: {processed}, Failed: {failed}, Total: {total_rows}")
    if errors:
        for e in errors[:20]:
            lines.append(f"  - {e}")
        if len(errors) > 20:
            lines.append(f"  ... +{len(errors) - 20} more")
    else:
        lines.append("OK.")
    lines.append("=" * 50)
    return lines

