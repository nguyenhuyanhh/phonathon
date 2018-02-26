# -*- coding: utf-8 -*-
"""CSV uploading functions for app ccall."""

from __future__ import unicode_literals

import logging

from django.core.exceptions import ObjectDoesNotExist

from .forms import UploadForm
from .models import Fund, PhonathonUser

ccall_log = logging.getLogger('ccall')


def get_model_func(model_string):
    """
    Parse the model choice to a Model class and
    corresponding processing function.
    """
    lookup = {
        UploadForm.MODEL_USER: {
            "model": PhonathonUser,
            "func": process_user_data
        },
        UploadForm.MODEL_FUND: {
            "model": Fund,
            "func": process_data
        }
    }
    try:
        result = lookup[model_string]
        return result['model'], result['func']
    except KeyError:
        # Upload is not implemented for this model
        ccall_log.error('Cannot upload %s data', model_string)


def process_user_data(model, data):
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
                for attr, value in obj.items():
                    setattr(user_obj, attr, value)
                # manually set password
                user_obj.set_password(obj['password'])
                user_obj.save()
                ccall_log.debug('Updated %s object: %s', model.__name__, obj)
            except ObjectDoesNotExist:
                # create new user
                user_obj = model.objects.create_user(**obj)
                ccall_log.debug('Created %s object: %s', model.__name__, obj)
        except BaseException as exc_:
            ccall_log.error('(%s) %s', str(exc_), obj)


def process_data(model, data):
    """Process data for other models."""
    for obj in data:
        try:
            _, created = model.objects.update_or_create(**obj)
            if created:
                ccall_log.debug('Created %s object: %s', model.__name__, obj)
            else:
                ccall_log.debug('Updated %s object: %s', model.__name__, obj)
        except BaseException as exc_:
            ccall_log.error('%s: %s', str(exc_), obj)
