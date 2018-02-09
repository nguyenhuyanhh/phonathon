# -*- coding: utf-8 -*-
"""Views for app ccall."""

from __future__ import unicode_literals

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def home(request):
    """Default view for ccall."""
    return render(request, 'ccall/base.html')


class LoginView(auth_views.LoginView):
    """Login view for ccall."""
    template_name = 'ccall/login.html'


class LogoutView(auth_views.LogoutView):
    """Logout view for ccall."""
    pass
