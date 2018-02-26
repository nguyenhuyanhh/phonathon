# -*- coding: utf-8 -*-
"""Forms for app ccall."""

from __future__ import unicode_literals

from django import forms


class UploadForm(forms.Form):
    """Form to upload a CSV file."""
    MODEL_USER = 'Caller'
    MODEL_FUND = 'Fund'
    MODEL_PROSPECT = 'Prospect'
    MODELS = (
        (MODEL_USER, MODEL_USER),
        (MODEL_FUND, MODEL_FUND),
        (MODEL_PROSPECT, MODEL_PROSPECT),
    )
    model = forms.ChoiceField(label='Data type', choices=MODELS)
    uploaded_file = forms.FileField(
        label='Upload file', allow_empty_file=False)
