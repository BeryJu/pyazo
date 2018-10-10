"""pyazo upload management forms"""

from django import forms
from django.db.models import QuerySet


class CollectionSelectForm(forms.Form):
    """Assign Upload to collection"""

    collection = forms.ModelChoiceField(queryset=QuerySet().none(), required=False)
