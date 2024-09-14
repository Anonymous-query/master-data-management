from django.conf import settings

def page_title_breadcrumbs(*crumbs, **kwargs):
    """
    This function creates a suitable page title in the form:
    Specific | Less Specific | General | edX
    It will output the correct platform name for the request.
    Pass in a `separator` kwarg to override the default of " | "
    """
    separator = kwargs.get("separator", " | ")
    crumbs = [c for c in crumbs if c is not None]
    if crumbs:
        return f'{separator.join(crumbs)}{separator}{settings.PLATFORM_NAME}'
    else:
        return settings.PLATFORM_NAME