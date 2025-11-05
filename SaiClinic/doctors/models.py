from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=200)
    established = models.DateField()
    phno = models.IntegerField()

    def __str__(self):
        return f"Department: {self.name.capitalize()}"


class Doctor(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL,
                                    null=True, blank=True)
    image = models.ImageField(upload_to = 'doctor/images/')
    phno = models.IntegerField()

    @property # using the property decorator to use the method return value like a data field(or property) of the Doctor object
    def full_name(self):
        return f"Dr. {self.first_name.capitalize()} {self.last_name.capitalize()}"
    
    def __str__(self):
        if self.department:
            return f"{self.full_name} | Department : {self.department.name.capitalize()}"
        else:
            return self.full_name
    

    