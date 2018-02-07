# -*- coding: utf-8 -*-
"""Tests for views."""

from __future__ import unicode_literals

from django.test import TestCase
from django.urls import resolve

from ..views import home
from django.contrib.auth.views import LoginView, LogoutView


class TestViews(TestCase):
    """Tests for views."""

    def test_view_home(self):
        """Test whether empty url resolves to default view."""
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_view_login(self):
        """Test whether login/ resolves to login view."""
        view = resolve('/login/')
        self.assertEqual(view.func.view_class, LoginView)

    def test_view_logout(self):
        """Test whether logout/ resolves to logout view."""
        view = resolve('/logout/')
        self.assertEqual(view.func.view_class, LogoutView)
