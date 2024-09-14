from crum import get_current_request
from django.template import RequestContext
from common.mdm_django_utils.cache import RequestCache

# from common.lib.request_utils import safe_get_host


def get_template_request_context(request=None):
    """
    Returns the template processing context to use for the current request,
    or returns None if there is not a current request.
    """

    if request is None:
        request = get_current_request()

    if request is None:
        return None
    
    request_cache_dict = RequestCache('edxmako').data
    cache_key = "request_context"
    if cache_key in request_cache_dict:
        return request_cache_dict[cache_key]

    context = RequestContext(request)

    context['is_secure'] = request.is_secure()
    # context['site'] = safe_get_host(request)

    request_cache_dict[cache_key] = context
    return context