from django.urls import path

from . import views
urlpatterns=[
path('',views.home,name="home"),
path('home',views.home,name="home"),
path('home_location',views.home_location,name="home_location"),
path('add_product',views.add_product,name="add_product"),
path('product_details',views.product_details,name='product_details'),
path('product_details_location',views.product_details_location,name='product_details_location'),
path('qr_code_input',views.qr_code_input,name='qr_code_input'),
path('update_product',views.update_product,name='update_product'),
path('update_product_details',views.update_product_details,name='update_product_details'),
path('upload/', views.upload_products, name='upload_products'),
]