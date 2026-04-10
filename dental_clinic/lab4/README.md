# Лабораторна 4 — паттерн Strategy

## Вимога

- Код **вичитки з файлу** відокремлений від коду **виводу**.
- Вивід організований через **Strategy** (консоль / Kafka).
- Перемикання **без зміни коду пайплайну** — лише через **конфіг** (`config.json`).

## Структура

| Файл | Роль |
|------|------|
| `file_reader.py` | Тільки читання рядків з файлу |
| `output_strategies.py` | Strategy: `ConsoleOutputStrategy`, `KafkaOutputStrategy`, фабрика за конфігом |
| `main.py` | Зв’язує reader + strategy |
| `config.json` | `output.type`: `console` або `kafka` |
| `config.kafka.json` | Приклад конфігу для Kafka (можна скопіювати в `config.json`) |

## Запуск (консоль)

З каталогу `dental_clinic`:

```bash
python -m lab4.main
```

## Перемикання на Kafka

1. Встанови залежність:

```bash
pip install -r lab4/requirements-lab4.txt
```

2. Запусти Kafka (локально або кластер).

3. У `lab4/config.json` зміни:

```json
"output": { "type": "kafka" }
```

і за потреби відредагуй `kafka.bootstrap_servers` та `kafka.topic`.

Або скопіюй `config.kafka.json` → `config.json`.

4. Знову:

```bash
python -m lab4.main
```

Код `main.py` і `file_reader.py` **не змінюються** — лише конфіг.
