from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from wagtail.admin import messages

User = get_user_model()


class Brand(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    code = models.CharField(max_length=200, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    code = models.CharField(max_length=200, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    code = models.CharField(max_length=200, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    code = models.CharField(max_length=200, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    code = models.CharField(max_length=200, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    detail = models.TextField()
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    mainImage = models.ImageField(upload_to='sku')


class ImageProduct(models.Model):
    code = models.CharField(max_length=200, null=False, blank=False, unique=True)
    sku = models.ImageField(upload_to="sku")
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f'{self.quantity} of {self.item.name}'

    def get_total(self):
        total = self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal


class Order(models.Model):
    orderItems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username








