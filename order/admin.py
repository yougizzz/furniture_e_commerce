from django.contrib import admin
# from products.models import Order, OrderItem, Cart
from .models import Paypal, Order, OrderItem, Cart


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'quantity', 'order')
    list_per_page = 20
    search_fields = ['id', 'item', 'quantity', 'order']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'total', 'ordered', 'status')
    list_filter = ('user', 'status')
    list_per_page = 20


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')
    list_per_page = 20


class PaypalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created')

admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Paypal, PaypalAdmin)
