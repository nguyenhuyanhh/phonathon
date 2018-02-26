# -*- coding: utf-8 -*-
"""Tests for models."""

from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.test import TestCase

from ..models import (Call, Fund, PhonathonUser, Pledge, Pool, Project,
                      Prospect, ResultCode)


class TestStrings(TestCase):
    """Tests for string representation for all models in the project."""

    @classmethod
    def setUpTestData(cls):
        cls.test_user = PhonathonUser(username='AlexA', name='Alex Ang')
        cls.test_prospect = Prospect(name='Alex Ang', nric='S1234567A')
        cls.test_fund = Fund(name='NTU Bursaries')
        cls.test_project = Project(name='Alumni Giving 2018')
        cls.test_pool = Pool(name='AQ2017')
        cls.test_result_code = ResultCode(result_code='Specified Pledge (EM)')

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

    def test_string_project(self):
        """Test the string representation for Project."""
        self.assertEqual(str(self.test_project), 'Alumni Giving 2018')

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


class TestPhonathonUser(TestCase):
    """Test cases for PhonathonUser."""

    @classmethod
    def setUpTestData(cls):
        cls.test_user = PhonathonUser(username='AlexA', name='Alex Ang')
        cls.test_user.save()

    def test_manager_and_above_manager(self):
        """Test the attribute is_manager_and_above for Managers."""
        self.test_user.groups.add(Group.objects.get(name='Managers'))
        self.assertTrue(self.test_user.is_manager_and_above)

    def test_manager_and_above_superuser(self):
        """Test the attribute is_manager_and_above for superusers."""
        self.test_user.is_superuser = True
        self.assertTrue(self.test_user.is_manager_and_above)

    def test_manager_and_above_other(self):
        """Test the attribute is_manager_and_above for other users."""
        self.assertFalse(self.test_user.is_manager_and_above)
