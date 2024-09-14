"""
Utilities for use in Mako markup.
"""


import markupsafe
import nh3
from lxml.html.clean import Cleaner
from mako.filters import decode

# Text() can be used to declare a string as plain text, as HTML() is used
# for HTML.  It simply wraps markupsafe's escape, which will HTML-escape if
# it isn't already escaped.
Text = markupsafe.escape                        # pylint: disable=invalid-name


def HTML(html):                                 # pylint: disable=invalid-name
    return markupsafe.Markup(html)


def strip_all_tags_but_br(string_to_strip):
    if string_to_strip is None:
        string_to_strip = ""

    string_to_strip = decode.utf8(string_to_strip)
    string_to_strip = nh3.clean(string_to_strip, tags={'br'})

    return HTML(string_to_strip)


def clean_dangerous_html(html):
    if not html:
        return html
    cleaner = Cleaner(style=True, inline_style=False, safe_attrs_only=False)
    html = cleaner.clean_html(html)
    return HTML(html)