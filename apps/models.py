from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from datetime import datetime

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


class Device(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	shop_name = models.CharField(max_length=255, default=None, null=True)
	address = models.TextField(default=None, null=True)
	install_date = models.DateTimeField(auto_now=True)
	sr_no = models.CharField(max_length=255, default=None, null=True)
	pin = models.CharField(max_length=255, null=True)

	def __str__(self):
		return self.user.username


class Category(models.Model):
	parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
	name = models.CharField(max_length=100)
	status = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	image = models.ImageField(null=True, blank=True)
	regular_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	in_stock = models.BooleanField(default=True)
	unite = models.CharField(max_length=100, default='KG')
	updated_time = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		self.updated_time = datetime.now()
		super(Product, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Order(models.Model):
	created_time = models.DateTimeField(auto_now=True)
	device = models.ForeignKey(Device, on_delete=models.CASCADE)
	processed_time = models.DateTimeField(null=True, blank=True)
	processed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
	order_total = models.DecimalField(max_digits=10, decimal_places=2)

	@property
	def action_button_disable(self):
		if self.status == 'PENDING':
			return False
		else:
			return True

	def __str__(self):
		return self.pk


class OrderLine(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.DecimalField(max_digits=10, decimal_places=2)
	unite_price = models.DecimalField(max_digits=10, decimal_places=2)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	dicount = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.pk


class Invoice(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	created_time = models.DateTimeField()
	processed_time = models.DateTimeField(null=True, blank=True)
	status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='UNPAID')
	total = models.DecimalField(max_digits=10, decimal_places=2)
	discount = models.DecimalField(max_digits=10, decimal_places=2)
	total_payable = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.pk


class InvoiceLine(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.DecimalField(max_digits=10, decimal_places=2)
	unite_price = models.DecimalField(max_digits=10, decimal_places=2)
	amount = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.pk


