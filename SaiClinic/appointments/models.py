from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient
from doctors.models import Doctor  


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    diagnosis = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Prevent double-booking (same doctor, date, and time)
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time'],
                name='unique_doctor_appointment'
            ),
        ]
        ordering = ['-date', '-time']

    def __str__(self):
        return f"Appointment: {self.patient.name} with Dr. {self.doctor.full_name} on {self.date} at {self.time}"
    
    @property
    def total_amount(self):
        return self.doctor.rate 