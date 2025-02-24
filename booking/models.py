from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hotels/')
    rating = models.FloatField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
#     check_in = models.DateField()
#     check_out = models.DateField()
#     guests = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.hotel.name} ({self.check_in} - {self.check_out})"


class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"Отзыв от {self.author}"

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=100, choices=[
        ('standard', 'Стандартный'),
        ('deluxe', 'Делюкс'),
        ('suite', 'Люкс'),
    ])
    guests_num = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Комната {self.room_number} ({self.get_room_type_display()}) - {self.hotel.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Добавили связь с номером
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name}, Комната {self.room.room_number} ({self.check_in} - {self.check_out})"