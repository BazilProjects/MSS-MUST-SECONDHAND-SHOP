from django.urls import path
from .views import *
urlpatterns = [
    path("add/", add_products, name="add_products"),
    path('success/', success_page, name='success_page'),  # Ensure this exists

    path("signup/", sign_up, name="signup"),
    path("login/", log_in, name="login"),
    path("logout/", log_out, name="logout"),


    
     path('disclaimer', disclaimer_view, name='disclaimer'),
    path('terms-and-conditions', terms_view, name='terms_and_conditions'),
    path('our-apps/', our_apps_view, name='our_apps'),


    path("", product_list, name="product_list"),
    path("add_product", add_product, name="add_product"),
    path("dashboard", dashboard, name="dashboard"),
    path("products/ajax/<int:page>/", product_list_ajax, name="product_list_ajax"),
    path("products/edit/<int:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", delete_product, name="delete_product"),
]

