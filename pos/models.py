from django.db import models
from inventory.models import Product
from consumer.models import Device, COA
# Create your models here.

ORDER_STATUS = (
	('PENDING', 'PENDING'),
	('COMPLETED', 'COMPLETED'),
	('CANCELLED', 'CANCELLED')
)

INVOICE_STATUS = (
	('UNPAID', 'UNPAID'),
	('PAID', 'PAID'),
	('CARRY_FORWARD', 'CARRY_FORWARD')
)

class Order(models.Model):
    created_time = models.DateTimeField(auto_now=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    processed_time = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    order_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.pk)


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unite_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    dicount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.pk)


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_time = models.DateTimeField()
    processed_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='UNPAID')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.pk)


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unite_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.pk)


class Transsection(models.Model):
    dabite_account = models.ForeignKey(COA, related_name='dabite_account')
    credite_account = models.ForeignKey(COA, related_name='credite_account')
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class SalesReturn(models.Model):
    created_time = models.DateTimeField(auto_now=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    processed_time = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    order_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.pk)


class ReturnLine(models.Model):
    sales_return = models.ForeignKey(SalesReturn, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unite_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    dicount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.pk)

