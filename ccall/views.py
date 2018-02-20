# -*- coding: utf-8 -*-
"""Views for app ccall."""

from __future__ import unicode_literals

import logging

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from .forms import UploadForm
from .models import PhonathonUser


def _get_model_func(model_string):
    """
    Parse the model choice to a Model class and
    corresponding processing function.
    """
    if model_string == UploadForm.MODEL_USER:
        return PhonathonUser, _process_user_data
    else:
        raise NotImplementedError('Cannot upload %s data', model_string)


def _process_user_data(model, data):
    """Process data for the User model."""
    for obj in data:
        try:
            # default password = username if not exist
            username = obj['username']
            if 'password' not in obj or not obj['password']:
                obj['password'] = username
            try:
                user_obj = model.objects.get_by_natural_key(username)
                # update attributes
                for attr, value in obj.items():
                    setattr(user_obj, attr, value)
                # manually set passwords
                user_obj.set_password(obj['password'])
                user_obj.save()
                logging.getLogger('ccall').debug(
                    'Updated %s object: %s', model.__name__, obj)
            except ObjectDoesNotExist:
                # create new user
                user_obj = model.objects.create_user(**obj)
                user_obj.set_password(obj['password'])
                user_obj.save()
                logging.getLogger('ccall').debug(
                    'Created %s object: %s', model.__name__, obj)
        except BaseException as exc_:
            logging.getLogger('ccall').error('(%s) %s', str(exc_), obj)


def _process_data(model, data):
    """Process data for other models."""
    for obj in data:
        try:
            model.objects.update_or_create(**obj)
        except BaseException as exc_:
            logging.getLogger('ccall').error('%s: %s', str(exc_), obj)


@login_required()
def home(request):
    """Default view for ccall."""
    return render(request, 'ccall/base.html')


@login_required()
def upload(request):
    """Upload csv from admin interface."""
    import csv
    from io import StringIO

    # if GET, render the form
    if request.method == 'GET':
        return render(request, 'admin/upload.html',
                      {'form': UploadForm, 'title': 'Upload data'})
    # else process the form
    try:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get data
            csv_file = request.FILES['uploaded_file']
            csv_file.seek(0)
            data = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))

            # process data
            model, _func = _get_model_func(form.cleaned_data['model'])
            _func(model, data)
            return HttpResponseRedirect('/admin/')
        else:
            return render(request, 'admin/upload.html',
                          {'form': UploadForm, 'title': 'Upload data'})
    except BaseException as exc:
        print(exc)


class LoginView(auth_views.LoginView):
    """Login view for ccall."""
    template_name = 'ccall/login.html'


class LogoutView(auth_views.LogoutView):
    """Logout view for ccall."""
    pass
