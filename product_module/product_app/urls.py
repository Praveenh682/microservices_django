from django.urls import path
from product_app import views

app_name = 'product_app'

urlpatterns = [
    path('product_master/',views.ProductMasterAPI.as_view(),name='productcreate'),
]