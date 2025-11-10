

from django.urls import path
from .views import AddPatient, ViewPatients, PatientDetail, PatientEdit, PatientDelete

urlpatterns = [
    path('', ViewPatients.as_view(), name='view_patients'),
    path('add/', AddPatient.as_view(), name='add_patient'),
    path('<int:pk>/', PatientDetail.as_view(), name='patient_detail'),
    path('<int:pk>/edit/', PatientEdit.as_view(), name='edit_patient'),
    path('<int:pk>/delete/', PatientDelete.as_view(), name='delete_patient'),
]
