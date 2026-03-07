from __future__ import annotations

import json
import sys
from collections.abc import Iterator
from typing import IO, Any

from django.core.management import BaseCommand

from django_urr import extract_urls


class Command(BaseCommand):
    requires_migrations_checks = False

    def add_arguments(self, parser) -> None:
        parser.add_argument("-f", "--format", choices={"json", "jsonl"}, default="jsonl")

    def handle(self, format: str, **options: Any) -> None:
        formatter = getattr(self, f"format_{format}")
        formatter(objects=self.get_objects(), output=sys.stdout)

    def get_objects(self) -> Iterator[dict[str, Any]]:
        for entry in extract_urls():
            path, groups = entry.normalize()[0]
            yield {
                "pattern": entry.merged_pattern,
                "path": path,
                "groups": groups,
                "name": entry.qualified_name,
                "namespace": entry.namespace,
            }

    def format_json(self, objects: Iterator[dict[str, Any]], output: IO[str]) -> None:
        json.dump(list(objects), output, indent=2, sort_keys=True)

    def format_jsonl(self, objects: Iterator[dict[str, Any]], output: IO[str]) -> None:
        for obj in objects:
            json.dump(obj, output, sort_keys=True)
            output.write("\n")
