# -*- coding: utf-8 -*-
"""Tests for app ccall."""

from __future__ import unicode_literals

from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import resolve

from .models import (Call, Fund, PhonathonUser, Pledge,
                     Pool, Prospect, ResultCode)
from .views import home


class TestGroups(TestCase):
    """Tests for default groups and permissions."""

    def setUp(self):
        self.manager_perms = Group.objects.get(
            name='Managers').permissions.all()
        self.supervisor_perms = Group.objects.get(
            name='Supervisors').permissions.all()
        self.caller_perms = Group.objects.get(name='Callers').permissions.all()

    def test_groups(self):
        """Tests for existence of groups."""
        self.assertEqual(len(Group.objects.all()), 3)
        self.assertEqual(len(Group.objects.filter(
            name__in=['Managers', 'Supervisors', 'Callers'])), 3)

    def test_permissions_user(self):
        """Tests for User permission."""
        add = Permission.objects.get(codename='add_phonathonuser')
        change = Permission.objects.get(codename='change_phonathonuser')
        delete = Permission.objects.get(codename='delete_phonathonuser')

        self.assertIn(add, self.manager_perms)
        self.assertIn(change, self.manager_perms)
        self.assertIn(delete, self.manager_perms)
        self.assertNotIn(add, self.supervisor_perms)
        self.assertIn(change, self.supervisor_perms)
        self.assertNotIn(delete, self.supervisor_perms)
        self.assertNotIn(add, self.caller_perms)
        self.assertNotIn(change, self.caller_perms)
        self.assertNotIn(delete, self.caller_perms)

    def test_permissions_prospect(self):
        """Tests for Prospect permission."""
        add = Permission.objects.get(codename='add_prospect')
        change = Permission.objects.get(codename='change_prospect')
        delete = Permission.objects.get(codename='delete_prospect')

        self.assertIn(add, self.manager_perms)
        self.assertIn(change, self.manager_perms)
        self.assertIn(delete, self.manager_perms)
        self.assertNotIn(add, self.supervisor_perms)
        self.assertIn(change, self.supervisor_perms)
        self.assertNotIn(delete, self.supervisor_perms)
        self.assertNotIn(add, self.caller_perms)
        self.assertIn(change, self.caller_perms)
        self.assertNotIn(delete, self.caller_perms)

    def test_permissions_pledge(self):
        """Tests for Pledge permission."""
        add = Permission.objects.get(codename='add_pledge')
        change = Permission.objects.get(codename='change_pledge')
        delete = Permission.objects.get(codename='delete_pledge')

        self.assertIn(add, self.manager_perms)
        self.assertIn(change, self.manager_perms)
        self.assertIn(delete, self.manager_perms)
        self.assertNotIn(add, self.supervisor_perms)
        self.assertNotIn(change, self.supervisor_perms)
        self.assertNotIn(delete, self.supervisor_perms)
        self.assertNotIn(add, self.caller_perms)
        self.assertNotIn(change, self.caller_perms)
        self.assertNotIn(delete, self.caller_perms)

    def test_permissions_fund(self):
        """Tests for Fund permission."""
        add = Permission.objects.get(codename='add_fund')
        change = Permission.objects.get(codename='change_fund')
        delete = Permission.objects.get(codename='delete_fund')

        self.assertIn(add, self.manager_perms)
        self.assertIn(change, self.manager_perms)
        self.assertIn(delete, self.manager_perms)
        self.assertNotIn(add, self.supervisor_perms)
        self.assertNotIn(change, self.supervisor_perms)
        self.assertNotIn(delete, self.supervisor_perms)
        self.assertNotIn(add, self.caller_perms)
        self.assertNotIn(change, self.caller_perms)
        self.assertNotIn(delete, self.caller_perms)

    def test_permissions_pool(self):
        """Tests for Pool permission."""
        add = Permission.objects.get(codename='add_pool')
        change = Permission.objects.get(codename='change_pool')
        delete = Permission.objects.get(codename='delete_pool')

        self.assertIn(add, self.manager_perms)
        self.assertIn(change, self.manager_perms)
        self.assertIn(delete, self.manager_perms)
        self.assertNotIn(add, self.supervisor_perms)
        self.assertIn(change, self.supervisor_perms)
        self.assertNotIn(delete, self.supervisor_perms)
        self.assertNotIn(add, self.caller_perms)
        self.assertNotIn(change, self.caller_perms)
        self.assertNotIn(delete, self.caller_perms)

    def test_permissions_resultcode(self):
        """Tests for ResultCode permission."""
        add = Permission.objects.get(codename='add_resultcode')
        change = Permission.objects.get(codename='change_resultcode')
        delete = Permission.objects.get(codename='delete_resultcode')

        self.assertIn(add, self.manager_perms)
        self.assertIn(change, self.manager_perms)
        self.assertIn(delete, self.manager_perms)
        self.assertNotIn(add, self.supervisor_perms)
        self.assertNotIn(change, self.supervisor_perms)
        self.assertNotIn(delete, self.supervisor_perms)
        self.assertNotIn(add, self.caller_perms)
        self.assertNotIn(change, self.caller_perms)
        self.assertNotIn(delete, self.caller_perms)

    def test_permissions_call(self):
        """Tests for Call permission."""
        add = Permission.objects.get(codename='add_call')
        change = Permission.objects.get(codename='change_call')
        delete = Permission.objects.get(codename='delete_call')

        self.assertIn(add, self.manager_perms)
        self.assertIn(change, self.manager_perms)
        self.assertIn(delete, self.manager_perms)
        self.assertIn(add, self.supervisor_perms)
        self.assertIn(change, self.supervisor_perms)
        self.assertNotIn(delete, self.supervisor_perms)
        self.assertIn(add, self.caller_perms)
        self.assertNotIn(change, self.caller_perms)
        self.assertNotIn(delete, self.caller_perms)


