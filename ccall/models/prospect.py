# -*- coding: utf-8 -*-"""
"""Models for a Prospect."""

from __future__ import unicode_literals

import logging

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models, transaction
from django.utils import timezone

ccall_log = logging.getLogger('ccall')


class ProspectManager(models.Manager):
    """Custom manager for model Prospect."""

    def get_by_natural_key(self, nric):
        return self.get(nric=nric)

    def from_upload(self, data):
        """Process data from Prospect upload."""
        created = []
        updated = []
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
                updated.append(model_obj)
                ccall_log.debug('Updated Prospect object %s: %s',
                                natural_value, update_obj)
            except Prospect.DoesNotExist:
                # create new prospect
                try:
                    with transaction.atomic():
                        model_obj = self.create(**obj)
                    created.append(model_obj)
                    ccall_log.debug('Created Prospect object: %s', obj)
                except IntegrityError:
                    ccall_log.error('Cannot create Prospect object: %s', obj)
            except BaseException as exc_:
                ccall_log.exception(exc_)
                ccall_log.error(
                    'Exception encountered on Prospect object: %s', obj)
        return created, updated


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

    def natural_key(self):
        return self.nric
