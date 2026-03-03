#!/usr/bin/env python
"""Compatibility entrypoint: use Django's manage.py for development commands.

This file previously contained a FastAPI demo. The project is now Django-based.
Running this script behaves like `manage.py` so tools or editors that invoke
``main.py`` will still work.
"""
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?"
        ) from exc
    execute_from_command_line(sys.argv)
