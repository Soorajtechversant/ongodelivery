from re import template
from django.urls import path, include
from deliveryapp.views import *
from .views import *
from deliveryapp import views


urlpatterns = [
    path('',Customer_index.as_view(),name="products/customer/customer_index" ),
    path('registration',Registration.as_view(),name="products/registration/registration"),
    path('auth/login/',Login.as_view(),name="products/registration/login"),
    path('logout/',Logout.as_view(),name="logout"),
    path('auth/settings', views.settings, name='settings'),


    path('owner_index/',Owner_index.as_view(),name="products/productshop_owner/owner_index"),
    path('add_product/',Add_product.as_view(),name="products/productshop_owner/add_product"),
    path('edit_product/<int:id>/',Edit_product.as_view(),name="products/productshop_owner/edit_product"),
    path('Delete_product/<int:id>',Delete_product.as_view(),name="products/productshop_owner/Delete_product"),
   
    path('customer_index/',Customer_index.as_view(),name="products/customer/customer_index"),
    
    


]