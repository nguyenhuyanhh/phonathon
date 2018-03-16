# -*- coding: utf-8 -*-"""
"""Models for a Pledge."""

from __future__ import unicode_literals

import logging
from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import IntegrityError, models, transaction

from ..models.fund import Fund
from ..models.prospect import Prospect

ccall_log = logging.getLogger('ccall')


class PledgeManager(models.Manager):
    """Custom manager for model Pledge."""

    def from_upload(self, data):
        """Process data from Pledge upload."""
        for obj in data:
            try:
                # get the prospect & fund by natural key
                obj['prospect'] = Prospect.objects.get_by_natural_key(
                    obj['prospect'])
                obj['pledge_fund'] = Fund.objects.get_by_natural_key(
                    obj['pledge_fund'])
                obj['pledge_date'] = datetime.strptime(
                    obj['pledge_date'], r'%d/%m/%Y')
                try:
                    with transaction.atomic():
                        self.create(**obj)
                    ccall_log.debug('Created Pledge object: %s', obj)
                except IntegrityError:
                    ccall_log.error('Cannot create Pledge object: %s', obj)
            except Prospect.DoesNotExist:
                # no prospect
                ccall_log.error(
                    'Cannot create Pledge object, no Prospect: %s', obj)
            except Fund.DoesNotExist:
                # no fund
                ccall_log.error(
                    'Cannot create Pledge object, no Fund: %s', obj)
            except BaseException as exc_:
                ccall_log.exception(exc_)
                ccall_log.error(
                    'Exception encountered on Pledge object: %s', obj)


class Pledge(models.Model):
    """Model for a Pledge."""
    objects = PledgeManager()

    pledge_amount = models.DecimalField(
        verbose_name='Pledge amount', decimal_places=2,
        max_digits=12, validators=[MinValueValidator(0)])
    pledge_fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    pledge_date = models.DateField(verbose_name='Pledge date')
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - ${} ({})'.format(
            self.prospect, self.pledge_amount, self.pledge_fund)
