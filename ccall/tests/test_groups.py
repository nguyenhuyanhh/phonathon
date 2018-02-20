# -*- coding: utf-8 -*-
"""Tests for default groups and permissions."""

from __future__ import unicode_literals

from django.contrib.auth.models import Group, Permission
from django.test import TestCase


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
        self.assertEqual(Group.objects.count(), 3)
        self.assertEqual(Group.objects.filter(
            name__in=['Managers', 'Supervisors', 'Callers']).count(), 3)

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

    def test_permissions_project(self):
        """Tests for Project permission."""
        add = Permission.objects.get(codename='add_project')
        change = Permission.objects.get(codename='change_project')
        delete = Permission.objects.get(codename='delete_project')

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
