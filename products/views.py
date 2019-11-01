from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import Product, Cart, Order, Categories
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import template


class Home(ListView):
    model = Product
    template_name = 'home.html'


def home(request):
    list_product = Product.objects.all()
    page = request.GET.get('page', 1)
    paging = Paginator(list_product, 8)
    catalog = Categories.objects.all()
    cart = Cart.objects.all()
    try:
        product = paging.page(page)
    except PageNotAnInteger:
        product = paging.page(1)
    except EmptyPage:
        product = paging.page(paging.num_pages)
    return render(request, 'home.html', {'product': product, 'catalog': catalog, 'cart': cart})


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
                messages.info(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="login.html",
                  context={"form": form})


def sigout(request):
    logout(request)
    return redirect('/')


def ShoppingCart(request):
    cart = Cart.objects.all()
    total = 0
    for i in cart:
        total += i.get_total()
    return render(request, 'cart.html', {'cart': cart, 'total': total})


@login_required
def add_to_cart(request, id):
    item = get_object_or_404(Product, id=id)
    quantity = int(request.POST['qtybutton'])
    order_item = Cart.objects.get_or_create(
        item=item,
        user=request.user,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderItems.filter(item_id=item.id).exists():
            order_item[0].quantity += quantity
            order_item[0].save()
            return redirect("/product/" + item.name)
        else:
            order_item[0].quantity = quantity
            order_item[0].save()
            order.orderItems.add(order_item[0])
            return redirect("/product/" + item.name)
    else:
        order = Order.objects.create(
            user=request.user)
        order.orderItems.add(order_item)
        return redirect("/")


@login_required
def remove_from_cart(request, id):
    item = Product.objects.filter(id=id)
    cart_qs = Cart.objects.filter(user_id=request.user, item_id=id)
    if cart_qs.exists():
        cart = cart_qs[0]
        # Checking the cart quantity
        cart.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderItems.filter(item_id=id).exists():
            order.delete()
            # order_item = Cart.objects.filter(
            #     item=item,
            #     user=request.user,
            # )
            # order.orderItems.remove(order_item)
            # messages.info(request, "This item was removed from your cart.")
            return redirect("/cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("/cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("/cart")


def catalog(request, id):
    item = Product.objects.filter(categories=id)
    catagory = Categories.objects.all()
    return render(request, 'home.html', {'product': item, 'catalog': catagory})



def product_modal(request, id):
    item = Product.objects.filter(id=id).first()
    print(item)
    # return render(request, 'product_modal.html', {'product_detail': item})
    return HttpResponse(product_modals=item)


def product_detail(request, name):
    item = Product.objects.filter(name=name).first()
    return render(request, 'product_detail.html', {'product': item})


def confirm_order(request):
    order_item = Order.objects.filter(user=request.user, ordered=False)
    cart_item = Cart.objects.all()
    total = 0
    for i in cart_item:
        total += i.get_total()
    if order_item.exists():
        order_item[0].ordered = True
        order_item[0].save()
        return render(request, 'order.html', {'order_item': cart_item, 'total': total})
    else:
        return redirect('/cart')
