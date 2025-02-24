from django.urls import path
from .views import hotel_list,book_hotel, booking_success
from django.contrib.auth import views as auth_views
from . import views
from .views import register, user_login, user_logout, contact_view


urlpatterns = [
    path('', hotel_list, name='hotel-list'),
    #path('book/<int:hotel_id>/', book_hotel, name='book-hotel'),
    #path('booking-success/', booking_success, name='booking_success'),
    path("book/<int:room_id>/", book_hotel, name="book-hotel"),
    path("booking-success/", booking_success, name="booking_success"),
    path("register/", register, name="register"),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact_view, name='contact'),
]
