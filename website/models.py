from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

from .managers import *
import os

# Modelo de la base de datos

class ProfileUser(AbstractBaseUser, PermissionsMixin):
    def img_upload_to(self, instance=None):
        if instance:
            return os.path.join('restaurants/', str(self.email), instance)
        return None
    # password = models.CharField(max_length=200, verbose_name='Contraseña')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='Último inicio de sesión')
    username = models.CharField(max_length=200, default=None, unique=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Primer nombre')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Apellido')
    phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Coloque un número de teléfono válido.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name='Número de télefono')
    profile_img = models.ImageField(default='restaurants/profile.png', upload_to=img_upload_to, blank=True, null=True, verbose_name='Foto del perfil')
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, verbose_name='Cuenta activa')
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username if self.username != None else self.email
    
# class Comensale(Usuario):
#   username = models.CharField(max_length=200, null=True, unique=True)
#   address = models.TextField(null=True)

#   def __str__(self):
#     return self.nombre_usuario

class Restaurant(ProfileUser):
    PLAN = (
        ('Plan Básico','Plan Básico'),
        ('Plan Plata', 'Plan Plata'),
        ('Plan Oro', 'Plan Oro'),
        ('Plan Platino','Plan Platino'),
    )
    name = models.CharField(max_length=300, blank=True, null=True, unique=True, verbose_name='Nombre del restaurante')
    plan = models.CharField(max_length=200, choices=PLAN, blank=True, null=True)
    start_schedule = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='Horario de apertura')
    end_schedule = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='Horario de cierre')
    pick_up = models.BooleanField(blank=True, null=True, verbose_name='Pick-up')
    my_delivery = models.BooleanField(blank=True, null=True, verbose_name='Delivery propio')
    external_delivery = models.BooleanField(blank=True, null=True, verbose_name='Servicio de delivery externo')
    others_services = models.BooleanField(blank=True, null=True, verbose_name='Otros tipos de servicios')
    delivery = models.TextField(default=None, blank=True, null=True, verbose_name='Servicios externos')
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name='Estado')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ciudad')
    parish = models.CharField(max_length=100, blank=True, null=True, verbose_name='Parroquia')
    avenue = models.CharField(max_length=100, blank=True, null=True, verbose_name='Avenida')
    street = models.CharField(max_length=100, blank=True, null=True, verbose_name='Calle')
    full_address = models.CharField(max_length=500, blank=True, null=True, verbose_name='Dirección completa')
  
    def __str__(self):
        return self.name

# class Administrador(Usuario):
#   username = models.CharField(max_length=200, null=True, unique=True)
  
#   def __str__(self):
#     return self.nombre

class BrandOffice(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    is_restaurant = models.BooleanField(default=False, null=True)
    brand_name = models.CharField(max_length=300, null=True, verbose_name='Nombre de la sucursal')
    start_schedule = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='Horario de apertura')
    end_schedule = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='Horario de cierre')
    pick_up = models.BooleanField(blank=True, null=True, verbose_name='Pick-up')
    my_delivery = models.BooleanField(blank=True, null=True, verbose_name='Delivery propio')
    external_delivery = models.BooleanField(blank=True, null=True, verbose_name='Servicio de delivery externo')
    others_services = models.BooleanField(blank=True, null=True, verbose_name='Otros tipos de servicios')
    delivery = models.TextField(default=None, blank=True, null=True, verbose_name='Servicios externos')
    state = models.CharField(max_length=100, null=True, verbose_name='Estado')
    city = models.CharField(max_length=100, null=True, verbose_name='Ciudad')
    parish = models.CharField(max_length=100, null=True, verbose_name='Parroquia')
    avenue = models.CharField(max_length=100, blank=True, null=True, verbose_name='Avenida')
    street = models.CharField(max_length=100, blank=True, null=True, verbose_name='Calle')
    full_address = models.CharField(max_length=500, blank=True, null=True, verbose_name='Dirección completa')
    active = models.BooleanField(default=False, null=True, verbose_name='¿Esta operativa la sucursal?')
  
    def __str__(self):
        return self.brand_name
    
    def brand_img(self):
        return self.restaurant.profile_img

class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=500, null=True, verbose_name="Nombre del platillo")
    description = models.TextField(null=True, verbose_name="Descipción del platillo")
    price = models.FloatField(validators=[MinValueValidator(1)], null=True, verbose_name="Precio del platillo")
    tags = models.TextField(blank=True, null=True, verbose_name="Etiquetas del platillo")
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name="Cantidad disponible")
    active = models.BooleanField(default=False, null=True, verbose_name='Mostrar platillo')
    date_modify = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.dish_name

class ImgDish(models.Model):
    def img_upload_to(self, instance=None):
        if instance:
            return os.path.join('restaurants/', str(self.dish.restaurant.email) + "/dishes/" + str(self.folder), instance)
        return None
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=img_upload_to, null=True)
    select = models.BooleanField(default=True, null=True)
    order = models.PositiveIntegerField(default=None, null=True)
    folder = models.TextField(null=True, editable=False)
    date_upload = models.DateTimeField(default=timezone.now, null=True, editable=False)

class Menu(models.Model):
    def img_upload_to(self, instance=None):
        if instance:
            return os.path.join('restaurants/', str(self.restaurant.email) + "/menu/", instance)
        return None
    dishes = models.ManyToManyField(Dish, related_name="menudishes", through='MenuDish')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    brands = models.ManyToManyField(BrandOffice, related_name="menubrands", through='MenuBrand', blank=True)
    menu_name = models.CharField(max_length=200, null=True)
    promo = models.BooleanField(default=False, null=True)
    discount = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(100)], blank=True, null=True)
    imagen = models.ImageField(default='icon/front-page.png', upload_to=img_upload_to, blank=True, null=True)
    imagen_promo = models.ImageField(upload_to=img_upload_to, blank=True, null=True)
    active = models.BooleanField(default=False, null=True, verbose_name='Publicar menú')

    def __str__(self):
        return self.menu_name
    
class MenuDish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True)

    def get_data_dish(self):
        return Dish.objects.get(id=self.dish.id)
    
    def get_data_menu(self):
        return Menu.objects.get(id=self.menu.id)

class MenuBrand(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(BrandOffice, on_delete=models.CASCADE, null=True)