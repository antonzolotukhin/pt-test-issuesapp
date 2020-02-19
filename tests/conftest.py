# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import urlparse

import httpretty
import pytest



def request_callback_get(request, uri, headers):
    # Map path from url to a file
    path = urlparse(uri).path
    response_file = os.path.normpath('tests/resources/{}'.format(path))
    response_file = os.path.join(response_file, 'response.json')

    if os.path.exists(response_file):
        code = 200
        response = open(response_file, mode="r", encoding="utf-8-sig").read()
    else:
        code = 404
        response = '{\n  "message": "\'' + response_file + '\' Not Found",\n  "documentation_url": "https://developer.mockhub.tld/v3"\n}'


    return code, headers, response


@pytest.fixture(autouse=True)
def github_server_mock():
    for method in (httpretty.GET, httpretty.POST, httpretty.PUT, httpretty.PATCH):
        httpretty.register_uri(method, re.compile(r"https://api.github.com/.*"),
                               body=request_callback_get,
                               content_type="application/json")


