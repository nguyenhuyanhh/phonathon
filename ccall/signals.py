# -*- coding: utf-8 -*-
"""Signals for app ccall."""

from __future__ import unicode_literals

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models.user import PhonathonUser


@receiver(m2m_changed, sender=PhonathonUser.groups.through)
def add_staff_status(sender, action, instance, **kwargs):
    """Add staff status to managers and supervisors."""
    if action in ['post_remove', 'post_add']:
        instance.is_staff = instance.groups.filter(
            name__in=['Managers', 'Supervisors']).exists()
        instance.save()
