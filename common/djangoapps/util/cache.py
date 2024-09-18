from functools import wraps
from urllib.parse import urlencode

from django.core import cache
from django.utils.translation import get_language

try:
    cache = cache.caches['general']         # pylint: disable=invalid-name
except Exception:  # lint-amnesty, pylint: disable=broad-except
    cache = cache.cache

def cache_if_anonymous(*get_parameters):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if (
                not request.user.is_authenticated
            ):
                cache_key = "cache_if_anonymous." + get_language() + '.' + request.path
                for get_parameter in get_parameters:
                    parameter_value = request.GET.get(get_parameter)
                    if parameter_value is not None:
                        cache_key = cache_key + '.' + urlencode({
                            get_parameter: str(parameter_value).encode('utf-8')
                        })

                response = cache.get(cache_key)
                if response:
                    response_content = list(response._container)
                    response.content = b''
                    for item in response_content:
                        response.write(item)
                else:
                    response = view_func(request, *args, **kwargs)
                    cache.set(cache_key, response, 60 * 3)
                
                return response
            else:
                return view_func(request, *args, **kwargs)
            
        return wrapper
    return decorator

