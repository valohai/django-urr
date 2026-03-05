from __future__ import annotations

import itertools
import re
from collections.abc import Iterator
from typing import Union

from django.urls import URLPattern, URLResolver
from django.urls.resolvers import URLResolver as _URLResolver
from django.utils.functional import cached_property
from django.utils.regex_helper import normalize

URLBit = Union[URLResolver, URLPattern]  # noqa: UP007


class URLEntry:
    def __init__(self, url_bits: list[URLBit]) -> None:
        self.bits: list[URLBit] = url_bits[:]
        last = url_bits[-1]
        self.name: str | None = last.name if isinstance(last, URLPattern) else None

    def __repr__(self) -> str:
        if self.qualified_name:
            return f"<URLEntry {self.merged_pattern!r} (name: {self.qualified_name!r})>"
        return f"<URLEntry {self.merged_pattern!r}>"

    def normalize(self) -> list[tuple[str, list[str]]]:
        return normalize(self.merged_pattern)

    @cached_property
    def namespace(self) -> str | None:
        first = self.bits[0]
        if isinstance(first, _URLResolver):
            return first.namespace
        return None

    @cached_property
    def qualified_name(self) -> str | None:
        if self.name and self.namespace:
            return f"{self.namespace}:{self.name}"
        return self.name

    @cached_property
    def regexes(self) -> list[re.Pattern[str]]:
        return [bit.pattern.regex for bit in self.bits]

    @cached_property
    def merged_pattern(self) -> str:
        return "".join(r.pattern.lstrip("^").rstrip("$") for r in self.regexes)

    @cached_property
    def named_groups(self) -> set[str]:
        keys = (r.groupindex.keys() for r in self.regexes)
        return set(itertools.chain(*keys))

    @cached_property
    def group_count(self) -> int:
        return sum(r.groups for r in self.regexes)


def _extract_urls(urlpatterns: list[URLBit], parents: list[URLBit]) -> Iterator[URLEntry]:
    for pattern in urlpatterns:
        path = parents[:] + [pattern]
        if isinstance(pattern, _URLResolver):
            yield from _extract_urls(pattern.url_patterns, path)
        else:
            yield URLEntry(path)


def extract_urls(urlpatterns: list[URLBit] | None = None) -> Iterator[URLEntry]:
    """
    Extract URLEntry objects from the given iterable
    of Django URL pattern objects.  If no iterable is given,
    the patterns exposed by the root resolver are used, i.e.
    all of the URLs routed in the project.

    :param urlpatterns: Iterable of URLPattern objects
    :return: Generator of `URLEntry` objects.
    :rtype: list[URLEntry]
    """
    if urlpatterns is None:
        from django.urls import get_resolver

        urlpatterns = get_resolver(None).url_patterns
    yield from _extract_urls(urlpatterns, [])
