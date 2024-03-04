from django.contrib import admin
from .models import Client, Account, Card
from app.internal.admin.admin_user import AdminUserAdmin

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass
    list_display = ["first_name", "phone_number", "email",]
    list_per_page = 10


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass
    list_display = ["account_number", "balance"]

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass
    list_display = ["account", "card_number"]


admin.site.site_title = "Client page"
admin.site.site_header = "Client page"
