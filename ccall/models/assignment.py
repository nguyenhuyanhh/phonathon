# -*- coding: utf-8 -*-"""
"""Models for an Assignment."""

from __future__ import unicode_literals

from django.core.validators import MinValueValidator
from django.db import models

from ..models.pool import Pool
from ..models.user import PhonathonUser


class Assignment(models.Model):
    """
    Model for Pool assignments to PhonathonUser.
    Through model for many-to-many relationship on Pool.
    """
    user = models.ForeignKey(PhonathonUser, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
