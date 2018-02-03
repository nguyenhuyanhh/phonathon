# -*- coding: utf-8 -*-"""
"""Models for ccall app."""

from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class PhonathonUser(AbstractUser):
    """Model for a User."""
    username = models.CharField(max_length=15, unique=True)
    name = models.CharField(
        max_length=50, verbose_name='Full name', blank=False)
    date_joined = models.DateField(
        verbose_name='Date joined', default=timezone.localdate)
    REQUIRED_FIELDS = ['name', 'email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return '{} ({})'.format(self.name, self.username)


class Prospect(models.Model):
    """Model for a Prospect."""
    nric = models.CharField(max_length=15, verbose_name='NRIC', unique=True)
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    email = models.EmailField(verbose_name='Email address', blank=True)
    address_1 = models.CharField(
        max_length=50, verbose_name='Address (line 1)', blank=True)
    address_2 = models.CharField(
        max_length=50, verbose_name='Address (line 2)', blank=True)
    address_3 = models.CharField(
        max_length=50, verbose_name='Address (line 3)', blank=True)
    address_postal = models.CharField(
        max_length=6, verbose_name='Postal code', blank=True)
    phone_home = models.CharField(
        max_length=8, verbose_name='Home phone', blank=True)
    phone_mobile = models.CharField(
        max_length=8, verbose_name='Mobile phone', blank=True)
    education_school = models.CharField(
        max_length=50, verbose_name='School graduated from')
    education_degree = models.CharField(max_length=50, verbose_name='Degree')
    education_year = models.PositiveIntegerField(verbose_name='Year of graduation', validators=(
        MinValueValidator(1950), MaxValueValidator(timezone.now().year)))

    def __str__(self):
        return '{} ({})'.format(self.name, self.nric)


class Fund(models.Model):
    """Model for a Pledge Fund."""
    name = models.CharField(verbose_name='Fund name',
                            max_length=50, unique=True)

    def __str__(self):
        return self.name


class Pledge(models.Model):
    """Model for a Pledge."""
    pledge_amount = models.DecimalField(
        verbose_name='Pledge amount', decimal_places=2,
        max_digits=12, validators=[MinValueValidator(0)])
    pledge_fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    pledge_date = models.DateField(verbose_name='Pledge date')
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - ${} ({})'.format(self.prospect, self.pledge_amount, self.pledge_fund)


class Pool(models.Model):
    """Model for a Pool."""
    name = models.CharField(max_length=50, verbose_name='Pool name')
    max_attempts = models.PositiveSmallIntegerField(
        verbose_name='Maximum number of attempts')
    prospects = models.ManyToManyField(
        to=Prospect, related_name='prospect_set',
        related_query_name='prospects', verbose_name='Prospects', blank=True)

    def __str__(self):
        return self.name


class ResultCode(models.Model):
    """Model for calling result codes."""
    result_code = models.CharField(
        max_length=25, verbose_name='Result code', unique=True)
    is_complete = models.BooleanField(
        verbose_name='Complete status', default=True)

    def __str__(self):
        return self.result_code


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
        verbose_name='Pledge method', max_length=10, choices=METHODS, blank=True)
    pledge_meta = models.TextField(verbose_name='Pledge metadata', blank=True)

    def __str__(self):
        return '{} - {}'.format(self.prospect, self.caller)
