# -*- coding: utf-8 -*-"""
"""Models for a Project."""

from __future__ import unicode_literals

from django.db import models


class Project(models.Model):
    """Model for a Project."""
    name = models.CharField(
        max_length=50, verbose_name='Project name', unique=True)

    def __str__(self):
        return self.name
