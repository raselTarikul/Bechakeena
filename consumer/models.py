from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class COA(models.Model):
    account_no = models.CharField(max_length=10)


class SalesRepresentative(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Zone(models.Model):
    name = models.CharField(max_length=255)
    sales_representative = models.ForeignKey(SalesRepresentative)
    description = models.TextField()


class Device(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coa = models.ForeignKey(COA)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=255, null=True, blank=True, default=None)
    shop_name = models.CharField(max_length=255, default=None, null=True)
    address = models.TextField(default=None, null=True)
    install_date = models.DateTimeField(auto_now=True)
    sr_no = models.CharField(max_length=255, default=None, null=True)
    pin = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username


class AdminUser(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

