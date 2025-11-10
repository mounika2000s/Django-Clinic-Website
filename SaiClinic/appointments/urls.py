from django.urls import path
from . import views

urlpatterns = [
    path('', views.AppointmentList.as_view(), name='appointment_list'),
    path('add/', views.AppointmentCreate.as_view(), name='add_appointment'),
    path('<int:pk>/edit/', views.AppointmentEdit.as_view(), name='edit_appointment'),
    path('<int:pk>/delete/', views.AppointmentDelete.as_view(), name='delete_appointment'),
    path('<int:pk>/', views.AppointmentDetail.as_view(), name='appointment_detail'),
]
