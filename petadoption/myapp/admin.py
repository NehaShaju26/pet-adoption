from django.contrib import admin
from .models import Address, Pet, PetType, Category, Booking, Profile
# Register your models here.
admin.site.register(Address)
admin.site.register(Pet)
admin.site.register(PetType)
admin.site.register(Category)
admin.site.register(Booking)
admin.site.register(Profile)
