from django.db import models
from datetime import datetime

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Origin(models.Model):
    name = models.CharField(max_length=255)


class Unit(models.Model):
    name = models.CharField(max_length=255)


class Supplier(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)


