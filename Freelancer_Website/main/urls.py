from django.urls import path

from .import views

from register import views as views_register
from userprofile import views as view_profile

urlpatterns=[
path("home/", views.home,name="home"),
path("register/",views_register.register_request,name="register"),
path("login/",views_register.login_request,name="login"),
path('social/signup/', views_register.signup_redirect, name='signup_redirect'),
path('profile/', view_profile.profile, name='profile'),
path('search/', view_profile.search,name="search"),
path('provide_service/', view_profile.provide_service,name="provide_service"),
path('edit_profile/', view_profile.edit_profile,name="edit_profile"),
path('tickets/', view_profile.ticket_form,name="tickets"),
path('your_tickets/', view_profile.your_tickets,name="your_tickets"),
path('updateprofile/',view_profile.updateprofile,name="updateprofile"),
path('wishlist/',view_profile.wishlist,name="wishlist"),
path('wishlist/add_to_wishlist/<int:id>',view_profile.add_to_wishlist,name="user_wishlist"),
path('cart/add_to_cart/<int:id>',view_profile.add_to_cart,name="user_cart"),
path('cart/',view_profile.cart,name="cart"),
path('ticket_list/',view_profile.ticket_list,name="ticket_list"),
path('invite/',view_profile.invite,name="invite"),
path('activity/',view_profile.activity,name="activity"),
path('mainchat/',view_profile.mainchat,name="mainchat"),
path('mainchat/chat/<int:sender_id>/<int:recipient_id>/', view_profile.chat, name='chat'),
path('mainchat/send_message/<int:sender_id>/<int:recipient_id>/', view_profile.send_message, name='send_message'),
]