from django.contrib import admin

# Register your models here.
from .models import Doctor, Department


admin.site.register(Department)

admin.site.register(Doctor)