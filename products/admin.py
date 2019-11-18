from django.contrib import admin
from .models import Product, Material, Country, Color, Categories, Brand, \
    ImageProduct, UserAddress, UserProfile

admin.site.site_header = 'Admin Web Furniture'

class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ['name',]


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_per_page = 20
    search_fields = ['name', 'code']


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_per_page = 20
    search_fields = ['name', 'code']


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ['name', 'code']
    list_per_page = 20


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    list_per_page = 20


class ColorAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'code')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'total', 'ordered', 'status')
    list_filter = ('user', )
    list_per_page = 20


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')
    list_per_page = 20


class ProductAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'categories', 'brand', 'material', 'price', 'quantity')
    search_fields = ['name',]


class UserProfileAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('user', 'phone',)


class UserAddressAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('user', 'number_address', 'street', 'ward', 'district', 'provice')
    search_fields = ['number_address', 'street', 'ward', 'district', 'provice',]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'quantity', 'order')
    list_per_page = 20
    search_fields = ['id', 'item', 'quantity', 'order']


admin.site.register(ImageProduct, ImageAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Color, CountryAdmin)
# admin.site.register(Order, OrderAdmin)
# admin.site.register(Cart, CartAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
# admin.site.register(OrderItem, OrderItemAdmin)