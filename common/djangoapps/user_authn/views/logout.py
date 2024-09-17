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
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        response = super().dispatch(request, *args, **kwargs)

        # delete_logged_in_cookies(response)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'target': '/',
            'logout_uri': '/logout',
        })

        return context