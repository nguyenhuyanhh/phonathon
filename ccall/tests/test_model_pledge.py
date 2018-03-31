# -*- coding: utf-8 -*-
"""Tests for model Pledge."""

from __future__ import unicode_literals

from django.test import TestCase

from ..models.fund import Fund
from ..models.pledge import Pledge
from ..models.prospect import Prospect


class TestPledge(TestCase):
    """Test cases for Pledge."""

    def setUp(self):
        prospect_obj = {
            'nric': 'S1234567A',
            'salutation': 'Ms',
            'name': 'Anna Low',
            'gender': 'F',
            'education_school': 'School of Humanities',
            'education_degree': 'B.A (Econs)',
            'education_year': '2017'
        }
        self.prospect_obj = Prospect.objects.create(**prospect_obj)
        self.fund_obj = Fund.objects.create(name='NTU Bursaries')
        self.pledge_obj_add_1 = {
            'prospect': 'S1234567A',
            'pledge_amount': '50',
            'pledge_fund': 'NTU Bursaries',
            'pledge_date': '01/03/2017'
        }
        self.pledge_obj_add_2 = {
            'prospect': 'S1234567A',
            'pledge_amount': '100',
            'pledge_fund': 'NTU Bursaries',
            'pledge_date': '01/03/2016'
        }
        self.pledge_obj_err = {
            'prospect': 'S1234567A',
            'pledge_amount': '100',
            'pledge_fund': 'NTU Bursaries',
        }

    def test_string_pledge(self):
        test_pledge = Pledge(
            pledge_amount=50,
            pledge_fund=self.fund_obj,
            prospect=self.prospect_obj)
        self.assertEqual(str(test_pledge),
                         'Anna Low (S1234567A) - $50 (NTU Bursaries)')

    def test_from_upload_add_pledge(self):
        """Test adding Pledge via custom manager."""
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
