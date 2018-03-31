# -*- coding: utf-8 -*-
"""Tests for model ResultCode."""

from __future__ import unicode_literals

from django.test import TestCase

from ..models.result_code import ResultCode


class TestResultCode(TestCase):
    """Test cases for ResultCode."""

    def test_string_result_code(self):
        """Test the string representation for ResultCode."""
        test_result_code = ResultCode.objects.get(
            result_code='Specified Pledge (EM)')
        self.assertEqual(str(test_result_code), 'Specified Pledge (EM)')
