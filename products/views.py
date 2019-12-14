from django import template
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import RegisterForm, UserAddress, UserProfile, UserAddressForm, UserProfileForm, UserAccount, \
    Product, Categories, Brand
from order.models import Order, OrderItem, Cart

register = template.Library()


class Home(ListView):
    model = Product
    template_name = 'home.html'


def home(request):
    # return render(request, 'manager/manage_order.html')
    list_product = Product.objects.all()
    list_product = get_catalog(None)
    page = request.GET.get('page', 1)
    paging = Paginator(list_product, 8)
    catalog = Categories.objects.all()
    brand = Brand.objects.all()
    cart = Cart.objects.all()
    try:
        product = paging.page(page)
    except PageNotAnInteger:
        product = paging.page(1)
    except EmptyPage:
        product = paging.page(paging.num_pages)
    return render(request, 'home.html', {'product': product, 'catalog': catalog, 'cart': cart, 'brand': brand})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.saveData()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            UserAddress.objects.create(user=user)
            UserProfile.objects.create(user=user)
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            redirect('/login')
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
            if user is not None and user.is_staff is False:
                login(request, user)
                return redirect('/')
            elif user and user.is_staff and user.is_superuser is False:
                login(request, user)
                return redirect(request, manager_page)
    form = AuthenticationForm()
    return render(request=request,
                  template_name="login.html",
                  context={"form": form})


def sigout(request):
    logout(request)
    return redirect('/')


@login_required
def my_info(request, id):
    user = request.user
    profile = UserProfile.objects.get(user_id=id)
    address = UserAddress.objects.filter(user_id=id)
    address_form = UserAddressForm()

    profile_form = UserProfileForm()
    profile_form['phone'].initial = profile.phone
    profile_form['gender'].initial = profile.gender

    account = UserAccount()
    account['first_name'].initial = user.first_name
    account['last_name'].initial = user.last_name
    account['email'].initial = user.email

    list_waiting_order_item = []
    waiting_order = Order.objects.filter(status="waiting", user_id=id)
    for i in waiting_order:
        waiting_order_detail = OrderItem.objects.filter(order_id=i.id)
        for j in waiting_order_detail:
            product = Product.objects.get(id=j.item_id)
            myDict = {
                "id": j.id,
                "quantity": j.quantity,
                "created": j.created,
                "item_name": product.name,
                "item_price": product.price,
                "item_image": product.mainImage.url,
                "order_id": j.order_id
            }
            list_waiting_order_item.append(myDict)

    order = Order.objects.filter(user=request.user, ordered=True).order_by('-created')
    return render(request, 'my_info.html', {'profile': profile_form,
                                            'address': address_form,
                                            'account': account,
                                            'my_address': address,
                                            'order': order,
                                            'waiting_order': waiting_order,
                                            'waiting_order_item': list_waiting_order_item
                                            })


def ShoppingCart(request):
    cart = Cart.objects.all()
    total = 0
    for i in cart:
        total += i.get_total()
    return render(request, 'cart.html', {'cart': cart, 'total': total})


@login_required
def add_to_cart(request, id):
    item = get_object_or_404(Product, id=id)
    quantity_product = int(request.POST['qtybutton'])
    cart = Cart.objects.filter(user=request.user, item=item)
    if cart.exists():
        cart.update(user=request.user, item=item, quantity=cart[0].quantity + quantity_product)
        return redirect("/product/" + item.name)
    else:
        cart.create(user=request.user, item=item, quantity=quantity_product)
        return redirect("/product/" + item.name)


@login_required
def remove_from_cart(request, id):
    item = Product.objects.filter(id=id)
    cart_qs = Cart.objects.filter(user_id=request.user, item_id=id)
    if cart_qs.exists():
        cart = cart_qs[0]
        cart.delete()
        return redirect("/cart")
    return redirect("/cart")


def get_catalog(id):
    if id:
        item = Product.objects.filter(categories=id)
        # category = Categories.objects.all()
        # brand = Brand.objects.all()
        return item
    else:
        products = Product.objects.all()
        return products


def get_brand(id):
    if id:
        item = Product.objects.filter(brand=id)
        # category = Categories.objects.all()
        # brand = Brand.objects.all()
        return item
    else:
        products = Product.objects.all()
        return products


