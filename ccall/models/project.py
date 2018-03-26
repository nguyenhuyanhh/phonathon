# -*- coding: utf-8 -*-"""
"""Models for a Project."""

from __future__ import unicode_literals

from django.db import models


class ProjectManager(models.Manager):
    """Custom manager for Project."""

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Project(models.Model):
    """Model for a Project."""
    objects = ProjectManager()

    name = models.CharField(
        max_length=50, verbose_name='Project name', unique=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name
