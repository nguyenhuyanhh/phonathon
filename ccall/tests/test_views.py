# -*- coding: utf-8 -*-
"""Tests for views."""

from __future__ import unicode_literals

import os

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import resolve
from django.views.generic.base import RedirectView

from ..models import Fund, PhonathonUser, Pledge, Pool, Project, Prospect
from ..views import LoginView, LogoutView, home, upload, upload_pool


class TestResolveURLs(TestCase):
    """Tests for resolving URLs to views."""

    def test_resolve_url_root(self):
        """Test whether empty url redirects to default view."""
        view = resolve('/')
        self.assertEqual(view.func.view_class, RedirectView)

    def test_resolve_url_ccall(self):
        """Test whether /ccall/ resolves to default view."""
        view = resolve('/ccall/')
        self.assertEqual(view.func, home)

    def test_resolve_url_login(self):
        """Test whether login/ resolves to login view."""
        view = resolve('/login/')
        self.assertEqual(view.func.view_class, LoginView)

    def test_resolve_url_logout(self):
        """Test whether logout/ resolves to logout view."""
        view = resolve('/logout/')
        self.assertEqual(view.func.view_class, LogoutView)

    def test_resolve_url_upload(self):
        """Test whether /admin/upload resolves to upload view."""
        view = resolve('/admin/upload/')
        self.assertEqual(view.func, upload)

    def test_resolve_url_upload_pool(self):
        """Test whether /admin/upload_pool resolves to upload_pool view."""
        view = resolve('/admin/upload_pool/')
        self.assertEqual(view.func, upload_pool)


class TestLoginLogout(TestCase):
    """Test the login-logout flow."""

    @classmethod
    def setUpTestData(cls):
        cls.user_normal_credentials = {
            'username': 'test', 'password': 'test'
        }
        user_normal = PhonathonUser.objects.create_user(
            **cls.user_normal_credentials)
        user_normal.groups.add(Group.objects.get(name='Callers'))
        user_normal.save()

    def test_login_template(self):
        """Test for the login template."""
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'ccall/login.html')

    def test_login_normal(self):
        """Test login for normal user."""
        response = self.client.post(
            '/login/', self.user_normal_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][0], '/ccall/')

    def test_login_elevated(self):
        """Test login for elevated users (supervisors and above)."""
        # use the default superuser
        response = self.client.post(
            '/login/', {'username': 'admin', 'password': 'admin'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][0], '/admin/')

    def test_logout(self):
        """Test logout."""
        self.client.post(
            '/login/', self.user_normal_credentials, follow=True)
        response = self.client.post('/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][0], '/login/')


class TestUploadView(TestCase):
    """Test the upload view."""
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(cur_dir, 'test_data')

    @classmethod
    def setUpTestData(cls):
        cls.user = PhonathonUser.objects.create_user(
            username='test', password='test')
        cls.user.groups.add(Group.objects.get(name='Managers'))
        cls.user.save()

    def setUp(self):
        self.client.force_login(self.user)

    def test_upload_user(self):
        """Test upload a user CSV file."""
        data_file = os.path.join(self.data_dir, 'test_user.csv')
        with open(data_file, 'r') as csv_:
            response = self.client.post('/admin/upload/',
                                        {'model': 'Caller',
                                         'uploaded_file': csv_},
                                        follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PhonathonUser.objects.get(username='Test1'))

    def test_upload_fund(self):
        """Test upload a fund CSV file."""
        data_file = os.path.join(self.data_dir, 'test_fund.csv')
        with open(data_file, 'r') as csv_:
            response = self.client.post('/admin/upload/',
                                        {'model': 'Fund',
                                         'uploaded_file': csv_},
                                        follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Fund.objects.get(name='NTU Bursaries'))

    def test_upload_prospect(self):
        """Test upload a fund CSV file."""
        data_file = os.path.join(self.data_dir, 'test_prospect.csv')
        with open(data_file, 'r') as csv_:
            response = self.client.post('/admin/upload/',
                                        {'model': 'Prospect',
                                         'uploaded_file': csv_},
                                        follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Prospect.objects.get(nric='S1234567A'))

    def test_upload_pledge(self):
        """Test upload a pledge CSV file."""
        self.test_upload_fund()
        self.test_upload_prospect()
        data_file = os.path.join(self.data_dir, 'test_pledge.csv')
        with open(data_file, 'r') as csv_:
            response = self.client.post('/admin/upload/',
                                        {'model': 'Pledge',
                                         'uploaded_file': csv_},
                                        follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Pledge.objects.get(prospect__nric='S1234567A'))

    def test_upload_pool(self):
        """Test upload a pool CSV file."""
        project_obj = Project.objects.create(name='Test Project')
        data_file = os.path.join(self.data_dir, 'test_prospect.csv')
        with open(data_file, 'r') as csv_:
            response = self.client.post('/admin/upload_pool/',
                                        {'name': 'Test Pool',
                                         'project': project_obj.id,
                                         'uploaded_file': csv_},
                                        follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Pool.objects.get(name='Test Pool'))
        self.assertEqual(Pool.objects.get(
            name='Test Pool').prospects.count(), 1)
