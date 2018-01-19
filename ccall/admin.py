# -*- coding: utf-8 -*-
"""Registering models for admin interface."""

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PhonathonUser, Pledge, Prospect


class PhonathonUserAdmin(UserAdmin):
    """Admin interface for model User."""
    list_display = ('username', 'name', 'email', 'is_staff')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
                                    'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {'fields': ('name', 'email', 'password1', 'password2')}),
    )


admin.site.register(PhonathonUser, PhonathonUserAdmin)
admin.site.register(Prospect)
admin.site.register(Pledge)
