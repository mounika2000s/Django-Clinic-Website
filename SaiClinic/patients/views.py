from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from .models import Patient
from .forms import PatientForm

# ----------- Patients CRUD -----------------

# CREATE
class AddPatient(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/add_patient.html'
    success_url = reverse_lazy('view_patients')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # pass logged-in user to the form
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# READ (List View)
class ViewPatients(LoginRequiredMixin, ListView):
    model = Patient
    context_object_name = 'patients'
    template_name = 'patients/patient.html'

    # show only logged-in user's patients
    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)


#  READ (Detail View)
class PatientDetail(LoginRequiredMixin, DetailView):
    model = Patient
    context_object_name = 'patient'
    template_name = 'patients/patient_details.html'


#  UPDATE
class PatientEdit(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    context_object_name = 'patient'
    template_name = 'patients/edit_patient.html'
    success_url = reverse_lazy('view_patients')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # pass logged-in user to the form
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


#  DELETE
class PatientDelete(LoginRequiredMixin, DeleteView):
    model = Patient
    context_object_name = 'patient'
    template_name = 'patients/del_patient.html'
    success_url = reverse_lazy('view_patients')






# from django.shortcuts import render
# from django.urls import reverse_lazy

# Create your views here.
# creating the CURD operations
# Create your views here.

# from .models import  Patient
# from django.views.generic import (CreateView, ListView, 
#                                   DetailView, UpdateView, DeleteView)




# -----------Patients CRUD-----------------
# class AddPatient(CreateView):
#     model = Patient
#     fields = '__all__'
#     template_name = 'patients/add_patient.html'
#     success_url = reverse_lazy("view_patients")

# class ViewPatients(ListView):
#     model = Patient
#     context_object_name = 'patients'
#     template_name = 'patients/patient.html'

# class PatientDetail(DetailView):
#     model = Patient
#     context_object_name = 'patients'
#     template_name = 'patients/patient_details.html'

# this is the update and delete

# class PatientDelete(DeleteView):
#     model = Patient
#     context_object_name = 'patient'
#     template_name = 'patient/del_patient.html'
#     success_url = reverse_lazy('view_patient')
    

# class PatientEdit(UpdateView):
#     model = Patient
#     fields ='__all__'
#     context_object_name = 'patient'
#     template_name = 'patient/edit_patient.html'
#     success_url = reverse_lazy('view_patient')