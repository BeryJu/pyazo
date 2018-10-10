"""pyazo upload management forms"""

from django import forms
from django.db.models import QuerySet


class CollectionAssignForm(forms.Form):
    """Assign Upload to collection"""

    collections = forms.ModelChoiceField(queryset=QuerySet().none())
