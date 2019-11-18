from django.db import models
from django.contrib.auth.models import User
from products.models import Product, UserAddress


class Paypal(models.Model):
    id = id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f'{self.quantity} of {self.item.name}'

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = float("{0:.2f}".format(total))
        return float_total


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)
    status = models.CharField(default='waiting', max_length=50, choices=[('waiting', 'waiting'),
                                                                         ('cancel', 'cancel'),
                                                                         ('complete', 'complete'), ])

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = float("{0:.2f}".format(total))
        return float_total

    def __str__(self):
        return self.item.name

