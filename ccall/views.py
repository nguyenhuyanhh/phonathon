# -*- coding: utf-8 -*-
"""Views for app ccall."""

from __future__ import unicode_literals

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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
            model.objects.create_user(**obj)
        except BaseException:
            print(obj)


def _process_data(model, data):
    """Process data for other models."""
    for obj in data:
        try:
            model.objects.create(**obj)
        except BaseException:
            print(obj)


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
