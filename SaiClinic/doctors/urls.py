from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddDoctor.as_view(), name='add_doctor'),
    path('', views.ViewDoctors.as_view(), name='view_doctor'),
    path('<int:pk>/', views.DoctorDetail.as_view(), name='doctor_detail'),
    path('del/<int:pk>/', views.DoctorDelete.as_view(), name = 'del_doctor'),
   path('edit/<int:pk>/', views.DoctorEdit.as_view(), name='edit_doctor'),


   path("<int:doctor_id>/create-account/",views.CreateDoctorAccountView.as_view(),name="create_doctor_account"),
   path('update/<int:pk>/', views.AppointmentUpdate.as_view(), name='doctor_appointment_update'),

]
