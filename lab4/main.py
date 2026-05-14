import json
import os
import sys
from pathlib import Path

from strategies import create_strategy
from reader import CsvFileReader, ApiReader


def load_config(path: str | None = None):
    config_path = Path(path) if path else (Path(__file__).resolve().parent / "config.json")
    return json.loads(config_path.read_text(encoding="utf-8")), config_path


def prompt_output_type(default_type: str | None):
    options = {
        "1": "console",
        "2": "kafka",
        "3": "redis",
        "4": "file",
    }

    print("Choose output destination:")
    print("1) Console")
    print("2) Kafka")
    print("3) Redis")
    print("4) File")

    prompt = "Enter 1-4"
    if default_type:
        prompt += f" (default: {default_type})"
    prompt += ": "

    while True:
        choice = input(prompt).strip()
        if not choice and default_type:
            return default_type
        if choice in options:
            return options[choice]
        print("Invalid choice. Please enter a number from 1 to 4.")


def main():
    config_arg = None
    for arg in sys.argv[1:]:
        if arg.startswith("-"):
            continue
        config_arg = arg
        break

    config_path = os.getenv("LAB4_CONFIG") or config_arg
    config, config_path = load_config(config_path)
    input_config = config.get("input") or {}
    output_config = config.get("output") or {}

    if "--choose-output" in sys.argv or "--interactive" in sys.argv:
        output_config["type"] = prompt_output_type(output_config.get("type"))

    input_type = (input_config.get("type") or "file").strip().lower()

    if input_type == "api":
        url = input_config.get("url")
        if not url:
            raise ValueError("Config field 'input.url' is required for input.type='api'.")
        reader = ApiReader(
            url=str(url),
            timeout_seconds=int(input_config.get("timeout_seconds", 20)),
            max_items=int(input_config.get("max_items", 100)),
        )
    elif input_type == "file":
        file_path = input_config.get("file")
        if not file_path:
            raise ValueError("Config field 'input.file' is required for input.type='file'.")

        input_path = Path(file_path)
        if not input_path.is_absolute():
            candidate = (config_path.parent / input_path).resolve()
            if candidate.exists():
                input_path = candidate
            else:
                cwd_candidate = (Path.cwd() / input_path).resolve()
                if cwd_candidate.exists():
                    input_path = cwd_candidate
                elif len(input_path.parts) >= 2 and input_path.parts[0] == ".." and input_path.parts[1] == "dental_clinic":
                    # Зручний фолбек для конфігів поза репозиторієм (наприклад, /tmp/*.json)
                    alt = (Path.cwd() / Path(*input_path.parts[1:])).resolve()
                    input_path = alt
                else:
                    input_path = cwd_candidate

        reader = CsvFileReader(
            file_path=str(input_path),
            max_rows=int(input_config.get("max_rows", 100)),
            delimiter=str(input_config.get("delimiter", ";")),
        )
    else:
        raise ValueError("Config field 'input.type' must be 'file' or 'api'.")

    items = reader.read()

    strategy = create_strategy(output_config)
    strategy.write(items)


if __name__ == "__main__":
    main()
