import json
import logging
from django.conf import settings

from django.utils.translation import gettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from common.djangoapps.mdmmako.shortcuts import render_to_response

@require_http_methods(['GET'])
@ensure_csrf_cookie
def login_form(request, initial_mode="login"):
    context = {}
    response = render_to_response('user_authn/login.html', context)
    return response

@require_http_methods(['GET'])
@ensure_csrf_cookie
def registration_form(request, initial_mode="login"):
    context = {}
    response = render_to_response('user_authn/register.html', context)
    return response