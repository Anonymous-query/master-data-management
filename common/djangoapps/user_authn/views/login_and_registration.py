import json
import logging
from django.conf import settings
from django.shortcuts import redirect

from django.utils.translation import gettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from common.djangoapps.mdmmako.shortcuts import render_to_response

from common.djangoapps.user_authn.helpers import get_next_url_for_login_page
from common.djangoapps.user_authn.cookies import set_logged_in_cookies

@require_http_methods(['GET'])
@ensure_csrf_cookie
def login_form(request):
    redirect_to = get_next_url_for_login_page(request)

    if request.user.is_authenticated:
        response = redirect(redirect_to)
        response = set_logged_in_cookies(request, response, request.user)
        return response
    
    context = {
        'login_redirect_url': redirect_to,
    }

    response = render_to_response('user_authn/login.html', context)
    return response

@require_http_methods(['GET'])
@ensure_csrf_cookie
def registration_form(request):
    redirect_to = get_next_url_for_login_page(request)
    
    if request.user.is_authenticated:
        response = redirect(redirect_to)
        response = set_logged_in_cookies(request, response, request.user)
        return response
    
    context = {
        'login_redirect_url': redirect_to,
    }
    response = render_to_response('user_authn/register.html', context)
    return response