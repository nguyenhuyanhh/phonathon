# -*- coding: utf-8 -*-
"""Tests for app ccall."""

from __future__ import unicode_literals

from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import resolve

from .models import Fund, PhonathonUser, Pledge, Pool, Prospect
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


class TestPhonathonUser(TestCase):
    """Tests for model User."""

    def test_string_representation(self):
        """Test the string representation."""
        test_model = PhonathonUser(username='AlexA', name='Alex Ang')
        self.assertEqual(str(test_model), 'Alex Ang (AlexA)')


class TestProspect(TestCase):
    """Tests for model Prospect."""

    def test_string_representation(self):
        """Test the string representation."""
        test_model = Prospect(name='Alex Ang', nric='S1234567A')
        self.assertEqual(str(test_model), 'Alex Ang (S1234567A)')


class TestFund(TestCase):
    """Tests for model Fund."""

    def test_string_representation(self):
        """Test the string representation."""
        test_model = Fund(name='NTU Bursaries')
        self.assertEqual(str(test_model), 'NTU Bursaries')


class TestPledge(TestCase):
    """Tests for model Pledge."""

    def test_string_representation(self):
        """Test the string representation."""
        test_prospect = Prospect(name='Alex Ang', nric='S1234567A')
        test_fund = Fund(name='NTU Bursaries')
        test_pledge = Pledge(
            pledge_amount=50, pledge_fund=test_fund, prospect=test_prospect)
        self.assertEqual(str(test_pledge),
                         'Alex Ang (S1234567A) - $50 (NTU Bursaries)')


class TestPool(TestCase):
    """Tests for model Pool."""

    def test_string_representation(self):
        """Test the string representation."""
        test_model = Pool(name='AQ2017')
        self.assertEqual(str(test_model), 'AQ2017')


class TestViews(TestCase):
    """Tests for views."""

    def test_view_home(self):
        """Test whether empty url resolves to default view."""
        view = resolve('/')
        self.assertEqual(view.func, home)