class TestStaffStatus(TestCase):
    """Tests for staff status."""

    def test_caller_created(self):
        """Test staff status for a newly created caller."""
        test_model = PhonathonUser(username='AlexA', name='Alex Ang')
        test_model.save()
        test_model.groups.add(Group.objects.get(name='Callers'))
        self.assertFalse(test_model.is_staff)

    def test_supervisor_created(self):
        """Test staff status for a newly created supervisor."""
        test_model = PhonathonUser(username='AlexA', name='Alex Ang')
        test_model.save()
        test_model.groups.add(Group.objects.get(name='Supervisors'))
        self.assertTrue(test_model.is_staff)

    def test_manager_created(self):
        """Test staff status for a newly created supervisor."""
        test_model = PhonathonUser(username='AlexA', name='Alex Ang')
        test_model.save()
        test_model.groups.add(Group.objects.get(name='Managers'))
        self.assertTrue(test_model.is_staff)

    def test_change_status(self):
        """Test for status change."""
        test_model = PhonathonUser(username='AlexA', name='Alex Ang')
        test_model.save()
        test_model.groups.add(Group.objects.get(name='Managers'))
        self.assertTrue(test_model.is_staff)
        test_model.groups.remove(Group.objects.get(name='Managers'))
        test_model.groups.add(Group.objects.get(name='Callers'))
        self.assertFalse(test_model.is_staff)


class TestInitialSuperuser(TestCase):
    """Tests for the initial superuser."""

    def test_initial_superuser(self):
        """Tests for the initial superuser."""
        superuser = PhonathonUser.objects.get(username='admin')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)


class TestInitialResultCodes(TestCase):
    """Tests for the initial result codes."""

    def test_initial_result_code_count(self):
        """Tests for the number of initial result codes."""
        self.assertEqual(len(ResultCode.objects.all()), 13)

    def test_initial_result_code_type(self):
        """Tests for the types of initial result codes."""
        self.assertEqual(len(ResultCode.objects.filter(is_complete=False)), 2)
        self.assertEqual(len(ResultCode.objects.filter(is_complete=True)), 11)


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


class TestViews(TestCase):
    """Tests for views."""

    def test_view_home(self):
        """Test whether empty url resolves to default view."""
        view = resolve('/')
        self.assertEqual(view.func, home)
