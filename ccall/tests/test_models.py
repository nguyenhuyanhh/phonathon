# -*- coding: utf-8 -*-
"""Tests for models."""

from __future__ import unicode_literals

from django.test import TestCase

from ..models import (Call, Fund, PhonathonUser, Pledge,
                      Pool, Prospect, ResultCode)


class TestModels(TestCase):
    """Tests for all the models in the project."""

    def setUp(self):
        self.test_user = PhonathonUser(username='AlexA', name='Alex Ang')
        self.test_prospect = Prospect(name='Alex Ang', nric='S1234567A')
        self.test_fund = Fund(name='NTU Bursaries')
        self.test_pool = Pool(name='AQ2017')
        self.test_result_code = ResultCode(result_code='Specified Pledge (EM)')

    def test_string_user(self):
        """Test the string representation for PhonathonUser."""
        self.assertEqual(str(self.test_user), 'Alex Ang (AlexA)')

    def test_string_prospect(self):
        """Test the string representation for Prospect."""
        self.assertEqual(str(self.test_prospect), 'Alex Ang (S1234567A)')

    def test_string_fund(self):
        """Test the string representation for Fund."""
        self.assertEqual(str(self.test_fund), 'NTU Bursaries')

    def test_string_pledge(self):
        """Test the string representation for Pledge."""
        test_pledge = Pledge(
            pledge_amount=50,
            pledge_fund=self.test_fund,
            prospect=self.test_prospect)
        self.assertEqual(str(test_pledge),
                         'Alex Ang (S1234567A) - $50 (NTU Bursaries)')

    def test_string_pool(self):
        """Test the string representation for Pool."""
        self.assertEqual(str(self.test_pool), 'AQ2017')

    def test_string_result_code(self):
        """Test the string representation for ResultCode."""
        self.assertEqual(str(self.test_result_code), 'Specified Pledge (EM)')

    def test_string_call(self):
        """Test the string representation for Call."""
        test_call = Call(caller=self.test_user, prospect=self.test_prospect)
        self.assertEqual(
            str(test_call), 'Alex Ang (S1234567A) - Alex Ang (AlexA)')