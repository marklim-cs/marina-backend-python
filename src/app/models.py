from app.internal.models.admin_user import AdminUser
from django.db import models 

class Account(models.Model):
    account_number = models.IntegerField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.account_number}"

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    external_id = models.IntegerField(null=True, unique=True)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(blank=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="client_account")

    def __str__(self):
        return f"{self.external_id}, {self.first_name}"
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    
class Card(models.Model):
    card_number = models.IntegerField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.card_number}"
    


