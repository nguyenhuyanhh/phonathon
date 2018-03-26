# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-26 07:45
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccall', '0004_call_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='pledge_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Pledge amount'),
        ),
    ]