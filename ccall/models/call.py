# -*- coding: utf-8 -*-"""
"""Models for a Call."""

from __future__ import unicode_literals

from django.core.validators import MinValueValidator
from django.db import models

from ..models.pool import Pool
from ..models.prospect import Prospect
from ..models.result_code import ResultCode
from ..models.user import PhonathonUser


class Call(models.Model):
    """Model for a Call."""
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
    pool = models.ForeignKey(Pool, verbose_name='Pool',
                             on_delete=models.SET_NULL, null=True)
    result_code = models.ForeignKey(
        ResultCode, verbose_name='Result code', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comments', blank=True)
    pledge_amount = models.DecimalField(
        verbose_name='Pledge amount', blank=True, decimal_places=2,
        max_digits=12, validators=[MinValueValidator(0)])
    pledge_method = models.CharField(
        verbose_name='Pledge method', max_length=10,
        choices=METHODS, blank=True)
    pledge_meta = models.TextField(verbose_name='Pledge metadata', blank=True)

    def __str__(self):
        return '{} - {}'.format(self.prospect, self.caller)
