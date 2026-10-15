from django import forms

from .models import Property, SelectionRequest


class SelectionRequestForm(forms.ModelForm):
    class Meta:
        model = SelectionRequest
        fields = (
            'name',
            'phone',
            'email',
            'deal_type',
            'property_type',
            'city',
            'budget_min',
            'budget_max',
            'rooms',
            'comment',
        )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Как к вам обращаться'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 …'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город или регион'}),
            'budget_min': forms.NumberInput(attrs={'placeholder': 'От', 'min': 0, 'step': 100000}),
            'budget_max': forms.NumberInput(attrs={'placeholder': 'До', 'min': 0, 'step': 100000}),
            'rooms': forms.NumberInput(attrs={'placeholder': 'Например, 2', 'min': 0}),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Район, этаж, новостройка/вторичка, срок сделки…',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['property_type'].required = False
        self.fields['property_type'].choices = [('', 'Не важно')] + list(
            Property.PropertyType.choices
        )
        for name, field in self.fields.items():
            css = 'input' if name != 'comment' else 'textarea'
            if isinstance(field.widget, forms.Select):
                css = 'select'
            field.widget.attrs.setdefault('class', css)
