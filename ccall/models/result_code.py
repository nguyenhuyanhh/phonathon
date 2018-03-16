# -*- coding: utf-8 -*-"""
"""Models for a ResultCode."""

from __future__ import unicode_literals

from django.db import models


class ResultCode(models.Model):
    """Model for calling result codes."""
    result_code = models.CharField(
        max_length=25, verbose_name='Result code', unique=True)
    is_complete = models.BooleanField(
        verbose_name='Complete status', default=True)

    def __str__(self):
        return self.result_code
