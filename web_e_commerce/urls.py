from django.contrib import admin
from django.urls import path, include
from products.views import home, register, sigin, sigout, add_to_cart, remove_from_cart, \
    ShoppingCart, product_modal, product_detail, confirm_order, my_info, update_info, \
    update_address, delete_address, check_out, select_address, order_detail, filter_catalog, \
    filter_brand, search_product, cancel_order, manager_page, manager_shipping_order, manager_cancel_order, manager_complete_order, \
    show_order_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', home, name='home'),
                  path('register/', register, name="register"),
                  path('login/', sigin, name='login'),
                  path('logout/', sigout, name='sigout'),
                  path('add_cart/<id>', add_to_cart, name='cart'),
                  path('remove_cart/<id>', remove_from_cart, name='remove_from_cart'),
                  path('cart/', ShoppingCart, name='cart'),
                  path('product-modal/<id>', product_modal, name='product_modal'),
                  path('product/<name>', product_detail, name='product_detail'),
                  path('order/<id_address>', confirm_order, name='order'),
                  path('my-info/<id>', my_info, name='my-info'),
                  path('update-info/', update_info, name='update-info'),
                  path('update-address/', update_address, name='update-address'),
                  path('delete-address/<id>', delete_address, name='delete-address'),
                  path('check-out/<id>', check_out, name='checkout'),
                  path('select-address', select_address, name='select-address'),
                  path('order-detail/<id>', order_detail, name='order-detail'),
                  path('product/catalog/<id>', filter_catalog, name='filter-catalog-product'),
                  path('product/brand/<id_brand>', filter_brand, name='filter-brand-product'),
                  path('search/product', search_product, name='search-product'),
                  path('cancel-order/<id>', cancel_order, name='cancel-order'),
                  path('manager/', manager_page, name='manager-page'),                  
                  path('manager-shipping-order/<id>', manager_shipping_order, name="manager-shipping-order"),
                  path('manager-complete-order/<id>', manager_complete_order, name="manager-complete-order"),
                  path('manager-cancel-order/<id>', manager_cancel_order, name="manager-cancel-order"),
                  path('show-order-detail/<id>', show_order_detail, name="show_order_detail"),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
