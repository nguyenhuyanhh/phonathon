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
        cls.user_obj_add = {
            'username': 'Test1',
            'password': 'Test1',
            'name': 'Test User 1'
        }
        cls.user_obj_upd = {
            'username': 'AlexA',
            'name': 'Alex Au'
        }
        cls.user_obj_err = {
            'name': 'Error'
        }

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

    def test_from_upload_new_user(self):
        """Test adding new user via custom manager's from_upload()."""
        PhonathonUser.objects.from_upload([self.user_obj_add])
        # check for 3 users: default admin + test class' + test case'
        self.assertEqual(PhonathonUser.objects.count(), 3)

    def test_from_upload_new_user_no_password(self):
        """Test adding new user via custom manager, with no password."""
        user_obj = self.user_obj_add.copy()
        del user_obj['password']
        PhonathonUser.objects.from_upload([user_obj])
        self.assertTrue(PhonathonUser.objects.get_by_natural_key(
            'Test1').check_password('Test1'))

    def test_from_upload_update_user(self):
        """Test updating user via custom manager."""
        PhonathonUser.objects.from_upload([self.user_obj_upd])
        self.assertEqual(PhonathonUser.objects.count(), 2)
        self.assertEqual(PhonathonUser.objects.get_by_natural_key(
            'AlexA').name, 'Alex Au')

    def test_from_upload_multiple_user(self):
        """Test adding/ updating multiple users via custom manager."""
        PhonathonUser.objects.from_upload(
            [self.user_obj_add, self.user_obj_upd])
        self.assertEqual(PhonathonUser.objects.count(), 3)

    def test_from_upload_multiple_user_with_errors(self):
        """Test adding/ updating multiple users, with errors."""
        PhonathonUser.objects.from_upload(
            [self.user_obj_err, self.user_obj_add])
        self.assertEqual(PhonathonUser.objects.count(), 3)


class TestProspect(TestCase):
    """Test cases for Prospect."""

    @classmethod
    def setUpTestData(cls):
        prospect_obj = {
            'nric': 'S1234567A',
            'salutation': 'Ms',
            'name': 'Anna Low',
            'gender': 'F',
            'education_school': 'School of Humanities',
            'education_degree': 'B.A (Econs)',
            'education_year': '2017'
        }
        Prospect.objects.create(**prospect_obj)
        cls.prospect_obj_add = {
            'nric': 'S1111111A',
            'salutation': 'Mr',
            'name': 'Alex Ang',
            'gender': 'M',
            'education_school': 'Nanyang Business School',
            'education_degree': 'B.BUS',
            'education_year': '2017'
        }
        cls.prospect_obj_upd = {
            'nric': 'S1234567A',
            'salutation': 'Ms',
            'name': 'Anna Low',
            'gender': 'F',
            'education_school': 'School of Humanities',
            'education_degree': 'B.A (Econs)',
            'education_year': '2016'
        }
        cls.prospect_obj_err = {
            'nric': 'S1111112A',
            'salutation': 'Mr',
            'name': 'Alex Ang',
            'gender': 'M'
        }

    def test_from_upload_new_prospect(self):
        """Test adding new Prospect via custom manager's from_upload()."""
        created, updated = Prospect.objects.from_upload(
            [self.prospect_obj_add])
        # check for 2 prospect - 1 from test class and 1 from test case
        self.assertEqual(Prospect.objects.count(), 2)
        self.assertEqual(len(created), 1)
        self.assertEqual(len(updated), 0)

    def test_from_upload_update_prospect(self):
        """Test updating Prospect via custom manager."""
        created, updated = Prospect.objects.from_upload(
            [self.prospect_obj_upd])
        self.assertEqual(Prospect.objects.count(), 1)
        self.assertEqual(Prospect.objects.get_by_natural_key(
            'S1234567A').education_year, 2016)
        self.assertEqual(len(created), 0)
        self.assertEqual(len(updated), 1)

    def test_from_upload_multiple_prospect(self):
        """Test adding/ updating multiple Prospects via custom manager."""
        created, updated = Prospect.objects.from_upload(
            [self.prospect_obj_add, self.prospect_obj_upd])
        self.assertEqual(Prospect.objects.count(), 2)
        self.assertEqual(len(created), 1)
        self.assertEqual(len(updated), 1)

    def test_from_upload_multiple_prospect_with_errors(self):
        """Test adding/ updating multiple Prospects with errors."""
        created, updated = Prospect.objects.from_upload(
            [self.prospect_obj_err, self.prospect_obj_add])
        self.assertEqual(Prospect.objects.count(), 2)
        self.assertEqual(len(created), 1)
        self.assertEqual(len(updated), 0)


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

    def test_from_upload_add_fund(self):
        """Test adding Fund via custom manager's from_upload()."""
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


class TestPledge(TestCase):
    """Test cases for Pledge."""

    @classmethod
    def setUpTestData(cls):
        prospect_obj = {
            'nric': 'S1234567A',
            'salutation': 'Ms',
            'name': 'Anna Low',
            'gender': 'F',
            'education_school': 'School of Humanities',
            'education_degree': 'B.A (Econs)',
            'education_year': '2017'
        }
        Prospect.objects.create(**prospect_obj)
        Fund.objects.create(name='NTU Bursaries')
        cls.pledge_obj_add_1 = {
            'prospect': 'S1234567A',
            'pledge_amount': '50',
            'pledge_fund': 'NTU Bursaries',
            'pledge_date': '01/03/2017'
        }
        cls.pledge_obj_add_2 = {
            'prospect': 'S1234567A',
            'pledge_amount': '100',
            'pledge_fund': 'NTU Bursaries',
            'pledge_date': '01/03/2016'
        }
        cls.pledge_obj_err = {
            'prospect': 'S1234567A',
            'pledge_amount': '100',
            'pledge_fund': 'NTU Bursaries',
        }

    def test_from_upload_add_pledge(self):
        """Test adding Pledge via custom manager's from_upload()."""
        Pledge.objects.from_upload([self.pledge_obj_add_1])
        self.assertEqual(Pledge.objects.count(), 1)

    def test_from_upload_multiple_pledge(self):
        """Test adding multiple Pledges via custom manager."""
        Pledge.objects.from_upload(
            [self.pledge_obj_add_1, self.pledge_obj_add_2])
        self.assertEqual(Pledge.objects.count(), 2)

    def test_from_upload_multiple_pledge_error(self):
        """Test adding multiple Pledges, with errors."""
        Pledge.objects.from_upload(
            [self.pledge_obj_err, self.pledge_obj_add_1])
        self.assertEqual(Pledge.objects.count(), 1)
