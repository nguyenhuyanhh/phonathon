# -*- coding: utf-8 -*-
"""Views for app ccall."""

from __future__ import unicode_literals

from django.shortcuts import render


def home(request):
    """Default view for ccall."""
    return render(request, 'ccall/base.html')
