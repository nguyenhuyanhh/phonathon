# -*- coding: utf-8 -*-
"""App configuration for ccall app."""

from __future__ import unicode_literals

from django.apps import AppConfig


class CcallConfig(AppConfig):
    """App configuration for ccall app."""
    name = 'ccall'
    verbose_name = 'Phonathon'

    def ready(self):
        import ccall.signals  # noqa
