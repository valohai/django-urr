import itertools

from django.urls import get_resolver, URLResolver
from django.utils.functional import cached_property
from django.utils.regex_helper import normalize


class URLEntry:
    def __init__(self, url_bits):
        self.bits = url_bits[:]
        self.name = url_bits[-1].name

    def normalize(self):
        return normalize(self.merged_pattern)

    @cached_property
    def namespace(self):
        return getattr(self.bits[0], 'namespace', None)

    @cached_property
    def qualified_name(self):
        if self.name and self.namespace:
            return '{namespace}:{name}'.format(namespace=self.namespace, name=self.name)
        return self.name

    @cached_property
    def regexes(self):
        return [bit.pattern.regex for bit in self.bits]

    @cached_property
    def merged_pattern(self):
        return ''.join(
            re.pattern.lstrip('^').rstrip('$')
            for re
            in self.regexes
        )

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
        if isinstance(pattern, URLResolver):
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
        urlpatterns = get_resolver(None).url_patterns
    yield from _extract_urls(urlpatterns, [])
