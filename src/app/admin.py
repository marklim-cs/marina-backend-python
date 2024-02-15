from django.contrib import admin
from .models import Student
from app.internal.admin.admin_user import AdminUserAdmin

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
    list_display = ["first_name", "phone_number", "email",]
    list_per_page = 10

admin.site.site_title = "English abroad"
admin.site.site_header = "English abroad"
