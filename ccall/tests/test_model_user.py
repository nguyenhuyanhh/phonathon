# -*- coding: utf-8 -*-
"""Tests for model PhonathonUser."""

from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.test import TestCase

from ..models.pool import Pool
from ..models.project import Project
from ..models.user import Assignment, PhonathonUser


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

    def test_string_user(self):
        """Test the string representation for PhonathonUser."""
        self.assertEqual(str(self.test_user), 'Alex Ang (AlexA)')

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
        """Test adding new user via custom manager."""
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


class TestAssignment(TestCase):
    """Test cases for Assignment."""

    @classmethod
    def setUpTestData(cls):
        cls.caller_obj = PhonathonUser.objects.create_user(
            'test', password='test', name='Test')
        cls.project_obj = Project.objects.create(name='Project')
        # create 5 pools
        for i in range(1, 6):
            setattr(cls, 'pool_obj_{}'.format(i),
                    Pool.objects.create(name='Pool {}'.format(i),
                                        project=cls.project_obj))

    def test_string_assignment(self):
        """Test the string representation for Assignment."""
        test_assignment = Assignment(
            caller=self.caller_obj, pool=self.pool_obj_1, order=1)
        self.assertEqual(str(test_assignment), 'Test (test): (1) Pool 1')

    def test_get_current_pool(self):
        """Test get_current_pool() function."""
        for i in range(1, 6):
            Assignment.objects.create(caller=self.caller_obj,
                                      pool=getattr(self,
                                                   'pool_obj_{}'.format(i)),
                                      order=i)
        self.assertEqual(Assignment.objects.get_current_pool(
            self.caller_obj), self.pool_obj_1)

    def test_get_current_pool_order_not_1(self):
        """Test get_current_pool() when orders do not start from 1."""
        for i in range(1, 6):
            Assignment.objects.create(caller=self.caller_obj,
                                      pool=getattr(self,
                                                   'pool_obj_{}'.format(i)),
                                      order=i + 2)
        self.assertEqual(Assignment.objects.get_current_pool(
            self.caller_obj), self.pool_obj_1)
