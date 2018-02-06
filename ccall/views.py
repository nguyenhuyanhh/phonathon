# -*- coding: utf-8 -*-
"""Views for app ccall."""

from __future__ import unicode_literals

from django.http import HttpResponse


def home(request):
    """Default view for ccall."""
    return HttpResponse('Hello, World!')
