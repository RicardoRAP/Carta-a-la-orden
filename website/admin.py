from django.contrib import admin

# Register your models here.

from .admin_forms import *
from .models import *

# Vista de los modelos en la vista del administrador

admin.site.register(ProfileUser, CustomUserAdmin)
admin.site.register(Restaurant, CustomUserRestaurant)
admin.site.register(BrandOffice, BrandPanel)
admin.site.register(Menu, MenuPanel)
admin.site.register(Dish, DishPanel)
admin.site.register(ImgDish, ImgDishPanel)