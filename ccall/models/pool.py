# -*- coding: utf-8 -*-"""
"""Models for a Pool."""

from __future__ import unicode_literals

import logging

from django.core.validators import MinValueValidator
from django.db import models

from ..models.project import Project
from ..models.prospect import Prospect

ccall_log = logging.getLogger('ccall')


class PoolManager(models.Manager):
    """Custom manager for model Pool."""

    def get_by_natural_key(self, project, name):
        return self.get(project=project, name=name)

    def from_upload(self, project, name, data):
        """Process data from Pool upload."""
        try:
            # get the pool by natural key
            pool_obj = self.get_by_natural_key(project, name)
            created, updated = Prospect.objects.from_upload(data)
            pool_obj.prospects.add(*(created + updated))
            ccall_log.debug('Updated Pool object %s', name)
        except Pool.DoesNotExist:
            # create the pool
            pool_obj = self.create(project=project, name=name)
            created, updated = Prospect.objects.from_upload(data)
            pool_obj.prospects.add(*(created + updated))
            ccall_log.debug('Created Pool object %s', name)
        except BaseException as exc_:
            ccall_log.exception(exc_)
            ccall_log.error(
                'Exception encountered on Pool object: %s', name)


class Pool(models.Model):
    """Model for a Pool."""
    objects = PoolManager()

    name = models.CharField(max_length=50, verbose_name='Pool name')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name='Project')
    max_attempts = models.PositiveSmallIntegerField(
        verbose_name='Maximum number of attempts', default=0)
    prospects = models.ManyToManyField(
        to=Prospect, through='PoolProspects',
        verbose_name='Prospects', blank=True)

    class Meta:
        unique_together = ('name', 'project',)

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        return bool(self.max_attempts)

    def prospect_count(self):
        return self.prospects.count()
    prospect_count.short_description = 'Number of prospects'

    def natural_key(self):
        return(self.project, self.name,)


class PoolProspects(models.Model):
    """
    Model for Prospects in Pool.
    Through model for many-to-many relationship on Pool.
    """
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    attempts = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])

    def __str__(self):
        return '{} ({})'.format(self.prospect, self.pool)
