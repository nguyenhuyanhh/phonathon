# -*- coding: utf-8 -*-
"""Tests for app ccall."""

from __future__ import unicode_literals

from django.test import TestCase
from django.urls import resolve

from .models import Pledge, Prospect
from .views import home


class TestProspect(TestCase):
    """Tests for model Prospect."""

    def test_string_representation(self):
        """Test the string representation."""
        test_model = Prospect(name='Alex Ang', nric='S1234567A')
        self.assertEqual(str(test_model), 'Alex Ang (S1234567A)')


class TestPledge(TestCase):
    """Tests for model Pledge."""

    def test_string_representation(self):
        """Test the string representation."""
        test_prospect = Prospect(name='Alex Ang', nric='S1234567A')
        test_pledge = Pledge(
            pledge_amount=50, pledge_fund='Bursaries', prospect=test_prospect)
        self.assertEqual(str(test_pledge),
                         'Alex Ang (S1234567A) - $50 (Bursaries)')


class TestViews(TestCase):
    """Tests for views."""

    def test_view_home(self):
        """Test whether empty url resolves to default view."""
        view = resolve('/')
        self.assertEqual(view.func, home)
