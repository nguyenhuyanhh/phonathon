# -*- coding: utf-8 -*-
"""Tests for views."""

from __future__ import unicode_literals

from django.test import TestCase
from django.urls import resolve

from ..views import home


class TestViews(TestCase):
    """Tests for views."""

    def test_view_home(self):
        """Test whether empty url resolves to default view."""
        view = resolve('/')
        self.assertEqual(view.func, home)
