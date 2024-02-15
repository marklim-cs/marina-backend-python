from app.internal.models.admin_user import AdminUser
from django.db import models 


class Student(models.Model):
    LANGUAGE_LEVELS = [
        ("A1", "A1 Beginner"),
        ("A2", "A2 Elementary"),
        ("B1", "B1 Intermediate"),
        ("B2", "B2 Upper-Intermediate"),
        ("C1", "C1 Advanced"),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    external_id = models.IntegerField(null=True, unique=True)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(blank=True)
    english_level = models.CharField("choose your English level", max_length=2, choices=LANGUAGE_LEVELS, blank=True)
    bio = models.TextField("Why do you want to join our language exchange program?", blank=True)


    def __str__(self):
        return f"{self.first_name}"
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"