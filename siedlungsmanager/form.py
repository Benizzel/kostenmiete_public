from django import forms
from django.forms import widgets
from .models import Siedlung, Objekt


class BulmaTextInput(widgets.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'input'})


class BulmaNumberInput(widgets.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'input'})


class SiedlungForm(forms.ModelForm):
    class Meta:
        model = Siedlung
        fields = '__all__'
        widgets = {
            'internal_id': BulmaTextInput(),
            'bezeichnung': BulmaTextInput(),
            'anlagewert': BulmaNumberInput(),
            'versicherungswert': BulmaNumberInput(),
            'baurechtszins': BulmaNumberInput(),
            'betriebsquote_zuschlag': BulmaNumberInput(attrs={'step': '0.01'})
        }

    def __init__(self, *args, **kwargs):
        """
        Updates field data in the widget
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})
            if field.help_text:
                field.widget.attrs.update({'placeholder': field.help_text})

    def clean_betriebsquote_zuschlag(self):
        """
        In Django forms, any method named clean_<fieldname> is automatically treated
        as a custom cleaning/validation method for that specific field.
        This is part of Django's form validation process.
        """
        value = self.cleaned_data['betriebsquote_zuschlag']
        if value is not None:
            if value < 0 or value > 100:
                raise forms.ValidationError('Der Wert muss zwischen 0 und 100 liegen')
        return value


class ObjektCreateForm(forms.ModelForm):
    class Meta:
        model = Objekt
        exclude = ['siedlung']
