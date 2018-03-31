# -*- coding: utf-8 -*-
"""Tests for model Project."""

from __future__ import unicode_literals

from django.test import TestCase

from ..models.project import Project


class TestProject(TestCase):
    """Test cases for Project."""

    def test_string_project(self):
        """Test the string representation for Project."""
        test_project = Project.objects.create(name='Alumni Giving 2018')
        self.assertEqual(str(test_project), 'Alumni Giving 2018')
