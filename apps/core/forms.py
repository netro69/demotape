# Created-by: architect | Date: 2026-09-22
from django import forms
from .models import ContributorSubmission


class ContributorSubmissionForm(forms.Form):
    """Public form for anonymous users to submit link fixes or band updates."""
    band_id = forms.IntegerField(widget=forms.HiddenInput)
    link_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    submission_type = forms.ChoiceField(choices=[
        ('link_fix', 'Link Fix'),
        ('band_update', 'Band Update'),
    ])
    suggested_url = forms.URLField(required=False)
    comment = forms.CharField(widget=forms.Textarea, required=True)
    submitter_name = forms.CharField(required=False, max_length=100)
    submitter_email = forms.EmailField(required=False, max_length=254)
    # Spam protection
    company = forms.CharField(required=False, widget=forms.HiddenInput)
    captcha_answer = forms.IntegerField(required=True)
    captcha_expected = forms.CharField(widget=forms.HiddenInput)
