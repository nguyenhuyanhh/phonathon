# -*- coding: utf-8 -*-
"""Views for app ccall."""

from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def home(request):
    """Default view for ccall."""
    return render(request, 'ccall/base.html')
