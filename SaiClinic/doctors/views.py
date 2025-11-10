from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.
# creating the CURD operations


# Create your views here.
from .models import  Doctor, Department
from django.views.generic import (CreateView, ListView, 
                                  DetailView, UpdateView, DeleteView)

# -----------DOctor CRUD-----------------
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




# -----
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
import random
import string

from .models import Doctor, DoctorProfile



class CreateDoctorAccountView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff  # only staff can create accounts

    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, id=doctor_id)

        # Prevent duplicate
        if DoctorProfile.objects.filter(doctor=doctor).exists():
            messages.warning(request, "Account already exists for this doctor!")
            return redirect("doctor_list")

        # Create username from email
        base_username = doctor.email.split("@")[0]
        username = base_username

        # If username exists, append doctor.id
        if User.objects.filter(username=username).exists():
            username = f"{base_username}{doctor.id}"

        # Generate random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Create user account
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=doctor.first_name,
            last_name=doctor.last_name,
            email=doctor.email,
        )

        # Create doctor profile
        DoctorProfile.objects.create(
            user=user,
            doctor=doctor,
            address="",
            bio="",
            available=True,
            password_plain = password
        )

        messages.success(
            request,
            f"Account created for {doctor.full_name}! Username: {username}, Password: {password}"
        )

        return redirect("doctor_detail", pk=doctor.id)



from appointments.models import Appointment
class AppointmentUpdate(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ['diagnosis', 'status']
    template_name = 'doctor/doctor_appointment_update.html'

    def get_object(self, queryset=None):
        appointment = get_object_or_404(Appointment, pk=self.kwargs['pk'])

        # Restrict — doctor can edit only their appointments
        if hasattr(self.request.user, 'doctor_profile'):
            if appointment.doctor == self.request.user.doctor_profile.doctor:
                return appointment
        
        # No access for patients
        raise PermissionError("Not allowed")

    def get_success_url(self):
        return reverse_lazy('appointment_list')