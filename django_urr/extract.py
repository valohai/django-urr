import itertools

from django import urls
from django.utils.functional import cached_property
from django.utils.regex_helper import normalize

try:  # Django 2.0+
    url_resolver_types = (urls.URLResolver,)
    DJANGO_2 = True
except AttributeError:  # Django 1.11
    url_resolver_types = (urls.RegexURLResolver,)
    DJANGO_2 = False


class URLEntry:
    def __init__(self, url_bits):
        self.bits = url_bits[:]
        self.name = url_bits[-1].name

    def __repr__(self):
        if self.qualified_name:
            return f"<URLEntry {self.merged_pattern!r} (name: {self.qualified_name!r})>"
        return f"<URLEntry {self.merged_pattern!r}>"

    def normalize(self):
        return normalize(self.merged_pattern)

    @cached_property
    def namespace(self):
        return getattr(self.bits[0], "namespace", None)

    @cached_property
    def qualified_name(self):
        if self.name and self.namespace:
            return f"{self.namespace}:{self.name}"
        return self.name

    @cached_property
    def regexes(self):
        if DJANGO_2:
            return [bit.pattern.regex for bit in self.bits]
        return [bit.regex for bit in self.bits]

    @cached_property
    def merged_pattern(self):
        return "".join(re.pattern.lstrip("^").rstrip("$") for re in self.regexes)

    @cached_property
    def named_groups(self):
        keys = (re.groupindex.keys() for re in self.regexes)
        return set(itertools.chain(*keys))

    @cached_property
    def group_count(self):
        return sum(re.groups for re in self.regexes)


def _extract_urls(urlpatterns, parents):
    for pattern in urlpatterns:
        path = parents[:] + [pattern]
        if isinstance(pattern, url_resolver_types):
            yield from _extract_urls(pattern.url_patterns, path)
        else:
            yield URLEntry(path)


def extract_urls(urlpatterns=None):
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
        urlpatterns = urls.get_resolver(None).url_patterns
    yield from _extract_urls(urlpatterns, [])
