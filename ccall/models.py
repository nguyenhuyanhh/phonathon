# -*- coding: utf-8 -*-"""
"""Models for ccall app."""

from __future__ import unicode_literals

from django.db import models


class Prospect(models.Model):
    """Model for a Prospect."""
    nric = models.CharField(max_length=15)
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50)
    address_3 = models.CharField(max_length=50)
    address_postal = models.CharField(max_length=6)
    phone_home = models.CharField(max_length=8)
    phone_mobile = models.CharField(max_length=8)
    education_school = models.CharField(max_length=50)
    education_degree = models.CharField(max_length=50)
    education_year = models.DateField()
