from django.apps import AppConfig
from django.conf import settings

from . import add_lookup, clear_lookups

class MDMmakoConfig(AppConfig):
    name = 'common.djangoapps.mdmmako'
    verbose_name = "MDM Mako Templating"

    def ready(self):
        """
        Setup mako lookup directories.

        IMPORTANT: This method can be called multiple times during application startup. Any changes to this method
        must be safe for multiple callers during startup phase.
        """

        for backend in settings.TEMPLATES:
            if 'mdmmako' not in backend['BACKEND']:
                continue
            namespace = backend['OPTIONS'].get('namespace', 'main')
            directories = backend['DIRS']
            print(namespace)
            clear_lookups(namespace)
            for directory in directories:
                add_lookup(namespace, directory)