# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-11 06:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccall', '0002_auto_20180111_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pledge_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Pledge amount')),
                ('pledge_fund', models.CharField(max_length=50, verbose_name='Pledge fund')),
                ('pledge_date', models.DateField(verbose_name='Pledge date')),
                ('prospect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ccall.Prospect')),
            ],
        ),
    ]
