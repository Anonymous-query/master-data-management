import logging
import urllib.parse

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from common.djangoapps.util.cache import cache_if_anonymous
from common.djangoapps.mdmmako.shortcuts import render_to_response, render_to_string

log = logging.getLogger(__name__)

@ensure_csrf_cookie
@transaction.non_atomic_requests
@cache_if_anonymous()
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    context = {}
    return render_to_response('index.html', context)
 