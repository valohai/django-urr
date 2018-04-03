import pytest
from django.urls import reverse

from django_urr import extract_urls


@pytest.fixture()
def urls_by_qname():
    return {u.qualified_name: u for u in extract_urls()}


def test_qnames():
    for entry in extract_urls():
        if entry.name and not entry.named_groups and not entry.group_count:
            assert reverse(entry.qualified_name)


def test_named_groups(urls_by_qname):
    assert urls_by_qname['test1'].named_groups == {'a', 'b', 'c'}
    assert urls_by_qname['test2'].named_groups == {'a', 'b', 'c'}
    assert urls_by_qname['test3'].group_count == 3 and not urls_by_qname['test3'].named_groups


def test_merged_pattern(urls_by_qname):
    assert urls_by_qname['admin:auth_user_change'].merged_pattern == r'admin\/auth\/user\/(?P<object_id>.+)\/change\/'
    assert urls_by_qname['test1'].merged_pattern == r'test1\/(?P<a>[^/]+)\/(?P<b>[^/]+)\/(?P<c>[0-9]+)\/'


def test_normalize(urls_by_qname):
    assert urls_by_qname['test1'].normalize()[0] == ('test1/%(a)s/%(b)s/%(c)s/', ['a', 'b', 'c'])


def test_unnamed_url_enumeration():
    assert any(
        e.merged_pattern.startswith(r'unnamed\/') and not e.name
        for e
        in extract_urls()
    )
