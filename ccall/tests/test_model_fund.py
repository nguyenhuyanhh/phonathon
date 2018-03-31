# -*- coding: utf-8 -*-
"""Tests for model Fund."""

from __future__ import unicode_literals

from django.test import TestCase

from ..models.fund import Fund


class TestFund(TestCase):
    """Test cases for Fund."""

    @classmethod
    def setUpTestData(cls):
        cls.fund_obj_add_1 = {
            'name': 'NTU Bursaries'
        }
        cls.fund_obj_add_2 = {
            'name': 'NTU Student Life Activities Fund'
        }
        cls.fund_obj_err = {
            'hello': 'world'
        }

    def test_string_fund(self):
        """Test the string representation for Fund."""
        test_fund = Fund.objects.create(name='Test Fund')
        self.assertEqual(str(test_fund), 'Test Fund')

    def test_from_upload_add_fund(self):
        """Test adding Fund via custom manager."""
        Fund.objects.from_upload([self.fund_obj_add_1])
        self.assertEqual(Fund.objects.count(), 1)

    def test_from_upload_multiple_fund(self):
        """Test adding multiple Funds via custom manager."""
        Fund.objects.from_upload([self.fund_obj_add_1, self.fund_obj_add_2])
        self.assertEqual(Fund.objects.count(), 2)

    def test_from_upload_multiple_fund_with_errors(self):
        """Test adding multiple Funds, with errors."""
        Fund.objects.from_upload([self.fund_obj_err, self.fund_obj_add_1])
        self.assertEqual(Fund.objects.count(), 1)
