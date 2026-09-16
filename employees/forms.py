import re

from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    field_style = {
        'class': 'form-control',
    }

    class Meta:
        model = Employee
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'department',
            'position',
            'date_hired',
            'salary',
            'emergency_contact',
            'emergency_phone',
            'notes',
            'profile_photo',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Maya'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Chen'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@company.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09XX XXX XXXX or +63 9XX XXX XXXX'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Product'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Product Designer'}),
            'date_hired': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Alex Chen'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional notes', 'rows': 4}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        normalized = re.sub(r'[\s().-]', '', phone)
        if normalized.startswith('09') and len(normalized) == 11:
            normalized = '+63' + normalized[1:]
        if not re.fullmatch(r'\+639\d{9}', normalized):
            raise forms.ValidationError('Enter a valid Philippine mobile number, such as 0917 123 4567.')
        return normalized