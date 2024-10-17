from django.urls import path
from . import views

urlpatterns=[
    path('login',views.login_view,name="login_view"),
    path('registration',views.registration,name='registration'),
    path('forgot_password',views.forgot_password,name="forgot_password"),
    path('login',views.login_view,name='login'),
    path('my_logout_view',views.my_logout_view,name='my_logout_view')
]