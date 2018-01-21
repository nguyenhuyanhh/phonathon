# -*- coding: utf-8 -*-
"""Tests for app ccall."""

from __future__ import unicode_literals

from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import resolve

from .models import PhonathonUser, Pledge, Prospect
from .views import home


class TestGroups(TestCase):
    """Tests for default groups and permissions."""

    def test_groups(self):
        """Tests for existence of groups."""
        self.assertEqual(len(Group.objects.all()), 3)
        self.assertEqual(len(Group.objects.filter(name__exact='Managers')), 1)
        self.assertEqual(
            len(Group.objects.filter(name__exact='Supervisors')), 1)
        self.assertEqual(len(Group.objects.filter(name__exact='Callers')), 1)

    def test_permissions_prospect(self):
        """Tests for Prospect permission."""
        add = Permission.objects.get(codename='add_prospect')
        change = Permission.objects.get(codename='change_prospect')
        delete = Permission.objects.get(codename='delete_prospect')
        manager_perms = Group.objects.get(name='Managers').permissions.all()
        supervisor_perms = Group.objects.get(
            name='Supervisors').permissions.all()
        caller_perms = Group.objects.get(name='Callers').permissions.all()

        self.assertIn(add, manager_perms)
        self.assertIn(change, manager_perms)
        self.assertIn(delete, manager_perms)
        self.assertNotIn(add, supervisor_perms)
        self.assertIn(change, supervisor_perms)
        self.assertNotIn(delete, supervisor_perms)
        self.assertNotIn(add, caller_perms)
        self.assertIn(change, caller_perms)
        self.assertNotIn(delete, caller_perms)

    def test_permissions_pledge(self):
        """Tests for Pledge permission."""
        add = Permission.objects.get(codename='add_pledge')
        change = Permission.objects.get(codename='change_pledge')
        delete = Permission.objects.get(codename='delete_pledge')
        manager_perms = Group.objects.get(name='Managers').permissions.all()
        supervisor_perms = Group.objects.get(
            name='Supervisors').permissions.all()
        caller_perms = Group.objects.get(name='Callers').permissions.all()

        self.assertIn(add, manager_perms)
        self.assertIn(change, manager_perms)
        self.assertIn(delete, manager_perms)
        self.assertNotIn(add, supervisor_perms)
        self.assertNotIn(change, supervisor_perms)
        self.assertNotIn(delete, supervisor_perms)
        self.assertNotIn(add, caller_perms)
        self.assertNotIn(change, caller_perms)
        self.assertNotIn(delete, caller_perms)


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
