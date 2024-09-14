import logging

from django.conf import settings
from django.http import HttpResponse  # lint-amnesty, pylint: disable=unused-import
from django.template import engines

from . import Engines

log = logging.getLogger(__name__)


def render_to_string(template_name, dictionary, namespace='main', request=None):
    engine = engines[Engines.MAKO]
    template = engine.get_template(template_name)
    return template.render(dictionary, request)


def render_to_response(template_name, dictionary=None, namespace='main', request=None, **kwargs):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    lookup.get_template(args[0]).render with the passed arguments.
    """

    dictionary = dictionary or {}
    return HttpResponse(render_to_string(template_name, dictionary, namespace, request), **kwargs)