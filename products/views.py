from django import template
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import RegisterForm, UserAddress, UserProfile, UserAddressForm, UserProfileForm, UserAccount, \
    Product, Categories, Brand, BrandForm, Country, CountryForm, CategoriesForm, Material, MaterialForm, \
    ProductForm
from order.models import Order, OrderItem, Cart
from django.http import JsonResponse
from django.core import serializers

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
                return redirect('/manager')
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
    waiting_orders = Order.objects.filter(status='waiting')
    return render(request, 'manager/manage_order.html', {'waiting_orders': waiting_orders})


def show_order_detail(request, id):
    data = OrderItem.objects.filter(order_id=id)
    return render(request, 'manager/order_popup.html', {'order_detail': data})


def manage_brand(request):
    brand = Brand.objects.filter(active=True)
    page = request.GET.get('page')
    paging = Paginator(brand, 10)
    list_brand = paging.get_page(page)
    return render(request, 'manager/manage_brand.html', {'brand': list_brand})


def show_brand(request, id):
    brand = get_object_or_404(Brand, pk=id)
    brand_form = BrandForm(instance=brand)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            brand.code = form['code'].value()
            brand.name = form['name'].value()
            brand.save()
    return render(request, 'manager/brand.html', {'brand_form': brand_form, 'id': id, 'result': None})


def modify_brand(request, id):
    brand = get_object_or_404(Brand, pk=id)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            brand.code = form['code'].value()
            brand.name = form['name'].value()
            brand.save()
            return render(request, 'manager/brand.html', {'brand_form': form, 'id': id, 'result': 'OK'})
    return redirect('/brand')


def create_brand(request):
    brand_form = BrandForm()
    return render(request, 'manager/brand.html', {'brand_form': brand_form, 'result': None})


def execute_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        error = form.errors
        if form.is_valid():
            result = form.save()
            return render(request, 'manager/brand.html', {'brand_form': form, 'id': id, 'result': 'OK'})
        return render(request, 'manager/brand.html', {'brand_form': form, 'id': id, 'result': None, 'error': error})
    return redirect('create-brand')


def manage_country(request):
    countries = Country.objects.filter(active=True)
    page = request.GET.get('page')
    paging = Paginator(countries, 10)
    list_countries = paging.get_page(page)
    return render(request, 'manager/manage_country.html', {'countries': list_countries})


def show_country(request, id):
    countries = get_object_or_404(Country, pk=id)
    country_form = CountryForm(instance=countries)
    return render(request, 'manager/country.html', {'country_form': country_form, 'id': id, 'result': None})


def modify_country(request, id):
    countries = get_object_or_404(Country, pk=id)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=countries)
        if form.is_valid():
            countries.code = form['code'].value()
            countries.name = form['name'].value()
            countries.save()
            return render(request, 'manager/country.html', {'country_form': form, 'id': id, 'result': 'OK'})
    return redirect('/country')


def create_country(request):
    country_form = CountryForm()
    return render(request, 'manager/country.html', {'country_form': country_form, 'result': None})


def execute_country(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        error = form.errors
        if form.is_valid():
            result = form.save()
            return render(request, 'manager/country.html', {'country_form': form, 'id': id, 'result': 'OK'})
        return render(request, 'manager/country.html', {'country_form': form, 'id': id, 'result': None, 'error': error})
    return redirect('create-country')


def manage_category(request):
    categories = Categories.objects.filter(active=True)
    page = request.GET.get('page')
    paging = Paginator(categories, 10)
    list_categories = paging.get_page(page)
    return render(request, 'manager/manage_categories.html', {'categories': list_categories})


def show_category(request, id):
    categories = get_object_or_404(Categories, pk=id)
    categories_form = CategoriesForm(instance=categories)
    return render(request, 'manager/categories.html', {'categories_form': categories_form, 'id': id, 'result': None})


def modify_category(request, id):
    categories = get_object_or_404(Categories, pk=id)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=categories)
        if form.is_valid():
            categories.code = form['code'].value()
            categories.name = form['name'].value()
            categories.save()
            return render(request, 'manager/categories.html', {'categories_form': form, 'id': id, 'result': 'OK'})
    return redirect('/categories')


