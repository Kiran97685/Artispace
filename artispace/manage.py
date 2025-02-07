#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artispace.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError(
            "Could not import Django. Are you sure it's installed and available?"
        )
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()