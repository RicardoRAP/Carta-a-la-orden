from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  model = User
  list_display = ("username", "email", "first_name","phone", "is_staff", "is_active", "is_superuser", "last_login")
  list_filter = ("username", "email", "first_name","phone", "is_staff", "is_active", "is_superuser", "last_login")
  fieldsets = (
    (None, {"fields": ("username", "email", "first_name", "last_name", "phone", "profile_img", "password")}),
    ("Permisos", {"fields": ("is_staff", "is_active", "is_superuser","groups", "user_permissions")}),
  )
  add_fieldsets = (
    (None, {
      "classes": ("wide",),
      "fields": (
        "email","password1","password2","is_staff","is_active","is_superuser","groups","user_permissions"
      )}
    ),
  )
  search_fields = ("email",)
  ordering = ("email",)

class CustomUserRestaurant(UserAdmin):
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  model = Restaurant
  list_display = ("name", "email", "username", "phone", "plan", "is_active", "last_login")
  list_filter = ("name", "email", "username", "phone", "plan", "is_active", "last_login")
  fieldsets = (
    (None, {"fields": ("name", "email", "username", "phone", "plan", "password")}),
    ("Permisos", {"fields": ("is_staff", "is_active", "is_superuser","groups")}),
  )
  add_fieldsets = (
    (None, {
      "classes": ("wide",),
      "fields": (
        "email","name","phone","plan","password1","password2","is_active"
      )}
    ),
  )
  search_fields = ("email",)
  ordering = ("email",)