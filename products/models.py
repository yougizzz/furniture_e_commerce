
from django.db import models
# from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# User = get_user_model()


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

    def __str__(self):
        return self.name


class ImageProduct(models.Model):
    code = models.CharField(max_length=200, null=False, blank=False, unique=True)
    sku = models.ImageField(upload_to="sku")
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    email = forms.EmailField(label='Email address')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def saveData(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(self.cleaned_data["password1"])
        if commit:
            customer.save()
        return customer


class UserAccount(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'),
                                                      ('Female', 'Female'),
                                                      ('Other', 'Other')])


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'gender')

    def save_data(self, commit=True):
        user_save = super().save(commit=False)
        if commit:
            user_save.save()
        return user_save


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provice = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    number_address = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.number_address, self.street, self.ward, self.district, self.provice}'


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ('number_address', 'street', 'ward', 'district', 'provice')

    def save_data(self, commit=True):
        user_save = super().save(commit=False)
        if commit:
            user_save.save()
        return user_save

#
# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     item = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     created = models.DateTimeField(auto_now_add=True)
#
#     # def __str__(self):
#     #     return f'{self.quantity} of {self.item.name}'
#
#     def get_total(self):
#         total = self.item.price * self.quantity
#         float_total = float("{0:.2f}".format(total))
#         return float_total

#
# class Order(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
#     total = models.PositiveIntegerField(default=0)
#     status = models.CharField(default='waiting', max_length=50, choices=[('waiting', 'waiting'),
#                                                                          ('cancel', 'cancel'),
#                                                                          ('complete', 'complete'), ])
#
#     def __str__(self):
#         return str(self.id)

#
# class OrderItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     item = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     created = models.DateTimeField(auto_now_add=True)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#
#     def get_total(self):
#         total = self.item.price * self.quantity
#         float_total = float("{0:.2f}".format(total))
#         return float_total
#
#     def __str__(self):
#         return self.item.name

