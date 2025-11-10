from django import forms
from datetime import date
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',  # optional: only allow image files
            }),
            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'max': date.today().isoformat(),  # prevents future DOBs
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@gmail.com'
            }),
            'relation_type': forms.Select(attrs={'class': 'form-select'}),
        }

    # -----------------------------
    #  Custom initialization
    # -----------------------------
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # receive 'user' from view
        super().__init__(*args, **kwargs)

    # -----------------------------
    #  Custom validation logic
    # -----------------------------
    def clean(self):
        cleaned_data = super().clean()
        relation_type = cleaned_data.get('relation_type')

        if not self.user:
            return cleaned_data

        # Restrict only one unique relation per user for these types
        restricted_types = ['self', 'mother', 'father', 'spouse']

        if relation_type in restricted_types:
            existing = Patient.objects.filter(user=self.user, relation_type=relation_type)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                self.add_error(
                    'relation_type',
                    f"You already have a patient with relation type '{relation_type.title()}'."
                )

        return cleaned_data

    # -----------------------------
    #  Save method with user assignment
    # -----------------------------
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
