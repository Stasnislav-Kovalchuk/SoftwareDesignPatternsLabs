"""
Паттерн Strategy: різні способи «виводу» рядків без зміни коду клієнта.
Перемикання лише через конфіг (тип стратегії).
"""
from __future__ import annotations

import json
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, List, Mapping, Any

try:
    from kafka import KafkaProducer
except ImportError:
    KafkaProducer = None  # type: ignore


class OutputStrategy(ABC):
    """Інтерфейс стратегії виводу."""

    @abstractmethod
    def write_lines(self, lines: Iterable[str]) -> None:
        """Виводить або відправляє набір рядків."""
        raise NotImplementedError

    def close(self) -> None:
        """Звільнення ресурсів (наприклад, Kafka producer)."""
        pass


class ConsoleOutputStrategy(OutputStrategy):
    """Вивід у консоль (stdout)."""

    def write_lines(self, lines: Iterable[str]) -> None:
        for line in lines:
            print(line, file=sys.stdout)


class KafkaOutputStrategy(OutputStrategy):
    """Вивід у Kafka-топік (кожен рядок — окреме повідомлення)."""

    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        if KafkaProducer is None:
            raise RuntimeError(
                "Пакет kafka-python не встановлено. Виконай: pip install kafka-python"
            )
        servers = [s.strip() for s in bootstrap_servers.split(",") if s.strip()]
        self._topic = topic
        self._producer = KafkaProducer(
            bootstrap_servers=servers,
            value_serializer=lambda v: v.encode("utf-8"),
        )

    def write_lines(self, lines: Iterable[str]) -> None:
        for line in lines:
            self._producer.send(self._topic, value=line)
        self._producer.flush()

    def close(self) -> None:
        if self._producer is not None:
            self._producer.flush()
            self._producer.close()


def build_strategy_from_config(cfg: Mapping[str, Any]) -> OutputStrategy:
    """
    Фабрика стратегій за конфігом.
    Міняєш лише output.type у JSON — код пайплайну не чіпаєш.
    """
    out = cfg.get("output") or {}
    kind = (out.get("type") or "console").strip().lower()

    if kind == "console":
        return ConsoleOutputStrategy()
    if kind == "kafka":
        k = cfg.get("kafka") or {}
        return KafkaOutputStrategy(
            bootstrap_servers=str(k.get("bootstrap_servers", "localhost:9092")),
            topic=str(k.get("topic", "lab4-strategy-output")),
        )
    raise ValueError(f"Невідомий output.type: {kind!r}. Дозволено: console, kafka")


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
