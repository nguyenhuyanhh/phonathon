# -*- coding: utf-8 -*-
"""Tests for model Pool."""

from __future__ import unicode_literals

from django.test import TestCase

from ..models.pool import Pool, PoolProspects
from ..models.project import Project
from ..models.prospect import Prospect


class TestPool(TestCase):
    """Test cases for Pool."""

    @classmethod
    def setUpTestData(cls):
        cls.prospect_obj_1 = {
            'nric': 'S1234567A',
            'salutation': 'Ms',
            'name': 'Anna Low',
            'gender': 'F',
            'education_school': 'School of Humanities',
            'education_degree': 'B.A (Econs)',
            'education_year': '2017'
        }
        cls.prospect_obj_2 = {
            'nric': 'S1111111A',
            'salutation': 'Mr',
            'name': 'Andy Lau',
            'gender': 'M',
            'education_school': 'School of Computer Science and Engineering',
            'education_degree': 'B.Eng (Computer Science)',
            'education_year': '2015'
        }
        cls.project = Project.objects.create(name='Test Project')
        cls.test_pool = Pool.objects.create(
            name='Test Pool', project=cls.project)
        PoolProspects.objects.create(
            pool=cls.test_pool,
            prospect=Prospect.objects.create(**cls.prospect_obj_1))

    def test_string_pool(self):
        """Test the string representation for Pool."""
        self.assertEqual(str(self.test_pool), 'Test Pool')

    def test_is_active(self):
        """Test the attribute is_active."""
        self.assertFalse(self.test_pool.is_active)
        self.test_pool.max_attempts = 1
        self.test_pool.save()
        self.assertTrue(self.test_pool.is_active)

    def test_from_upload_add_pool(self):
        """Test adding pool via custom manager."""
        Pool.objects.from_upload(
            self.project, 'Test Pool 1', [self.prospect_obj_1])
        self.assertEqual(Pool.objects.count(), 2)
        test_pool = Pool.objects.get(name='Test Pool 1')
        self.assertEqual(test_pool.prospects.count(), 1)

    def test_from_upload_update_pool(self):
        """Test updating pool via custom manager."""
        Pool.objects.from_upload(
            self.project, 'Test Pool', [self.prospect_obj_2])
        self.assertEqual(Pool.objects.count(), 1)
        test_pool = Pool.objects.get(name='Test Pool')
        self.assertEqual(test_pool.prospects.count(), 2)

    def test_from_upload_update_pool_multiple_prospects(self):
        """Test updating pool with multiple prospects."""
        Pool.objects.from_upload(
            self.project, 'Test Pool',
            [self.prospect_obj_1, self.prospect_obj_2])
        self.assertEqual(Pool.objects.count(), 1)
        test_pool = Pool.objects.get(name='Test Pool')
        self.assertEqual(test_pool.prospects.count(), 2)

    def test_from_upload_invalid_pool(self):
        """Test adding invalid pool via custom manager."""
        Pool.objects.from_upload(
            'Test Project', 'Test Pool 1', [self.prospect_obj_1])
        self.assertEqual(Pool.objects.count(), 1)
