# -*- coding: utf-8 -*-
"""Registering models for admin interface."""

from __future__ import unicode_literals

from django.contrib import admin

from .models import Pledge, Prospect

admin.site.register(Prospect)
admin.site.register(Pledge)
