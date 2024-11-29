from django.forms import forms
from .models import Customfields


class CustomFieldCreation(forms.Form):
    class Meta:
        model = Customfields()
        fields = ('field_name', 'field_type', 'is_required')