def filter_catalog(request, id):
    list_product = get_catalog(id)
    page = request.GET.get('page', 1)
    paging = Paginator(list_product, 8)
    catalog = Categories.objects.all()
    brand = Brand.objects.all()
    cart = Cart.objects.all()
    try:
        product = paging.page(page)
    except PageNotAnInteger:
        product = paging.page(1)
    except EmptyPage:
        product = paging.page(paging.num_pages)
    return render(request, 'home.html', {'product': product, 'catalog': catalog, 'cart': cart, 'brand': brand})


def filter_brand(request, id_brand):
    list_product = get_brand(id_brand)
    page = request.GET.get('page', 1)
    paging = Paginator(list_product, 8)
    catalog = Categories.objects.all()
    brand = Brand.objects.all()
    cart = Cart.objects.all()
    try:
        product = paging.page(page)
    except PageNotAnInteger:
        product = paging.page(1)
    except EmptyPage:
        product = paging.page(paging.num_pages)
    return render(request, 'home.html', {'product': product, 'catalog': catalog, 'cart': cart, 'brand': brand})


def product_modal(request, id):
    item = Product.objects.get(id=id)
    return JsonResponse(data=item)


def product_detail(request, name):
    item = Product.objects.filter(name=name).first()
    related_product = Product.objects.filter(categories_id=item.categories_id)[:4]
    return render(request, 'product_detail.html', {'product': item, 'product_related': related_product})


def confirm_order(request, id_address):
    order = Order.objects.get_or_create(user=request.user, ordered=False, address_id=id_address)
    cart = Cart.objects.all()
    total = 0
    for item in cart:
        total += item.get_total()
        OrderItem.objects.get_or_create(user=request.user, order_id=order[0].id, item=item.item, quantity=item.quantity)
    order_item = OrderItem.objects.filter(user=request.user, order_id=order[0].id).all()
    order[0].total = total
    order[0].save()
    Cart.objects.all().delete()
    return render(request, 'order.html', {'order_item': order_item, 'total': total, 'order_id': order[0].id})


def order_detail(request, id):
    item = OrderItem.objects.filter(order_id=id)
    return render(request, 'order_detail.html', {'order_item': item})


def select_address(request):
    address = UserAddress.objects.filter(user=request.user)
    return render(request, 'address.html', {'address': address})


@login_required
def check_out(request, id):
    order = Order.objects.get(id=id)
    order.ordered = True
    order.save()
    return render(request, 'checkout.html', {'order': order})


@login_required
def update_info(request):
    page = '/my-info/' + str(request.user.id)
    profile = UserProfile.objects.get(user_id=request.user.id)
    account = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form_1 = UserProfileForm(request.POST)
        form_2 = UserAccount(request.POST)
        if form_1.is_valid() and form_2.is_valid():
            account.first_name = form_2['first_name'].value()
            account.last_name = form_2['last_name'].value()
            account.email = form_2['email'].value()
            profile.gender = form_1['gender'].value()
            profile.phone = form_1['phone'].value()
            account.save()
            profile.save()
            return redirect(page)
    return redirect(page)


@login_required
def update_address(request):
    page = '/my-info/' + str(request.user.id)
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            UserAddress.objects.update_or_create(user=request.user,
                                                 provice=form['provice'].value(),
                                                 district=form['district'].value(),
                                                 ward=form['ward'].value(),
                                                 street=form['street'].value(),
                                                 number_address=form['number_address'].value())
            return redirect(page)
    return redirect(page)


@login_required
def delete_address(request, id):
    page = '/my-info/' + str(request.user.id)
    address = UserAddress.objects.get(id=id)
    address.delete()
    return redirect(page)


def search_product(request):
    if request.method == 'GET':
        name = request.GET
        tmp = name.get('search_name')
    list_product = Product.objects.filter(name__icontains=tmp)
    page = request.GET.get('page', 1)
    paging = Paginator(list_product, 8)
    catalog = Categories.objects.all()
    brand = Brand.objects.all()
    cart = Cart.objects.all()
    try:
        product = paging.page(page)
    except PageNotAnInteger:
        product = paging.page(1)
    except EmptyPage:
        product = paging.page(paging.num_pages)
    return render(request, 'home.html', {'product': product, 'catalog': catalog, 'cart': cart, 'brand': brand})


def cancel_order(request, id):
    page = '/my-info/' + str(request.user.id)
    order = Order.objects.get(id=id)
    order.status = "cancel"
    order.save()
    return redirect(page)

@login_required
def manager_page(request):
    return render(request, 'manager/manage_order.html')
