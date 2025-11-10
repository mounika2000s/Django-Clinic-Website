from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import Appointment
from .forms import AppointmentForm
from django.shortcuts import redirect


class AppointmentList(LoginRequiredMixin, ListView):
    model = Appointment
    context_object_name = 'appointments'
    template_name = 'appointments/appointment_list.html'

    def get_queryset(self):
        user = self.request.user
        
        # If logged-in user is a doctor
        if hasattr(user, 'doctor_profile'):
            return (
                Appointment.objects
                .select_related('patient', 'doctor')
                .filter(doctor=user.doctor_profile.doctor)
                .order_by('date', 'time')
            )

        # Otherwise show patient appointments
        return (
            Appointment.objects
            .select_related('patient', 'doctor')
            .filter(patient__user=user)
            .order_by('date', 'time')
        )


class AppointmentCreate(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/add_appointment.html'
    success_url = reverse_lazy('appointment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        doctor_id = self.request.GET.get('doctor_id')
        from doctors.models import Doctor  # import your Doctor model
        doctor = None
        if doctor_id:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
            except Doctor.DoesNotExist:
                doctor = None
        kwargs['user'] = self.request.user
        kwargs['doctor'] = doctor
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_id = self.request.GET.get('doctor_id')
        from doctors.models import Doctor
        if doctor_id:
            context['doctor'] = Doctor.objects.filter(id=doctor_id).first()
        return context
    
    def form_valid(self, form):
        self.object = form.save()  # appointment saved
        # redirect to razorpay order view
        return HttpResponseRedirect(
        reverse('payment:create_razorpay_order', kwargs={'order_id': self.object.pk}))

class AppointmentEdit(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/edit_appointment.html'
    success_url = reverse_lazy('appointment_list')


class AppointmentDelete(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/del_appointment.html'
    success_url = reverse_lazy('appointment_list')


class AppointmentDetail(LoginRequiredMixin, DetailView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'appointments/appointment_detail.html'
