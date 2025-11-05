from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.
# creating the CURD operations


# Create your views here.
from .models import  Doctor, Department
from django.views.generic import (CreateView, ListView, 
                                  DetailView, UpdateView, DeleteView)

# -----------Product CRUD-----------------
class AddDoctor(CreateView):
    model = Doctor
    fields = '__all__'
    template_name = 'doctor/add_doctor.html'
    success_url = reverse_lazy("view_doctor")

class ViewDoctors(ListView):
    model = Doctor
    context_object_name = 'doctors'
    template_name = 'doctor/doctors.html'

class DoctorDetail(DetailView):
    model = Doctor
    context_object_name = 'doctor'
    template_name = 'doctor/doctor_details.html'

# this is the update and delete

class DoctorDelete(DeleteView):
    model = Doctor
    context_object_name = 'doctor'
    template_name = 'doctor/del_doctor.html'
    success_url = reverse_lazy('view_doctor')
    

class DoctorEdit(UpdateView):
    model = Doctor
    fields ='__all__'
    context_object_name = 'doctor'
    template_name = 'doctor/edit_doctor.html'
    success_url = reverse_lazy('view_doctor')