from django_filters import FilterSet, CharFilter,ChoiceFilter, NumberFilter, TimeFilter, ModelMultipleChoiceFilter, ModelChoiceFilter, ChoiceFilter
from django import forms
from django.forms.widgets import TextInput, NumberInput, TimeInput, NullBooleanSelect, SelectMultiple, Select

from .models import *

import json

CHOICE_ACTIVE = {
  ('true', 'Activos'),
  ('false', 'Inactivos')
}
CHOICE_YES_OR_NOT = {
  ('true', 'Sí'),
  ('false', 'No')
}

class BrandFilter(FilterSet):
  brand_name = CharFilter(
    field_name = "brand_name",
    lookup_expr = 'icontains',
    label = "Nombre",
    widget = TextInput(
      attrs = {
        'placeholder':'Nombre',
        'class': 'form-control'
      }
    )
  )
  start_schedule = TimeFilter(
    field_name = "start_schedule",
    lookup_expr = "gte",
    label = "Comienzo del horario",
    widget = TimeInput(
      attrs = {
        'type': 'time',
        'class':'form-control'
      }
    )
  )
  end_schedule = TimeFilter(
    field_name = "end_schedule",
    lookup_expr = "lte",
    label = "Fin del horario",
    widget = TimeInput(
      attrs = {
        'type': 'time',
        'class':'form-control'
      }
    )
  )
  pick_up = ChoiceFilter(
    field_name = "pick_up",
    label = "Tiene pick-up",
    widget = NullBooleanSelect(
      attrs = {
        'class': 'form-select'
      }
    ),
    choices = CHOICE_YES_OR_NOT,
  )
  my_delivery = ChoiceFilter(
    field_name = "my_delivery",
    label = "Tiene delivery propio",
    widget = NullBooleanSelect(
      attrs = {
        'class': 'form-select'
      }
    ),
    choices = CHOICE_YES_OR_NOT,
  )
  full_address = CharFilter(
    field_name = "full_address",
    lookup_expr = 'icontains',
    label = "Ubicación",
    widget = TextInput(
      attrs = {
        'placeholder': 'Ubicación',
        'class': 'form-control'
      }
    )
  )
  delivery = CharFilter(
    field_name = "delivery",
    lookup_expr = 'icontains',
    label = "Servicios externos",
    widget = TextInput(
      attrs = {
        'placeholder':'Servicios externos',
        'class': 'form-control'
      }
    )
  )
  CHOICE_ACTIVE_BRANDS = {
    ('true', 'Activas'),
    ('false', 'Inactivas')
  }
  active = ChoiceFilter(
    field_name = "active",
    lookup_expr = 'exact',
    label = "Mostrar sucursales",
    widget = NullBooleanSelect(
      attrs = {
        'class': 'form-select'
      }
    ),
    choices = CHOICE_ACTIVE_BRANDS,
  )
  class Meta:
    model = BrandOffice
    fields = ['brand_name', 'start_schedule', 'end_schedule', 'pick_up', 'my_delivery', 'delivery', 'full_address', 'active']
    exclude = ['restaurant', 'external_delivery', 'others_services','state', 'city', 'parish', 'avenue', 'street']

class MenuFilter(FilterSet):
  def __init__(self,*args, **kwargs):
    current_user = kwargs['current_user']
    del kwargs['current_user']
    super(MenuFilter, self).__init__(*args, **kwargs)
    dishes_all = current_user.user.restaurant.dish_set.all()
    restaurant_dishes = list(dishes_all.filter(active=True).values_list('id', flat=True))
    dishes_menu = list(MenuDish.objects.filter(dish__in=restaurant_dishes).distinct().values_list('dish_id', flat=True))
    brands_all = current_user.user.restaurant.brandoffice_set.all()
    restaurant_brands = list(brands_all.filter(active=True).values_list('id', flat=True))
    brands_menu = list(MenuBrand.objects.filter(brand__in=restaurant_brands).distinct().values_list('brand_id', flat=True))
    self.filters['dishes'].queryset = dishes_all.filter(id__in=dishes_menu)
    self.filters['dishes'].label = "Platillos"
    self.filters['brands'].queryset = brands_all.filter(id__in=brands_menu)
    self.filters['brands'].label = "Sucursales"

  menu_name = CharFilter(
    field_name = "menu_name",
    lookup_expr = 'icontains',
    label = "Nombre",
    widget = TextInput(
      attrs = {
        'placeholder':'Nombre',
        'class': 'form-control'
      }
    )
  )
  dishes = ModelMultipleChoiceFilter(
    field_name = "dishes",
    widget = SelectMultiple(
      attrs = {
        'class':'form-select'
      }
    )
  )
  # in_principal = ChoiceFilter(
  #   field_name="in_principal",
  #   label="¿Está en la sede principal?",
  #   widget = NullBooleanSelect(
  #     attrs = {
  #       'class': 'form-select'
  #     }
  #   ),
  #   choices = CHOICE_YES_OR_NOT,
  # )
  brands = ModelMultipleChoiceFilter(
    field_name = "brands",
    widget = SelectMultiple(
      attrs = {
        'class':'form-select'
      }
    )
  )
  active = ChoiceFilter(
    field_name = "active",
    lookup_expr = 'exact',
    label = "Mostrar menus",
    widget = NullBooleanSelect(
      attrs = {
        'class': 'form-select'
      }
    ),
    choices = CHOICE_ACTIVE,
  )
  class Meta:
    model = Menu
    fields = ['menu_name', 'dishes', 'brands', 'active']
    exclude = ['restaurant', 'imagen', 'imagen_promo', 'discount', 'promo']

