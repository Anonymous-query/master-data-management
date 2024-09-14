"""
Utilities for dealing with Javascript and JSON.
"""

import json

from django.utils.html import escapejs
from mako.filters import decode

def _escape_json_for_js(json_dumps_string):
    json_dumps_string = json_dumps_string.replace("&", "\\u0026")
    json_dumps_string = json_dumps_string.replace(">", "\\u003e")
    json_dumps_string = json_dumps_string.replace("<", "\\u003c")
    return json_dumps_string


def dump_js_escaped_json(obj):
    obj = list(obj) if isinstance(obj, type({}.values())) else obj  # lint-amnesty, pylint: disable=isinstance-second-argument-not-valid-type, line-too-long
    json_string = json.dumps(obj, ensure_ascii=True)
    json_string = _escape_json_for_js(json_string)
    return json_string


def js_escaped_string(string_for_js):
    if string_for_js is None:
        string_for_js = ""
    string_for_js = decode.utf8(string_for_js)
    string_for_js = escapejs(string_for_js)
    return string_for_js