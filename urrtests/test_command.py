import json

import pytest
from django.core.management import call_command

from django_urr import extract_urls


@pytest.mark.parametrize('format', ('json', 'jsonl'))
def test_list_command(capsys, format):
    urls = list(extract_urls())
    call_command('urr_list', format=format)
    cap = capsys.readouterr()
    objects = None
    if format == 'jsonl':
        objects = [json.loads(line) for line in cap.out.splitlines()]
        assert len(objects) == len(urls)
    elif format == 'json':
        objects = json.loads(cap.out)
        assert isinstance(objects, list)
    assert all(isinstance(obj, dict) for obj in objects)
