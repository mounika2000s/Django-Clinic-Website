from django.db import models

from django.contrib.auth.models import User

class Patient(models.Model):
    image = models.ImageField(upload_to='patients/images/', null=True, blank=True)
    RELATION_CHOICES = [
        ('self', 'Self'),
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('other', 'Other'),
    ]
    
    dob = models.DateField()
    name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ]
    )
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    relation_type = models.CharField(max_length=20, choices=RELATION_CHOICES, default='self')

    class Meta:
        constraints = [
            # Only one 'self' per user
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(relation_type='self'),
                name='unique_self_per_user'
            ),
            # Only one 'father' per user
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(relation_type='father'),
                name='unique_father_per_user'
            ),
            # Only one 'mother' per user
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(relation_type='mother'),
                name='unique_mother_per_user'
            ),
            # Only one 'spouse' per user
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(relation_type='spouse'),
                name='unique_spouse_per_user'
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.relation_type})"
