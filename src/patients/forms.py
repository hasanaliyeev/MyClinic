from django import forms

from patients.models import Patient, GENDER_CHOICES


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'middle_name', 'birth_date', 'gender', 'address', 'city', 'state',
            'phone_number', 'image',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=GENDER_CHOICES),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'rows': '3'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'upload'}),
        }
