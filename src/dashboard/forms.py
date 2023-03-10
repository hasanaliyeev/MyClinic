from django import forms

from doctors.models import Doctor, GENDER_SELECT, Education, Experience, Schedule, Speciality


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'middle_name', 'speciality', 'birth_date', 'phone',
                  'email', 'city', 'address', 'image', 'bio', 'skill', 'gender', 'is_active', 'state')
        widgets = {
            'speciality': forms.Select({'class': 'form-control js-example-basic-multiple'}),
            'first_name': forms.TextInput({'class': 'form-control'}),
            'last_name': forms.TextInput({'class': 'form-control'}),
            'middle_name': forms.TextInput({'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'skill': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.RadioSelect(attrs={'name': 'rating', 'class': 'form-check-input'}, choices=GENDER_SELECT),
            'is_active': forms.CheckboxInput(attrs={'class': ''})
        }


class DoctorEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('institution', 'faculty', 'starting_date', 'complete_date', 'grade')

        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control'}),
            'starting_date': forms.DateInput(attrs={'class': 'form-control'}),
            'complete_date': forms.DateInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DoctorExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ('company_name', 'job_position', 'address', 'period_from', 'period_to')

        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_position': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'period_from': forms.DateInput(attrs={'class': 'form-control'}),
            'period_to': forms.DateInput(attrs={'class': 'form-control'}),
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('start_from', 'finish_by', 'price')
        widgets = {
            'start_from': forms.TimeInput(attrs={'class': 'form-control'}),
            'finish_by': forms.TimeInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
