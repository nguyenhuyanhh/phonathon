# -*- coding: utf-8 -*-
"""Tests for model Prospect."""

from __future__ import unicode_literals

from django.test import TestCase

from ..models.prospect import Prospect


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
        cls.prospect_obj = Prospect.objects.create(**prospect_obj)
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

    def test_string_prospect(self):
        """Test the string representation for Prospect."""
        self.assertEqual(str(self.prospect_obj), 'Anna Low (S1234567A)')

    def test_from_upload_new_prospect(self):
        """Test adding new Prospect via custom manager."""
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
