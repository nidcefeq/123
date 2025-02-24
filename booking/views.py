from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Review, Booking, Room
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import BookingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import Min

# def hotel_list(request):
#     hotels = Hotel.objects.all()
#     reviews = Review.objects.all()
#     return render(request, 'booking/hotels.html', {'hotels': hotels, 'reviews': reviews})

# @login_required
# def book_hotel(request, hotel_id):
#     hotel = Hotel.objects.get(id=hotel_id)
#     if request.method == "POST":
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.hotel = hotel
#             booking.save()
#             return redirect('booking_success')
#     else:
#         form = BookingForm(initial={'hotel': hotel})
#
#     return render(request, 'booking/book_hotel.html', {'form': form, 'hotel': hotel})

@login_required
def book_hotel(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    hotel = room.hotel  # Получаем отель через связь

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.hotel = hotel
            booking.room = room  # Теперь номер сохраняется в БД
            booking.save()
            messages.success(request, "Бронирование успешно оформлено!")
            return redirect("booking_success")
    else:
        form = BookingForm(initial={"room": room})  # Передаём номер в форму

    return render(request, "booking/book_hotel.html", {
        "form": form,
        "room": room,
        "hotel": hotel
    })


def booking_success(request):
    return render(request, 'booking/booking_success.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect("hotel-list")
    else:
        form = RegisterForm()

    return render(request, "booking/register.html", {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('hotel-list')
    else:
        form = LoginForm()
    return render(request, 'booking/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('hotel-list')



def hotel_list(request):
    city = request.GET.get("city", "")
    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")
    guests = request.GET.get("guests")

    if city or check_in or check_out or guests:
        rooms = Room.objects.select_related('hotel').annotate(min_price=Min('price_per_night'))

        if city:
            rooms = rooms.filter(hotel__city__icontains=city)

        if check_in and check_out and guests:
            guests = int(guests)
            available_rooms = []

            for room in rooms:
                if room.guests_num >= guests:
                    conflicting_bookings = Booking.objects.filter(
                        hotel=room.hotel,
                        check_out__gt=check_in,
                        check_in__lt=check_out
                    )
                    if not conflicting_bookings.exists():
                        available_rooms.append(room)

            rooms = available_rooms

        reviews = Review.objects.select_related("hotel").order_by("-id")[:5]

        return render(request, "booking/hotels.html", {
            "rooms": rooms,
            "search_mode": True,
            "reviews": reviews
        })

    else:
        hotels = Hotel.objects.annotate(min_price=Min('rooms__price_per_night'))
        reviews = Review.objects.select_related("hotel").order_by("-id")[:5]

        return render(request, "booking/hotels.html", {
            "hotels": hotels,
            "search_mode": False,
            "reviews": reviews
        })


def contact_view(request):
    return render(request, 'booking/contact.html')
