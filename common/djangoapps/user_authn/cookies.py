import json
import logging
import time

from django.conf import settings
from django.contrib.auth.models import User  # lint-amnesty, pylint: disable=imported-auth-user
from django.utils.http import http_date, parse_http_date

log = logging.getLogger(__name__)

def standard_cookie_settings(request):
    cookie_settings = {
        'domain': settings.SHARED_COOKIE_DOMAIN,
        'path': '/',
        'httponly': None,
    }
    _set_expires_in_cookie_settings(cookie_settings, request.session.get_expiry_age())
    cookie_settings['secure'] = request.is_secure()

    return cookie_settings

def _set_expires_in_cookie_settings(cookie_settings, expires_in):
    """
    Updates the max_age and expires fields of the given cookie_settings,
    based on the value of expires_in.
    """
    expires_time = time.time() + expires_in
    expires = http_date(expires_time)

    cookie_settings.update({
        'max_age': expires_in,
        'expires': expires,
    })

def set_logged_in_cookies(request, response, user):
    if user.is_authenticated and not user.is_anonymous:
        standard_cookie_settings(request)

    return response
