# -*- coding: utf-8 -*-
"""Registering models for admin interface."""

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Call, Fund, PhonathonUser, Pledge, Pool, Prospect, ResultCode


class PhonathonUserAdmin(UserAdmin):
    """Admin interface for model User."""
    list_display = ('username', 'name', 'email', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'name', 'email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_active', 'groups')}),
    )


class ProspectAdmin(admin.ModelAdmin):
    """Admin interface for model Prospect."""
    list_display = ('nric', 'name', 'phone_home', 'phone_mobile')
    fieldsets = (
        (None, {'fields': ('nric', 'salutation', 'name',
                           'email', 'phone_home', 'phone_mobile')}),
        ('Address', {'fields': ('address_1',
                                'address_2', 'address_3', 'address_postal')}),
        ('Education', {'fields': ('education_school',
                                  'education_degree', 'education_year')}),
    )
    add_fieldsets = fieldsets


admin.site.register(PhonathonUser, PhonathonUserAdmin)
admin.site.register(Prospect, ProspectAdmin)
admin.site.register(Pledge)
admin.site.register(Fund)
admin.site.register(Pool)
admin.site.register(ResultCode)
admin.site.register(Call)
