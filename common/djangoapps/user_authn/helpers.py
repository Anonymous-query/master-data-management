import json
import logging
import urllib.parse

from django.conf import settings
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext as _

def get_next_url_for_login_page(request):
    # redirect_to = reverse('dashboard')
    redirect_to = '/dashboard'
    return redirect_to

def _get_redirect_to(request_host, request_headers, request_params, request_is_https):
    redirect_to = request_params.get('next')
    return redirect_to
