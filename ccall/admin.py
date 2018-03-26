# -*- coding: utf-8 -*-
"""Registering models for admin interface."""

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models.call import Call
from .models.fund import Fund
from .models.pledge import Pledge
from .models.pool import Pool
from .models.project import Project
from .models.prospect import Prospect
from .models.result_code import ResultCode
from .models.user import PhonathonUser


@admin.register(PhonathonUser)
class PhonathonUserAdmin(UserAdmin):
    """Admin interface for model User."""
    list_display = ('username', 'name', 'email', 'is_staff', 'is_active')
    list_filter = ('is_active', 'groups')
    search_fields = ('username', 'name')

    fieldsets = [
        (None, {'fields': ('username', 'name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    ]
    add_fieldsets = [
        (None, {'fields': ('username', 'name', 'email',
                           'password1', 'password2')}),
        ('Permissions', {'fields': ('is_active', 'groups')}),
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(PhonathonUserAdmin, self).get_fieldsets(
            request, obj)
        if not request.user.is_manager_and_above:
            # hide group permissions from form if user is supervisor and below
            fieldsets[1] = ('Permissions', {'fields': ('is_active',)})
        return fieldsets


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    """Admin interface for model Prospect."""
    list_display = ('nric', 'name', 'phone_home', 'phone_mobile')
    fieldsets = [
        (None, {'fields': ('nric', 'salutation', 'name', 'gender',
                           'email', 'phone_home', 'phone_mobile')}),
        ('Address', {'fields': ('address_1',
                                'address_2', 'address_3', 'address_postal')}),
        ('Education', {'fields': ('education_school',
                                  'education_degree', 'education_year')}),
    ]
    add_fieldsets = fieldsets


@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    """Admin interface for model Pledge."""
    list_display = ('prospect', 'pledge_fund', 'pledge_amount', 'pledge_date')


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    """Admin interface for model Fund."""
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for model Project."""
    pass


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    """Admin interface for model Pool."""
    pass


@admin.register(ResultCode)
class ResultCodeAdmin(admin.ModelAdmin):
    """Admin interface for model ResultCode."""
    pass


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    """Admin interface for model Call."""
    pass


# Unregister groups, since groups are automatically populated
admin.site.unregister(Group)

# Admin site rendering settings
admin.site.index_title = 'Home'
admin.site.index_template = 'admin/index_no_sidebar.html'
