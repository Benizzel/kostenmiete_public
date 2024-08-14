from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from .models import Siedlung, Objekt


class BulmaTextInput(widgets.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'input'})


class BulmaNumberInput(widgets.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'input'})


class BulmaSelect(widgets.Select):
    """
    To style the wrapper div of the <select> for BulmaSelect,
    we'll create a custom widget that renders both the select element and its wrapper div.
    """
    def __init__(self, *args, **kwargs):
        self.wrapper_attrs = kwargs.pop('wrapper_attrs', {})
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'select'})

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        # List literal ???
        output = [f'<div class="select {self.wrapper_attrs.get("class", "")}">',
                  super().render(name, value, final_attrs, renderer), '</div>']
        return mark_safe(''.join(output))


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


class ObjektForm(forms.ModelForm):
    """
    Generic Objekt Form so that Bulma Styling can be applied.
    """
    class Meta:
        model = Objekt
        fields = '__all__'
        widgets = {
            'internal_oid': BulmaTextInput(),
            'bezeichnung': BulmaTextInput(),
            'bereich': BulmaSelect(),
            'punkte': BulmaSelect(),
            'aktuelle_miete': BulmaNumberInput(attrs={'step': '0.05'}),
            'siedlung': BulmaSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, BulmaSelect):
                field.widget.attrs.update({'class': 'select is-fullwidth'})
            else:
                field.widget.attrs.update({'class': 'input'})
            if field.help_text:
                field.widget.attrs.update({'placeholder': field.help_text})
            if field.required:
                field.error_messages['required'] = f'Das Feld "{field.label}" ist erforderlich.'

        # Update the queryset for the siedlung field to show a meaningful representation
        self.fields['siedlung'].queryset = Siedlung.objects.all()
        self.fields['siedlung'].label_from_instance = lambda obj: f"{obj.internal_id} - {obj.bezeichnung}"

    def clean_aktuelle_miete(self):
        value = self.cleaned_data['aktuelle_miete']
        if value < 0:
            raise forms.ValidationError('Der Mietbetrag muss positiv sein.')
        return value

