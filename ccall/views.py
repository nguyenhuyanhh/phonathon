# -*- coding: utf-8 -*-
"""Views for app ccall."""

from __future__ import unicode_literals

import logging

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url

from .forms import UploadForm
from .models import Fund, PhonathonUser

ccall_log = logging.getLogger('ccall')


def test_user_manager_and_above(user):
    """Test whether an User is manager and above."""
    return user.is_manager_and_above


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


@login_required(login_url='login')
def home(request):
    """Default view for ccall."""
    return render(request, 'ccall/base.html')


@login_required(login_url='login')
@user_passes_test(test_user_manager_and_above)
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
            model, _func = get_model_func(form.cleaned_data['model'])
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

    def get_success_url(self):
        # if managers and above, redirect to admin interface, else normal
        if self.request.user.is_staff:
            redirect_url = 'admin:index'
        else:
            redirect_url = 'ccall'
        return resolve_url(redirect_url)


class LogoutView(auth_views.LogoutView):
    """Logout view for ccall."""
    next_page = 'login'
