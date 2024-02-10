from django.contrib import admin
from .models import Student, Country
from app.internal.admin.admin_user import AdminUserAdmin

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
    list_display = ["first_name", "last_name", "email", "english_level"]
    filter_vertical = ["countries_to_go"]
    list_per_page = 10

    
    

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

admin.site.site_title = "Study English abroad"
admin.site.site_header = "Study English abroad"
