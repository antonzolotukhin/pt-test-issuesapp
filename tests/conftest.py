# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import urlparse
import json
import httpretty
import pytest
import pttestissuesapp

def request_callback_get(request, uri, headers):
    """
    Берем содержимое ответов на GET-запросы из файлов,
    расположенных по соответствующему пути.
    Взято с devopshq/tfs.
    """
    code, response = get_from_file(uri)
    return code, headers, response


def get_from_file(uri):
    path = urlparse(uri).path
    response_file = os.path.normpath('tests/resources/{}'.format(path))
    response_file = os.path.join(response_file, 'response.json')

    if os.path.exists(response_file):
        code = 200
        response = open(response_file, mode="r", encoding="utf-8-sig").read()
    else:
        code = 404
        response = '''{\n  "message": "Not Found",\n
                   "documentation_url": "https://developer.mockhub.tld/v3"\n}
                   '''
    return code, response


@pytest.fixture(autouse=True)
def github_server_mock():
    """
    Подменяем GET-запросы во всех (autouse=True) тестах
    """
    for method in (httpretty.GET, httpretty.POST,
                   httpretty.PUT, httpretty.PATCH):
        httpretty.register_uri(method, re.compile(r"https://api.*/.*"),
                               body=request_callback_get,
                               content_type="application/json")


@pytest.fixture
def GitHubAPIRequest_mock(mocker):
    """
    Подмена функции GitHubAPIRequest()
    """
    def fakeGitHubAPIRequest(url: str, creds: str = ''):
        uri = f'https://{creds}api.github.com/{url}'
        code, response = get_from_file(uri)
        print(f'fakeGitHubAPIRequest: {uri}')
        return json.loads(response)
    mocker.patch('pttestissuesapp.issuesapp.GitHubAPIRequest', new=fakeGitHubAPIRequest)
