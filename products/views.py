from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import Product, Cart, Order
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class Home(ListView):
    model = Product
    template_name = 'home.html'


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    email = forms.EmailField(label='Email address')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    phone = forms.CharField(label='Phone number')

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def saveData(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(self.cleaned_data["password1"])
        if commit:
            customer.save()
        return customer


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.saveData()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            print('register success')
            # login(request, user)
            # return redirect('/register')
        else:
            print('register fail')
    else:
        # fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def sigin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="login.html",
                  context={"form": form})


def sigout(request):
    logout(request)
    return redirect('/')


@login_required
def add_to_cart(request, id):
    item = get_object_or_404(Product, id=id)
    cart = request.session['cart']
    if cart is not None and item is not None:
        for i in cart:
            if i.id == id:
                i.quantity += 1
    else:
        request.session['cart'] = item




