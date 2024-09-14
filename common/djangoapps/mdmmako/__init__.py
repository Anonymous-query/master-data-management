LOOKUP = {}

from .paths import add_lookup, clear_lookups, lookup_template, save_lookups  # lint-amnesty, pylint: disable=wrong-import-position


class Engines:
    """
    Aliases for the available template engines.
    Note that the preview engine is only configured for cms.
    """
    DJANGO = 'django'
    MAKO = 'mako'
    PREVIEW = 'preview'