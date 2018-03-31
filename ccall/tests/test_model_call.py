# -*- coding: utf-8 -*-
"""Tests for model Call."""

from __future__ import unicode_literals

from django.test import TestCase

from ..models.call import Call
from ..models.pool import Pool
from ..models.project import Project
from ..models.prospect import Prospect
from ..models.result_code import ResultCode
from ..models.user import PhonathonUser


class TestCall(TestCase):
    """Test cases for Call."""

    def setUp(self):
        caller_obj = {
            'username': 'Test1',
            'password': 'Test1',
            'name': 'Test User 1'
        }
        caller_obj = PhonathonUser.objects.create_user(**caller_obj)
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
        project_obj = Project.objects.create(name='Project 1')
        self.pool_obj = Pool.objects.create(
            name='Pool 1', project=project_obj)
        self.call_obj = Call.objects.create(caller=caller_obj,
                                            prospect=self.prospect_obj,
                                            project=project_obj,
                                            pool=self.pool_obj,
                                            attempt=1,
                                            result_code=ResultCode.objects.get(
                                                result_code='No Answer'))
        self.call_obj_add = {
            'caller': 'Test1',
            'prospect': 'S1234567A',
            'project': 'Project 1',
            'pool': 'Pool 1',
            'result_code': 'No Answer',
            'attempt': 2
        }
        self.call_obj_upd = {
            'caller': 'Test1',
            'prospect': 'S1234567A',
            'project': 'Project 1',
            'pool': 'Pool 1',
            'result_code': 'No Pledge',
            'attempt': 1
        }
        self.call_obj_err = {
            'caller': 'Test1',
            'prospect': 'S1234567A',
            'project': 'Project 2',
            'pool': 'Pool 1',
            'result_code': 'Not Available',
            'attempt': 3
        }

    def test_string_call(self):
        """Test the string representation for Call."""
        self.assertEqual(str(self.call_obj),
                         'Anna Low (S1234567A) - Test User 1 (Test1)')

    def test_from_upload_add_call(self):
        """Test adding Call via custom manager."""
        created, updated = Call.objects.from_upload([self.call_obj_add])
        self.assertEqual(Call.objects.count(), 2)
        self.assertEqual(len(created), 1)
        self.assertEqual(len(updated), 0)

    def test_from_upload_update_call(self):
        """Test updating Call via custom manager."""
        created, updated = Call.objects.from_upload([self.call_obj_upd])
        self.assertEqual(Call.objects.count(), 1)
        self.assertEqual(
            Call.objects.first().result_code,
            ResultCode.objects.get(result_code='No Pledge'))
        self.assertEqual(len(created), 0)
        self.assertEqual(len(updated), 1)

    def test_from_upload_multiple_call(self):
        """Test adding/ updating multiple Calls via custom manager."""
        created, updated = Call.objects.from_upload(
            [self.call_obj_upd, self.call_obj_add])
        self.assertEqual(Call.objects.count(), 2)
        self.assertEqual(len(created), 1)
        self.assertEqual(len(updated), 1)

    def test_from_upload_multiple_call_error(self):
        """Test adding multiple Calls via custom manager, with errors."""
        created, updated = Call.objects.from_upload(
            [self.call_obj_err, self.call_obj_add])
        self.assertEqual(Call.objects.count(), 2)
        self.assertEqual(len(created), 1)
        self.assertEqual(len(updated), 0)
