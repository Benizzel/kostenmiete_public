from django import forms
from .models import Objekt


class ObjektCreateForm(forms.ModelForm):
    class Meta:
        model = Objekt
        exclude = ['siedlung']


