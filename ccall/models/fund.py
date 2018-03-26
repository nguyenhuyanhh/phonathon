# -*- coding: utf-8 -*-"""
"""Models for a Fund."""

from __future__ import unicode_literals

import logging

from django.db import IntegrityError, models, transaction

ccall_log = logging.getLogger('ccall')


class FundManager(models.Manager):
    """Custom manager for model Fund."""

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def from_upload(self, data):
        """Process data from Fund upload."""
        for obj in data:
            try:
                natural_value = obj['name']
                model_obj = self.get_by_natural_key(natural_value)
                # update obj
                update_obj = {}
                for attr, value in obj.items():
                    if value != str(getattr(model_obj, attr)):
                        setattr(model_obj, attr, value)
                        update_obj[attr] = value
                model_obj.save()
                ccall_log.debug('Updated Fund object %s: %s',
                                natural_value, update_obj)
            except Fund.DoesNotExist:
                # create new obj
                try:
                    with transaction.atomic():
                        model_obj = self.create(**obj)
                    ccall_log.debug('Created Fund object: %s', obj)
                except IntegrityError:
                    ccall_log.error('Cannot create Fund object: %s', obj)
            except BaseException as exc_:
                ccall_log.exception(exc_)
                ccall_log.error(
                    'Exception encountered on Fund object: %s', obj)


class Fund(models.Model):
    """Model for a Pledge Fund."""
    objects = FundManager()

    name = models.CharField(verbose_name='Fund name',
                            max_length=50, unique=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name
