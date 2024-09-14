"""
Supports rendering an XBlock to HTML using mako templates.
"""
from django.template import engines
from django.template.utils import InvalidTemplateEngineError

from common.djangoapps.mdmmako.shortcuts import render_to_string
from common.djangoapps.mdmmako import Engines

try:
    engines[Engines.PREVIEW]
except InvalidTemplateEngineError:
    mdm_mako_namespace = "main"
else:
    mdm_mako_namespace = "mdm.main"


class MakoService:
    def __init__(
        self,
        namespace_prefix='',
        **kwargs
    ):
        super().__init__(**kwargs)
        # Set the "default" namespace prefix, in case it's not specified when render_template() is called.
        self.namespace_prefix = namespace_prefix

    def render_template(self, template_file, dictionary, namespace='main'):
        return render_to_string(template_file, dictionary, namespace=self.namespace_prefix + namespace)