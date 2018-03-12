# -*- coding: utf-8 -*-
"""Forms for app ccall."""

from __future__ import unicode_literals

from django import forms

from .models import Pool


class UploadForm(forms.Form):
    """Form to handle Caller/Fund/Prospect/Pledge CSV data uploads."""
    MODEL_USER = 'Caller'
    MODEL_FUND = 'Fund'
    MODEL_PROSPECT = 'Prospect'
    MODEL_PLEDGE = 'Pledge'
    MODELS = (
        (MODEL_USER, MODEL_USER),
        (MODEL_FUND, MODEL_FUND),
        (MODEL_PROSPECT, MODEL_PROSPECT),
        (MODEL_PLEDGE, MODEL_PLEDGE),
    )
    model = forms.ChoiceField(label='Data type', choices=MODELS)
    uploaded_file = forms.FileField(
        label='Upload file', allow_empty_file=False)


class UploadPoolForm(forms.ModelForm):
    """Form to handle Pool CSV data uploads."""

    uploaded_file = forms.FileField(
        label='Upload file', allow_empty_file=False)

    class Meta:
        model = Pool
        exclude = ('prospects', 'max_attempts',)
