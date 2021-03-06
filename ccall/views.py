# -*- coding: utf-8 -*-
"""Views for app ccall."""

from __future__ import unicode_literals

import logging

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url

from .forms import UploadForm, UploadPoolForm
from .models.call import Call
from .models.fund import Fund
from .models.pledge import Pledge
from .models.pool import Pool
from .models.prospect import Prospect
from .models.user import PhonathonUser

ccall_log = logging.getLogger('ccall')


def upload_data(data, model_string):
    """Parse the model choice to a Model class and process the data."""
    lookup = {
        UploadForm.MODEL_USER: PhonathonUser,
        UploadForm.MODEL_FUND: Fund,
        UploadForm.MODEL_PROSPECT: Prospect,
        UploadForm.MODEL_PLEDGE: Pledge,
        UploadForm.MODEL_CALL: Call,
    }
    try:
        lookup[model_string].objects.from_upload(data)
    except KeyError:
        # Upload is not implemented for this model
        ccall_log.error('Cannot upload %s data', model_string)


def test_user_manager_and_above(user):
    """Test whether an User is manager and above."""
    return user.is_manager_and_above


@login_required(login_url='login')
def home(request):
    """Default view for ccall."""
    return render(request, 'ccall/base.html')


@login_required(login_url='login')
@user_passes_test(test_user_manager_and_above)
def upload(request):
    """Upload Caller/ Fund/ Prospect/ Pledge CSV data from admin interface."""
    import csv
    from io import StringIO

    # if GET, render the form
    if request.method == 'GET':
        return render(request, 'admin/upload.html',
                      {'form': UploadForm,
                       'title': 'Upload Caller/Fund/' +
                                'Prospect/Pledge/Call data'})
    # else process the form
    try:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get data
            csv_file = request.FILES['uploaded_file']
            csv_file.seek(0)
            data = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))

            # upload data
            upload_data(data, form.cleaned_data['model'])

            return HttpResponseRedirect('/admin/')
        else:
            return render(request, 'admin/upload.html',
                          {'form': UploadForm,
                           'title': 'Upload Caller/Fund/' +
                                    'Prospect/Pledge/Call data'})
    except BaseException as exc:
        print(exc)


@login_required(login_url='login')
@user_passes_test(test_user_manager_and_above)
def upload_pool(request):
    """Upload Pool CSV data from admin interface."""
    import csv
    from io import StringIO

    # if GET, render the form
    if request.method == 'GET':
        return render(request, 'admin/upload_pool.html',
                      {'form': UploadPoolForm,
                       'title': 'Upload Pool data'})
    # else process the form
    try:
        form = UploadPoolForm(request.POST, request.FILES)
        if form.is_valid():
            # get data
            csv_file = request.FILES['uploaded_file']
            csv_file.seek(0)
            data = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))

            # upload data
            name = form.cleaned_data['name']
            project = form.cleaned_data['project']
            Pool.objects.from_upload(project, name, data)

            return HttpResponseRedirect('/admin/')
        else:
            return render(request, 'admin/upload_pool.html',
                          {'form': UploadPoolForm,
                           'title': 'Upload Pool data'})
    except BaseException as exc:
        ccall_log.exception(exc)


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