def create_category(request):
    categories_form = CategoriesForm()
    return render(request, 'manager/categories.html', {'categories_form': categories_form, 'result': None})


def execute_category(request):
    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        error = form.errors
        if form.is_valid():
            result = form.save()
            return render(request, 'manager/categories.html', {'categories_form': form, 'id': id, 'result': 'OK'})
        return render(request, 'manager/categories.html', {'categories_form': form, 'id': id, 'result': None, 'error': error})
    return redirect('create-categories')


def manage_material(request):
    material = Material.objects.filter(active=True)
    page = request.GET.get('page')
    paging = Paginator(material, 10)
    list_countries = paging.get_page(page)
    return render(request, 'manager/manage_material.html', {'material': list_countries})


def show_material(request, id):
    material = get_object_or_404(Material, pk=id)
    material_form = MaterialForm(instance=material)
    return render(request, 'manager/material.html', {'material_form': material_form, 'id': id, 'result': None})


def modify_material(request, id):
    material = get_object_or_404(Material, pk=id)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            material.code = form['code'].value()
            material.name = form['name'].value()
            material.save()
            return render(request, 'manager/material.html', {'material_form': form, 'id': id, 'result': 'OK'})
    return redirect('/material')


def create_material(request):
    material_form = MaterialForm()
    return render(request, 'manager/material.html', {'material_form': material_form, 'result': None})


def execute_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        error = form.errors
        if form.is_valid():
            result = form.save()
            return render(request, 'manager/material.html', {'material_form': form, 'id': id, 'result': 'OK'})
        return render(request, 'manager/material.html', {'material_form': form, 'id': id, 'result': None, 'error': error})
    return redirect('create-material')


def manage_product(request):
    product = Product.objects.filter(active=True)
    page = request.GET.get('page')
    paging = Paginator(product, 5)
    list_product = paging.get_page(page)
    return render(request, 'manager/manage_product.html', {'product': list_product})


def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product_form = ProductForm(instance=product)
    return render(request, 'manager/product.html', {'product_form': product_form, 'id': id, 'result': None})


def modify_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            product.name = form['name'].value()
            product.price = form['price'].value()
            product.quantity = form['quantity'].value()
            product.color_id = form['color'].value()
            product.material_id = form['material'].value()
            product.categories_id = form['categories'].value()
            product.detail = form['detail'].value()
            product.country_id = form['country'].value()
            product.description = form['description'].value()
            product.mainImage = form['mainImage'].value()
            product.save()
            return render(request, 'manager/product.html', {'product_form': form, 'id': id, 'result': 'OK'})
    return redirect('/product')


def create_product(request):
    product_form = ProductForm()
    return render(request, 'manager/product.html', {'product_form': product_form, 'result': None})


def execute_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        error = form.errors
        if form.is_valid():
            result = form.save()
            return render(request, 'manager/product.html', {'product_form': form, 'id': id, 'result': 'OK'})
        return render(request, 'manager/product.html', {'product_form': form, 'id': id, 'result': None, 'error': error})
    return redirect('create-product')


def delete_brand(request, id):
    brand = get_object_or_404(Brand, pk=id)
    brand.active = False
    brand.save()
    return redirect('manage-brand')


def delete_material(request, id):
    material = get_object_or_404(Material, pk=id)
    material.active = False
    material.save()
    return redirect('manage-material')


def delete_country(request, id):
    country = get_object_or_404(Country, pk=id)
    country.active = False
    country.save()
    return redirect('manage-country')


def delete_categories(request, id):
    categories = get_object_or_404(Categories, pk=id)
    categories.active = False
    categories.save()
    return redirect('manage-categories')

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.active = False
    product.save()
    return redirect('manage-product')
