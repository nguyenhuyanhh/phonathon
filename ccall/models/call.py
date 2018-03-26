# -*- coding: utf-8 -*-"""
"""Model for a Call."""

from __future__ import unicode_literals

import logging

from django.core.validators import MinValueValidator
from django.db import IntegrityError, models, transaction

from ..models.pool import Pool
from ..models.project import Project
from ..models.prospect import Prospect
from ..models.result_code import ResultCode
from ..models.user import PhonathonUser

ccall_log = logging.getLogger('ccall')


class CallManager(models.Manager):
    """Custom manager for model Call."""

    def get_by_natural_key(self, caller, prospect, project, pool, attempt):
        return self.get(caller=caller,
                        prospect=prospect,
                        project=project,
                        pool=pool,
                        attempt=attempt)

    def from_upload(self, data):
        """Process data from Call upload."""
        created = []
        updated = []
        for obj in data:
            try:
                # get caller, prospect, project, pool, result code
                obj['caller'] = PhonathonUser.objects.get_by_natural_key(
                    obj['caller'])
                obj['prospect'] = Prospect.objects.get_by_natural_key(
                    obj['prospect'])
                obj['project'] = Project.objects.get_by_natural_key(
                    obj['project'])
                obj['pool'] = Pool.objects.get_by_natural_key(
                    obj['project'], obj['pool'])
                obj['result_code'] = ResultCode.objects.get_by_natural_key(
                    obj['result_code'])
                args = (obj['caller'], obj['prospect'], obj['project'],
                        obj['pool'], obj['attempt'])
                call_obj = self.get_by_natural_key(*args)
                # update Call
                update_obj = {}
                for attr, value in obj.items():
                    if value != getattr(call_obj, attr):
                        setattr(call_obj, attr, value)
                        update_obj[attr] = value
                updated.append(call_obj)
                ccall_log.debug('Updated Call object %s: %s',
                                str(call_obj), update_obj)
            except PhonathonUser.DoesNotExist:
                # no caller
                ccall_log.error(
                    'Cannot create Call object, no PhonathonUser: %s', obj)
            except Prospect.DoesNotExist:
                # no prospect
                ccall_log.error(
                    'Cannot create Call object, no Prospect: %s', obj)
            except Project.DoesNotExist:
                # no project
                ccall_log.error(
                    'Cannot create Call object, no Project: %s', obj)
            except Pool.DoesNotExist:
                # no pool
                ccall_log.error(
                    'Cannot create Call object, no Pool: %s', obj)
            except ResultCode.DoesNotExist:
                # no result code
                ccall_log.error(
                    'Cannot create Call object, no ResultCode: %s', obj)
            except Call.DoesNotExist:
                # create Call
                try:
                    with transaction.atomic():
                        call_obj = self.create(** obj)
                    created.append(call_obj)
                    ccall_log.debug('Created Call object: %s', obj)
                except IntegrityError:
                    ccall_log.error('Cannot create Call object: %s', obj)
            except BaseException as exc_:
                ccall_log.exception(exc_)
                ccall_log.error(
                    'Exception encountered on Call object: %s', obj)
        return created, updated


class Call(models.Model):
    """Model for a Call."""
    objects = CallManager()

    METHOD_CHECK = 'Check'
    METHOD_CREDIT = 'Credit'
    METHOD_EFT = 'EFT'
    METHODS = (
        (METHOD_CHECK, METHOD_CHECK),
        (METHOD_CREDIT, METHOD_CREDIT),
        (METHOD_EFT, METHOD_EFT),
    )
    caller = models.ForeignKey(
        PhonathonUser, verbose_name='Caller', on_delete=models.CASCADE)
    call_time = models.DateTimeField(verbose_name='Time', auto_now=True)
    prospect = models.ForeignKey(
        Prospect, verbose_name='Prospect', on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, verbose_name='Project', on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, verbose_name='Pool',
                             on_delete=models.SET_NULL, null=True)
    attempt = models.PositiveSmallIntegerField(
        verbose_name='Attempt', validators=[MinValueValidator(1)])
    result_code = models.ForeignKey(
        ResultCode, verbose_name='Result code', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comments', blank=True)
    pledge_amount = models.DecimalField(
        verbose_name='Pledge amount', blank=True, null=True, decimal_places=2,
        max_digits=12, validators=[MinValueValidator(0)])
    pledge_method = models.CharField(
        verbose_name='Pledge method', max_length=10,
        choices=METHODS, blank=True)
    pledge_meta = models.TextField(verbose_name='Pledge metadata', blank=True)

    def __str__(self):
        return '{} - {}'.format(self.prospect, self.caller)

    def natural_key(self):
        return (self.caller, self.prospect, self.project,
                self.pool, self.attempt,)
