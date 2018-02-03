# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-03 02:51
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhonathonUser',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(
                    max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(
                    blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=15, unique=True)),
                ('first_name', models.CharField(blank=True,
                                                max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True,
                                               max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True,
                                            max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(
                    default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateField(
                    default=django.utils.timezone.localdate, verbose_name='Date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                                            related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('name', models.CharField(max_length=50, verbose_name='Full name')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50,
                                          unique=True, verbose_name='Fund name')),
            ],
        ),
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('pledge_amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[
                 django.core.validators.MinValueValidator(0)], verbose_name='Pledge amount')),
                ('pledge_date', models.DateField(verbose_name='Pledge date')),
            ],
        ),
        migrations.CreateModel(
            name='Prospect',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('nric', models.CharField(max_length=15,
                                          unique=True, verbose_name='NRIC')),
                ('salutation', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True,
                                            max_length=254, verbose_name='Email address')),
                ('address_1', models.CharField(blank=True,
                                               max_length=50, verbose_name='Address (line 1)')),
                ('address_2', models.CharField(blank=True,
                                               max_length=50, verbose_name='Address (line 2)')),
                ('address_3', models.CharField(blank=True,
                                               max_length=50, verbose_name='Address (line 3)')),
                ('address_postal', models.CharField(
                    blank=True, max_length=6, verbose_name='Postal code')),
                ('phone_home', models.CharField(blank=True,
                                                max_length=8, verbose_name='Home phone')),
                ('phone_mobile', models.CharField(blank=True,
                                                  max_length=8, verbose_name='Mobile phone')),
                ('education_school', models.CharField(
                    max_length=50, verbose_name='School graduated from')),
                ('education_degree', models.CharField(
                    max_length=50, verbose_name='Degree')),
                ('education_year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(
                    1950), django.core.validators.MaxValueValidator(2018)], verbose_name='Year of graduation')),
            ],
        ),
        migrations.AddField(
            model_name='pledge',
            name='prospect',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='ccall.Prospect'),
        ),
        migrations.AddField(
            model_name='pledge',
            name='pledge_fund',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='ccall.Fund'),
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Pool name')),
                ('max_attempts', models.PositiveSmallIntegerField(
                    verbose_name='Maximum number of attempts')),
                ('prospects', models.ManyToManyField(blank=True, related_name='prospect_set',
                                                     related_query_name='prospects', to='ccall.Prospect', verbose_name='Prospects')),
            ],
        ),
        migrations.CreateModel(
            name='ResultCode',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('result_code', models.CharField(max_length=25,
                                                 unique=True, verbose_name='Result code')),
                ('is_complete', models.BooleanField(
                    default=True, verbose_name='Complete status')),
            ],
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('call_time', models.DateTimeField(
                    auto_now=True, verbose_name='Time')),
                ('comment', models.TextField(blank=True, verbose_name='Comments')),
                ('pledge_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, validators=[
                 django.core.validators.MinValueValidator(0)], verbose_name='Pledge amount')),
                ('pledge_method', models.CharField(blank=True, choices=[('Check', 'Check'), (
                    'Credit', 'Credit'), ('EFT', 'EFT')], max_length=10, verbose_name='Pledge method')),
                ('pledge_meta', models.TextField(
                    blank=True, verbose_name='Pledge metadata')),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             to=settings.AUTH_USER_MODEL, verbose_name='Caller')),
                ('pool', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='ccall.Pool', verbose_name='Pool')),
                ('prospect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                               to='ccall.Prospect', verbose_name='Prospect')),
                ('result_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                  to='ccall.ResultCode', verbose_name='Result code')),
            ],
        ),
    ]
