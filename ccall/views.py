# -*- coding: utf-8 -*-
"""Views for app ccall."""

from __future__ import unicode_literals

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url

from .forms import UploadForm
from .upload import upload_data


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

            # upload data
            upload_data(data, form.cleaned_data['model'])

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
