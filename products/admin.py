from django.contrib import admin
from .models import Product, Material, Country, Color, Categories, Brand, ImageProduct, Order, Cart


class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name',)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_per_page = 10
    search_fields = ('name', 'code')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_per_page = 10
    search_fields = ('name', 'code')


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    list_per_page = 10


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    list_per_page = 10


class ColorAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('name', 'code')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user', )
    list_per_page = 10

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')
    list_per_page = 10

class ProductAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('name', 'price', 'quantity')
    search_fields = ('name',)




admin.site.register(ImageProduct, ImageAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Color, CountryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Product, ProductAdmin)
