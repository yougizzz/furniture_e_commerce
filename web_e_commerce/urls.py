from django.contrib import admin
from django.urls import path, include
from products.views import home, register, sigin, sigout, add_to_cart, remove_from_cart, \
    ShoppingCart, product_modal, product_detail, confirm_order, my_info, update_info, \
    update_address, delete_address, check_out, select_address, order_detail, filter_catalog, \
    filter_brand, search_product, cancel_order, manager_page, show_order_detail, manage_brand, \
    show_brand, modify_brand, create_brand, execute_brand, manage_country, modify_country, \
    create_country, execute_country, show_country, manage_category, modify_category, create_category, \
    show_category, execute_category, manage_material, show_material, modify_material, create_material, \
    execute_material, manage_product, show_product, create_product, modify_product, execute_product, \
    delete_brand, delete_categories, delete_country, delete_material, delete_product
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
                  path('order-info/<id>', show_order_detail, name='show-order-info'),
                  path('brand/', manage_brand, name='manage-brand'),
                  path('brand/<id>', show_brand, name='modify-brand'),
                  path('brand-modify/<id>', modify_brand, name='submit-brand'),
                  path('brand-create/', create_brand, name='create-brand'),
                  path('brand-save/', execute_brand, name='execute-brand'),
                  path('country/', manage_country, name='manage-country'),
                  path('country/<id>', show_country, name='modify-country'),
                  path('country-modify/<id>', modify_country, name='submit-country'),
                  path('country-create/', create_country, name='create-country'),
                  path('country-save', execute_country, name='execute-country'),
                  path('categories/', manage_category, name='manage-categories'),
                  path('categories/<id>', show_category, name='modify-categories'),
                  path('categories-modify/<id>', modify_category, name='submit-categories'),
                  path('categories-create/', create_category, name='create-categories'),
                  path('categories-save', execute_category, name='execute-categories'),
                  path('material/', manage_material, name='manage-material'),
                  path('material/<id>', show_material, name='modify-material'),
                  path('material-modify/<id>', modify_material, name='submit-material'),
                  path('material-create/', create_material, name='create-material'),
                  path('material-save', execute_material, name='execute-material'),
                  path('product/', manage_product, name='manage-product'),
                  path('product-detail/<id>', show_product, name='modify-product'),
                  path('product-modify/<id>', modify_product, name='submit-product'),
                  path('product-create/', create_product, name='create-product'),
                  path('product-save', execute_product, name='execute-product'),
                  path('brand-delete/<id>', delete_brand, name='delete-brand'),
                  path('country-delete/<id>', delete_country, name='delete-country'),
                  path('material-delete/<id>', delete_material, name='delete-material'),
                  path('categories-delete/<id>', delete_categories, name='delete-categories'),
                  path('product-delete/<id>', delete_product, name='delete-product'),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
