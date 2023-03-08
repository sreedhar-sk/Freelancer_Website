from django.urls import path

from .import views

from register import views as views_register

urlpatterns=[
path("home/", views.home,name="home"),
path("register/",views_register.register_request,name="register"),
path("login/",views_register.login_request,name="login"),
path('social/signup/', views_register.signup_redirect, name='signup_redirect'),
]