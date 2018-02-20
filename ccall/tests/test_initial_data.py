# -*- coding: utf-8 -*-
"""Tests for initial data created during data migration."""

from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.test import TestCase

from ..models import PhonathonUser, ResultCode


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
        self.assertEqual(ResultCode.objects.count(), 13)

    def test_initial_result_code_type(self):
        """Tests for the types of initial result codes."""
        self.assertEqual(ResultCode.objects.filter(
            is_complete=False).count(), 2)
        self.assertEqual(ResultCode.objects.filter(
            is_complete=True).count(), 11)
