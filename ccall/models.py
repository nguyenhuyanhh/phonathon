# -*- coding: utf-8 -*-"""
"""Models for ccall app."""

from __future__ import unicode_literals

import logging
from datetime import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models, transaction
from django.utils import timezone

ccall_log = logging.getLogger('ccall')


class PhonathonUserManager(UserManager):
    """Custom manager for model PhonathonUser."""

    def from_upload(self, data):
        """Process data from User upload."""
        for obj in data:
            try:
                # default password = username if not exist
                username = obj['username']
                if 'password' not in obj or not obj['password']:
                    obj['password'] = username
                user_obj = self.get_by_natural_key(username)
                # update user
                update_obj = {}
                for attr, value in obj.items():
                    if value != getattr(user_obj, attr):
                        setattr(user_obj, attr, value)
                        update_obj[attr] = value
                # manually set password
                user_obj.set_password(obj['password'])
                user_obj.save()
                ccall_log.debug('Updated PhonathonUser object %s: %s',
                                username, update_obj)
            except ObjectDoesNotExist:
                # create new user
                try:
                    with transaction.atomic():
                        user_obj = self.create_user(**obj)
                        ccall_log.debug(
                            'Created PhonathonUser object: %s', obj)
                except IntegrityError:
                    ccall_log.error(
                        'Cannot create PhonathonUser object: %s', obj)
            except BaseException as exc_:
                ccall_log.exception(exc_)
                ccall_log.error(
                    'Exception encountered during processing: %s', obj)


class PhonathonUser(AbstractUser):
    """Model for a User."""
    objects = PhonathonUserManager()

    username = models.CharField(max_length=15, unique=True)
    name = models.CharField(
        max_length=50, verbose_name='Full name', blank=False)
    date_joined = models.DateField(
        verbose_name='Date joined', default=timezone.localdate)
    REQUIRED_FIELDS = ['name', 'email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return '{} ({})'.format(self.name, self.username)

    @property
    def is_manager_and_above(self):
        """Check whether an user is a Manager or above."""
        return self.is_superuser or self.groups.filter(name='Managers').count()


class ProspectManager(models.Manager):
    """Custom manager for model Prospect."""

    def get_by_natural_key(self, nric):
        return self.get(nric=nric)

    def from_upload(self, data):
        """Process data from Prospect upload."""
        for obj in data:
            try:
                natural_value = obj['nric']
                model_obj = self.get_by_natural_key(natural_value)
                # update prospect
                update_obj = {}
                for attr, value in obj.items():
                    if value != str(getattr(model_obj, attr)):
                        setattr(model_obj, attr, value)
                        update_obj[attr] = value
                model_obj.save()
                ccall_log.debug('Updated Prospect object %s: %s',
                                natural_value, update_obj)
            except ObjectDoesNotExist:
                # create new prospect
                try:
                    with transaction.atomic():
                        model_obj = self.create(**obj)
                    ccall_log.debug('Created Prospect object: %s', obj)
                except IntegrityError:
                    ccall_log.error('Cannot create Prospect object: %s', obj)
            except BaseException as exc_:
                ccall_log.exception(exc_)
                ccall_log.error(
                    'Exception encountered during processing: %s', obj)


class Prospect(models.Model):
    """Model for a Prospect."""
    objects = ProspectManager()

    # choices for salutation
    SAL_MR = 'Mr'
    SAL_MRS = 'Mrs'
    SAL_MS = 'Ms'
    SAL_MDM = 'Mdm'
    SAL_DR = 'Dr'
    SAL_CHOICES = (
        (SAL_DR, SAL_DR),
        (SAL_MDM, SAL_MDM),
        (SAL_MR, SAL_MR),
        (SAL_MRS, SAL_MRS),
        (SAL_MS, SAL_MS),
    )
    # choices for gender
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = (
        (GENDER_FEMALE, GENDER_FEMALE),
        (GENDER_MALE, GENDER_MALE),
    )

    nric = models.CharField(max_length=15, verbose_name='NRIC', unique=True)
    salutation = models.CharField(
        max_length=3, choices=SAL_CHOICES, blank=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)
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
    education_year = models.PositiveIntegerField(
        verbose_name='Year of graduation', validators=(
            MinValueValidator(1950), MaxValueValidator(timezone.now().year)))

    def __str__(self):
        return '{} ({})'.format(self.name, self.nric)


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
            except ObjectDoesNotExist:
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
                    'Exception encountered during processing: %s', obj)


class Fund(models.Model):
    """Model for a Pledge Fund."""
    objects = FundManager()

    name = models.CharField(verbose_name='Fund name',
                            max_length=50, unique=True)

    def __str__(self):
        return self.name


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
                    'Exception encountered during processing: %s', obj)


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


class Project(models.Model):
    """Model for a Project."""
    name = models.CharField(
        max_length=50, verbose_name='Project name', unique=True)

    def __str__(self):
        return self.name


class Pool(models.Model):
    """Model for a Pool."""
    name = models.CharField(max_length=50, verbose_name='Pool name')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name='Project')
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
        verbose_name='Pledge method', max_length=10,
        choices=METHODS, blank=True)
    pledge_meta = models.TextField(verbose_name='Pledge metadata', blank=True)

    def __str__(self):
        return '{} - {}'.format(self.prospect, self.caller)
