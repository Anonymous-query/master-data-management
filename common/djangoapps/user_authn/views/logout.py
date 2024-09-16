import urllib.parse as parse  # pylint: disable=import-error
from urllib.parse import parse_qs, urlsplit, urlunsplit  # pylint: disable=import-error

import nh3
from django.conf import settings
from django.contrib.auth import logout
from django.views.generic import TemplateView

class LogoutView(TemplateView):
    oauth_client_ids = []
    template_name = 'logout.html'

    default_target = '/'

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
    
    @property
    def target(self):
        target_url = self.request.GET.get('redirect_url') or self.request.GET.get('next')
        if target_url:
            target_url = nh3.clean(parse.unquote(parse.quote_plus(target_url)))

        return target_url
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        response = super().dispatch(request, *args, **kwargs)

        # delete_logged_in_cookies(response)
        return response