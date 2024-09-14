#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from argparse import ArgumentParser

def parse_args():
    """Parse project specific arguments to manage.py"""
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title='system', description='Master Data Management to run')
    master_data_management = subparsers.add_parser(
        'master_data_management',
        help='master data management Service',
        add_help=False,
        usage='%(prog)s [options] ...'
    )
    master_data_management.add_argument('--settings', help="Which Django settings module to use under finance.settings.")
    master_data_management.add_argument('-h', '--help', action='store_true', help='show this help message and exit')
    master_data_management.set_defaults(
        help_string=master_data_management.format_help(),
        settings_base='master_data_management.settings',
        default_settings='master_data_management.settings.development',
        startup='master_data_management',
    )

    mdm_args, django_args = parser.parse_known_args()
    if mdm_args.help:
        print("Usage:")
        print(mdm_args.help_string)

    return mdm_args, django_args

def main():
    """Run administrative tasks."""
    mdm_args, django_args = parse_args()

    settings_base = mdm_args.settings_base.replace('/', '.') + '.'
    if mdm_args.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = settings_base + mdm_args.settings
    elif os.environ.get("DJANGO_SETTINGS_MODULE") is None:
        os.environ["DJANGO_SETTINGS_MODULE"] = mdm_args.default_settings

    if mdm_args.help:
        print("Django:")
        # This will trigger django-admin.py to print out its help
        django_args.append('--help')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line([sys.argv[0]] + django_args)


if __name__ == '__main__':
    main()