class DishFilter(FilterSet):
  dish_name = CharFilter(
    field_name = "dish_name",
    lookup_expr = 'icontains',
    label = "Nombre",
    widget = TextInput(
      attrs = {
        'placeholder':'Nombre',
        'class': 'form-control'
      }
    )
  )
  price = NumberFilter(
    field_name = "price",
    label = "Precio",
    widget = NumberInput(
      attrs = {
        'placeholder': 'Precio ($)',
        'class': 'form-control'
      }
    )
  )
  tags = CharFilter(
    field_name = "tags",
    lookup_expr = 'icontains',
    label = "Etiquetas",
    widget = TextInput(
      attrs = {
        'placeholder':'Etiquetas',
        'class': 'form-control'
      }
    )
  )
  active = ChoiceFilter(
    field_name = "active",
    lookup_expr = 'exact',
    label = "Mostrar platillos",
    widget = NullBooleanSelect(
      attrs = {
        'class': 'form-select'
      }
    ),
    choices = CHOICE_ACTIVE,
  )

  class Meta:
    model = Dish
    fields = ['dish_name', 'price', 'tags', 'active']
    exclude = ['restaurant', 'description', 'amount','date_modify']

class PromoFilter(FilterSet):
  def __init__(self,*args, **kwargs):
    current_user = kwargs['current_user']
    del kwargs['current_user']
    super(PromoFilter, self).__init__(*args, **kwargs)
    dishes_all = current_user.user.restaurant.dish_set.all()
    restaurant_dishes = list(dishes_all.filter(active=True).values_list('id', flat=True))
    dishes_menu = list(MenuDish.objects.filter(dish__in=restaurant_dishes).distinct().values_list('dish_id', flat=True))
    brands_all = current_user.user.restaurant.brandoffice_set.all()
    restaurant_brands = list(brands_all.filter(active=True).values_list('id', flat=True))
    brands_menu = list(MenuBrand.objects.filter(brand__in=restaurant_brands).distinct().values_list('brand_id', flat=True))
    self.filters['dishes'].queryset = dishes_all.filter(id__in=dishes_menu)
    self.filters['dishes'].label = "Platillos"
    self.filters['brands'].queryset = brands_all.filter(id__in=brands_menu)
    self.filters['brands'].label = "Sucursales"

  menu_name = CharFilter(
    field_name = "menu_name",
    lookup_expr = 'icontains',
    label = "Nombre",
    widget = TextInput(
      attrs = {
        'placeholder':'Nombre',
        'class': 'form-control'
      }
    )
  )
  discount = NumberFilter(
    field_name = "discount",
    label = "Descuento",
    widget = NumberInput(
      attrs = {
        'placeholder': 'Descuento (%)',
        'class': 'form-control',
        'min':'0',
        'max':'100'
      }
    )
  )
  discount__gte = NumberFilter(
    field_name = 'discount',
    lookup_expr = 'gte',
    label = "Descuento mayor que",
    widget = NumberInput(
      attrs = {
        'placeholder': '(%)',
        'class': 'form-control',
        'min':'0'
      }
    )
  )
  discount__lte = NumberFilter(
    field_name = 'discount',
    lookup_expr = 'lte',
    label = "Descuento menor que",
    widget = NumberInput(
      attrs = {
        'placeholder':'(%)',
        'class': 'form-control',
        'max':'100'
      }
    )
  )
  dishes = ModelMultipleChoiceFilter(
    field_name = "dishes",
    widget = SelectMultiple(
      attrs = {
        'class':'form-select'
      }
    )
  )
  brands = ModelMultipleChoiceFilter(
    field_name = "brands",
    widget = SelectMultiple(
      attrs = {
        'class':'form-select'
      }
    )
  )
  CHOICE_ACTIVE_PROMO = {
    ('true', 'Activas'),
    ('false', 'Inactivas')
  }
  active = ChoiceFilter(
    field_name = "active",
    lookup_expr = 'exact',
    label = "Mostrar promociones",
    widget = NullBooleanSelect(
      attrs = {
        'class': 'form-select'
      }
    ),
    choices = CHOICE_ACTIVE_PROMO,
  )
  class Meta:
    model = Menu
    fields = ['menu_name', 'discount','discount__gte','discount__lte','dishes', 'brands', 'active']
    exclude = ['restaurant', 'imagen', 'imagen_promo', 'promo']
    
class RestaurantsFilter(FilterSet):
  states = [str(state) for state in BrandOffice.objects.order_by('state').values_list('state', flat=True).distinct()]
  state_select = ChoiceFilter(
    field_name = "state",
    required = True, 
    widget = Select(
      attrs = {
        'id':'SelectState',
        'class':'form-select btn-address',
        'name':'state',
        'aria-placeholder':'Estado',
        'required':True,
        'hidden':True
      }
    ),
    choices=([(state, state) for state in states]),
  )
  full_address = CharFilter(
    field_name = "full_address",
    lookup_expr = 'icontains',
    widget = TextInput(
      attrs = {
        'id':'TextAddress',
        'placeholder':'Dirección: Ciudad, Parroquia, Avenida, Calle...',
        'class': 'form-control',
        'name':'address'
      }
    )
  )
  class Meta:
    model = BrandOffice
    fields = ['state_select', 'full_address']

  def clean_full_address(self):
    return self.cleaned_data['full_address'].lower().capitalize()