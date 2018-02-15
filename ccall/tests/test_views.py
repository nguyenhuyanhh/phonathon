# -*- coding: utf-8 -*-
"""Tests for views."""

from __future__ import unicode_literals

from django.test import TestCase
from django.urls import resolve
from django.views.generic.base import RedirectView

from ..views import LoginView, LogoutView, home, upload


class TestGenericViews(TestCase):
    """Tests for generic views."""

    def test_resolve_url_root(self):
        """Test whether empty url redirects to default view."""
        view = resolve('/')
        self.assertEqual(view.func.view_class, RedirectView)

    def test_resolve_url_ccall(self):
        """Test whether /ccall/ resolves to default view."""
        view = resolve('/ccall/')
        self.assertEqual(view.func, home)

    def test_resolve_url_login(self):
        """Test whether login/ resolves to login view."""
        view = resolve('/login/')
        self.assertEqual(view.func.view_class, LoginView)

    def test_resolve_url_logout(self):
        """Test whether logout/ resolves to logout view."""
        view = resolve('/logout/')
        self.assertEqual(view.func.view_class, LogoutView)


class TestUploadView(TestCase):
    """Test the upload view."""

    def test_resolve_url_upload(self):
        """Test whether /admin/upload resolves to upload view."""
        view = resolve('/admin/upload/')
        self.assertEqual(view.func, upload)
