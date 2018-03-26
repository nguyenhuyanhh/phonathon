# -*- coding: utf-8 -*-"""
"""Models for a PhonathonUser."""

from __future__ import unicode_literals

import logging

from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import IntegrityError, models, transaction
from django.utils import timezone

from ..models.pool import Pool

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
            except PhonathonUser.DoesNotExist:
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
                    'Exception encountered on PhonathonUser object: %s', obj)


class PhonathonUser(AbstractUser):
    """Model for a User."""
    objects = PhonathonUserManager()

    username = models.CharField(max_length=15, unique=True)
    name = models.CharField(
        max_length=50, verbose_name='Full name', blank=False)
    date_joined = models.DateField(
        verbose_name='Date joined', default=timezone.localdate)
    assignments = models.ManyToManyField(
        to=Pool, through='Assignment', verbose_name='Pool assignments')
    REQUIRED_FIELDS = ['name', 'email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return '{} ({})'.format(self.name, self.username)

    @property
    def is_manager_and_above(self):
        """Check whether an user is a Manager or above."""
        return self.is_superuser or self.groups.filter(name='Managers').count()


class Assignment(models.Model):
    """
    Model for Pool assignments to PhonathonUser.
    Through model for many-to-many relationship on Pool.
    """
    caller = models.ForeignKey(PhonathonUser, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return '{}: ({}) {}'.format(self.caller, self.order, self.pool)
