from django.contrib import admin
from .models import Hotel, Review, Booking, Room

admin.site.register(Hotel)
admin.site.register(Review)
admin.site.register(Booking)
admin.site.register(Room)