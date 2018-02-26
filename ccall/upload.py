# -*- coding: utf-8 -*-
"""CSV uploading functions for app ccall."""

from __future__ import unicode_literals

import logging

from django.core.exceptions import ObjectDoesNotExist

from .forms import UploadForm
from .models import (Fund, PhonathonUser, Prospect)

ccall_log = logging.getLogger('ccall')


def upload_data(data, model_string):
    """
    Parse the model choice to a Model class and
    corresponding processing function.
    """
    lookup = {
        UploadForm.MODEL_USER: {
            'func': _process_user_data,
            'kwargs': {
                'model': PhonathonUser
            }
        },
        UploadForm.MODEL_FUND: {
            'func': _process_data,
            'kwargs': {
                'model': Fund,
                'natural_key': 'name'
            }
        },
        UploadForm.MODEL_PROSPECT: {
            'func': _process_data,
            'kwargs': {
                'model': Prospect,
                'natural_key': 'nric'
            }
        }
    }
    try:
        result = lookup[model_string]
        result['func'](data, **result['kwargs'])
    except KeyError:
        # Upload is not implemented for this model
        ccall_log.error('Cannot upload %s data', model_string)


def _process_user_data(data, model):
    """Process data for the User model."""
    for obj in data:
        try:
            # default password = username if not exist
            username = obj['username']
            if 'password' not in obj or not obj['password']:
                obj['password'] = username
            try:
                user_obj = model.objects.get_by_natural_key(username)
                # update user
                update_obj = {}
                for attr, value in obj.items():
                    if value != getattr(user_obj, attr):
                        setattr(user_obj, attr, value)
                        update_obj[attr] = value
                # manually set password
                user_obj.set_password(obj['password'])
                user_obj.save()
                ccall_log.debug('Updated %s object %s: %s',
                                model.__name__, username, update_obj)
            except ObjectDoesNotExist:
                # create new user
                user_obj = model.objects.create_user(**obj)
                ccall_log.debug('Created %s object: %s', model.__name__, obj)
        except BaseException as exc_:
            ccall_log.error('(%s) %s', str(exc_), obj)


def _process_data(data, model, natural_key):
    """Process data for models that implement get_by_natural_key()."""
    for obj in data:
        try:
            natural_value = obj[natural_key]
            try:
                model_obj = model.objects.get_by_natural_key(natural_value)
                # update obj
                update_obj = {}
                for attr, value in obj.items():
                    if value != str(getattr(model_obj, attr)):
                        setattr(model_obj, attr, value)
                        update_obj[attr] = value
                model_obj.save()
                ccall_log.debug('Updated %s object %s: %s',
                                model.__name__, natural_value, update_obj)
            except ObjectDoesNotExist:
                # create new obj
                model_obj = model.objects.create(**obj)
                ccall_log.debug('Created %s object: %s', model.__name__, obj)
        except BaseException as exc_:
            ccall_log.error('%s: %s', str(exc_), obj)
