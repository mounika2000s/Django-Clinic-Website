from django import forms
from datetime import date
from .models import Appointment
from patients.models import Patient  # if Patient is in another app

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # get user and doctor from kwargs
        user = kwargs.pop('user', None)
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)

        # hide doctor field (patient shouldn’t choose)
        self.fields.pop('doctor', None)

        # show only logged-in user’s patients
        if user:
            self.fields['patient'].queryset = Patient.objects.filter(user=user)

        # store doctor for use in save()
        self.doctor = doctor

    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'time']  # doctor excluded from form fields
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': date.today().isoformat()
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'patient': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        doctor = self.doctor
        date_ = cleaned_data.get('date')
        time_ = cleaned_data.get('time')

        if doctor and date_ and time_:
            exists = Appointment.objects.filter(doctor=doctor, date=date_, time=time_)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise forms.ValidationError("This doctor already has an appointment at the selected date and time.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.doctor:
            instance.doctor = self.doctor  # assign doctor from view
        if commit:
            instance.save()
        return instance
