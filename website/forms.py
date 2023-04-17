from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet, BaseModelFormSet


from .models import *
import re


class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = ProfileUser
    fields = ("email",)
  
  def clean_email(self):
    return self.cleaned_data['email'].lower()


class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = ProfileUser
    fields = ("email",)
  
  def clean_email(self):
    return self.cleaned_data['email'].lower()

class CreateRestaurantForm(UserCreationForm):
  name = forms.CharField(
    max_length = 300,  
    required = True, 
    help_text = 'Se requiere: Nombre',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerName',
        'class': 'form-control', 
        'placeholder': 'Nombre'
      }
    )
  )
  email = forms.EmailField(
    required = True, 
    help_text = 'Se requiere: Email',
    widget = forms.TextInput(
      attrs = {
        'type': 'email',
        'id': 'registerEmail',
        'class': 'form-control', 
        'placeholder': 'Email'
      }
    )
  )
  phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Coloque un número de teléfono válido.")
  phone = forms.CharField(
    validators = [phone_regex], 
    max_length = 17, 
    required = True,
    help_text = 'Se requiere: Número de télefono',
    widget = forms.TextInput(
      attrs = {
        'type': 'tel',
        'id': 'registerPhone',
        'class': 'form-control', 
        'placeholder': 'Teléfono'
      }
    )
  )
  PLAN = (
    (None,'Selecciona tu plan'),
    ('Plan Básico','Plan Básico'),
    ('Plan Plata', 'Plan Plata'),
    ('Plan Oro', 'Plan Oro'),
    ('Plan Platino','Plan Platino'),
  )
  plan = forms.ChoiceField(
    choices = PLAN,
    required = True,
    help_text = 'Se requiere que seleccione un plan',
    widget = forms.Select(
      attrs = {
        'id': 'registerPlan',
        'class': 'form-select', 
        'aria-label': 'Selecciona tu plan'
      }
    )
  )
  state = forms.CharField(
    max_length = 100,  
    required = True, 
    help_text = 'Se requiere: Estado',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerState',
        'class': 'form-control address', 
        'placeholder': 'Estado'
      }
    )
  )
  city = forms.CharField(
    max_length = 100,  
    required = True, 
    help_text = 'Se requiere: Ciudad',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerCity',
        'class': 'form-control address', 
        'placeholder': 'Ciudad'
      }
    )
  )
  parish = forms.CharField(
    max_length = 100,  
    required = True, 
    help_text = 'Se requiere: Ciudad',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerParish',
        'class': 'form-control address', 
        'placeholder': 'Parroquia'
      }
    )
  )
  password1 = forms.CharField(
    label = _('Contraseña'),
    help_text = password_validation.password_validators_help_text_html(),
    widget = forms.PasswordInput(
      attrs = {
        'id': 'registerPassword',
        'class': 'form-control',
        'placeholder': 'Contraseña'
      }
    ),
  )
  password2 = forms.CharField(
    label = _('Password Confirmation'), 
    help_text = _('Introduzca la misma contraseña para confirmar'),
    widget = forms.PasswordInput(
      attrs = {
        'id': 'registerRepeatPassword',
        'class': 'form-control',
        'placeholder': 'Confirme la contraseña'
      }
    )
  )
  class Meta:
    model = Restaurant
    fields = ('name', 'email', 'phone', 'plan','state','city','parish', 'password1', 'password2',)
    exclude = ['full_address']

  def clean_email(self):
    return self.cleaned_data['email'].lower()

  def clean_state(self):
    return self.cleaned_data['state'].lower().capitalize()
  
  def clean_city(self):
    return self.cleaned_data['city'].lower().capitalize()
  
  def clean_parish(self):
    return self.cleaned_data['parish'].lower().capitalize()
  


#  Formulario del Perfil
class ProfileForm(ModelForm):
  profile_img = forms.ImageField(
    required = True, 
    help_text = 'Ingresa una imagen',
    widget = forms.FileInput(
      attrs = {
        'type': 'file',
        'id': 'formProfile_img',
        'class': 'form-control d-none'
      }
    )
  )
  username = forms.CharField(
    max_length = 200,  
    required = True, 
    help_text = 'Se requiere: Nombre de usuario',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'saveUsername',
        'class': 'form-control',
        'style':'text-transform: lowercase;',
        'placeholder':"Nombre de usuario"
      }
    )
  )
  name = forms.CharField(
    max_length = 300,  
    required = True, 
    help_text = 'Se requiere: Nombre del restaurante',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'saveName',
        'class': 'form-control',
        'placeholder':"Nombre del restaurante"
      }
    )
  )
  email = forms.EmailField(
    required = True, 
    help_text = 'Se requiere: Email',
    widget = forms.EmailInput(
      attrs = {
        'type': 'email',
        'id': 'saveEmail',
        'style':'text-transform: lowercase;',
        'class': 'form-control', 
        'placeholder': 'Email'
      }
    )
  )
  phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Coloque un número de teléfono válido.")
  phone = forms.CharField(
    validators = [phone_regex], 
    max_length = 17, 
    required = True,
    help_text = 'Se requiere: Número de télefono',
    widget = forms.TextInput(
      attrs = {
        'type': 'tel',
        'id': 'savePhone',
        'class': 'form-control', 
        'placeholder': 'Teléfono'
      }
    )
  )
  start_schedule = forms.TimeField(
    widget = forms.TimeInput(
      attrs={
        'id': 'saveStart_schedule',
        'type':'time',
        'class':'form-control',
        'min':"00:00",
        'max':'24:00',
        'placeholder': 'Comiezo del horario. Ej: 09:00'
      }
    )
  )
  end_schedule = forms.TimeField(
    widget = forms.TimeInput(
      attrs = {
        'id': 'saveEnd_schedule',
        'type':'time',
        'class':'form-control',
        'min':"00:00",
        'max':'24:00',
        'placeholder': 'Finaliza el horario. Ej: 08:00'
      }
    )
  )
  PLAN = (
    (None,'Selecciona tu plan'),
    ('Plan Básico','Plan Básico'),
    ('Plan Plata', 'Plan Plata'),
    ('Plan Oro', 'Plan Oro'),
    ('Plan Platino','Plan Platino'),
  )
  plan = forms.ChoiceField(
    choices = PLAN,
    required = True,
    help_text = 'Se requiere que seleccione un plan',
    widget = forms.Select(
      attrs = {
        'id': 'savePlan',
        'class': 'form-select', 
        'aria-label': 'Selecciona tu plan'
      }
    )
  )
  state = forms.CharField(
    max_length = 100,  
    required = True, 
    help_text = 'Se requiere: Estado',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'saveState',
        'class': 'form-control address', 
        'placeholder': 'Estado'
      }
    )
  )
  city = forms.CharField(
    max_length = 100,  
    required = True, 
    help_text = 'Se requiere: Ciudad',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'saveCity',
        'class': 'form-control address', 
        'placeholder': 'Ciudad'
      }
    )
  )
  parish = forms.CharField(
    max_length = 100,  
    required = True, 
    help_text = 'Se requiere: Parroquia',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'saveParish',
        'class': 'form-control address', 
        'placeholder': 'Parroquia'
      }
    )
  )
  avenue = forms.CharField(
    max_length = 100,  
    required = False,
    help_text = 'Se requiere: Avenida',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'saveAvenue',
        'class': 'form-control address', 
        'placeholder': 'Avenida'
      }
    )
  )
  street = forms.CharField(
    max_length = 100,  
    required = False,
    help_text = 'Se requiere: Calle',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'saveStreet',
        'class': 'form-control address', 
        'placeholder': 'Calle'
      }
    )
  )
  full_address = forms.CharField(
    max_length = 500,  
    required = False,
    help_text = 'Se requiere: Dirrección completa',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'saveFull_address',
        'class': 'form-control d-none', 
        'placeholder': 'Dirección completa',
      }
    ),
    show_hidden_initial = True
  )
  pick_up = forms.BooleanField(
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'flexCheckPickUp',
        'class':'form-check-input',
      }
    )
  )
  my_delivery = forms.BooleanField(
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'flexCheckMyDelivery',
        'class':'form-check-input',
      }
    )
  )
  external_delivery = forms.BooleanField(
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'flexCheckExternalDelivery',
        'class':'form-check-input others-serv',
      }
    )
  )
  others_services = forms.BooleanField(
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'flexCheckOthersServices',
        'class':'form-check-input others-serv',
      }
    )
  )
  delivery = forms.CharField(
    max_length = 500,
    required = False, 
    help_text = 'Ingresa los servicios que poseas',
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'saveDelivery',
        'class': 'form-control'
      }
    )
  )
  class Meta:
    model = Restaurant
    fields = ['profile_img','username','name','email','phone','start_schedule','end_schedule','plan','state','city','parish','avenue','street','full_address','pick_up','my_delivery','external_delivery','others_services','delivery']
    exculde = ['is_staff', 'is_active', 'is_superuser', 'group', 'date_joined']
  
  def NormalizeUsarname(self):
    cleaned_data = super(ProfileForm,self).clean()
    username = cleaned_data.get('username')
    username = str(username).lower()
    username_format = re.compile(r'(^[a-zA-Z0-9\_\.\&]+$)')
    if not re.match(username_format,username):
      return False
    return cleaned_data

  def clean_username(self):
    return self.cleaned_data['username'].lower()
  
  def clean_email(self):
    return self.cleaned_data['email'].lower()
  
  def clean_state(self):
    return self.cleaned_data['state'].lower().capitalize()
  
  def clean_city(self):
    return self.cleaned_data['city'].lower().capitalize()
  
  def clean_parish(self):
    return self.cleaned_data['parish'].lower().capitalize()
  
  def clean_avenue(self):
    return self.cleaned_data['avenue'].lower().capitalize()
  
  def clean_street(self):
    return self.cleaned_data['street'].lower().capitalize()
  
  def clean_full_address(self):
    return self.cleaned_data['full_address'].lower().capitalize()
  
  def clean(self):
    cleaned_data = super(ProfileForm, self).clean()
    user_exists = (Restaurant.objects.filter(email = cleaned_data.get('email')).count() > 0)
    if user_exists:
      self.add_error('email', 'ese email ya existe')

#  Formulario de las Sucursales
class BrandForm(ModelForm):
  brand_name = forms.CharField(
    label = 'Nombre de la sucursal:',
    max_length = 300,
    required = True, 
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerName',
        'class': 'form-control',
        'placeholder': 'Nombre de la sucursal'
      }
    )

  )
  start_schedule = forms.TimeField(
    label = 'Comienzo del Horario:',
    widget = forms.TimeInput(
      attrs={
        'id': 'registerStart_schedule',
        'type':'time',
        'class':'form-control',
        'min':"00:00",
        'max':'24:00',
        'placeholder': 'Comiezo del horario. Ej: 09:00'
      }
    )
  )
  end_schedule = forms.TimeField(
    label = 'Final del Horario:',
    widget = forms.TimeInput(
      attrs = {
        'id': 'registerEnd_schedule',
        'type':'time',
        'class':'form-control',
        'min':"00:00",
        'max':'24:00',
        'placeholder': 'Finaliza el horario. Ej: 08:00'
      }
    )
  )
  pick_up = forms.BooleanField(
    label = 'Pick-up',
    label_suffix = '',
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'flexCheckPickUp',
        'class':'form-check-input',
      }
    )
  )
  my_delivery = forms.BooleanField(
    label = 'Delivery propio',
    label_suffix = '',
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'flexCheckMyDelivery',
        'class':'form-check-input',
      }
    )
  )
  external_delivery = forms.BooleanField(
    label = 'Servicio de delivery externo',
    label_suffix = '',
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'flexCheckExternalDelivery',
        'class':'form-check-input others-serv',
      }
    )
  )
  others_services = forms.BooleanField(
    label = 'Otros tipos de servicios',
    label_suffix = '',
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'flexCheckOthersServices',
        'class':'form-check-input others-serv',
      }
    )
  )
  delivery = forms.CharField(
    label = '',
    max_length = 500,
    required = False, 
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerDelivery',
        'class': 'form-control'
      }
    )
  )
  state = forms.CharField(
    label = 'Estado',
    max_length = 100,  
    required = True, 
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerState',
        'class': 'form-control address', 
        'placeholder': 'Estado'
      }
    )
  )
  city = forms.CharField(
    label = 'Ciudad',
    max_length = 100,  
    required = True, 
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerCity',
        'class': 'form-control address', 
        'placeholder': 'Ciudad'
      }
    )
  )
  parish = forms.CharField(
    label = 'Parroquia',
    max_length = 100,  
    required = True, 
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerParish',
        'class': 'form-control address', 
        'placeholder': 'Parroquia'
      }
    )
  )
  avenue = forms.CharField(
    label = 'Avenida',
    max_length = 100,  
    required = False,
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerAvenue',
        'class': 'form-control address', 
        'placeholder': 'Avenida'
      }
    )
  )
  street = forms.CharField(
    label = 'Calle',
    max_length = 100,  
    required = False,
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerStreet',
        'class': 'form-control address', 
        'placeholder': 'Calle'
      }
    )
  )
  full_address = forms.CharField(
    label = '',
    max_length = 500,  
    required = False,
    widget = forms.HiddenInput(
      attrs = {
        'type': 'hidden',
        'id': 'registerFull_address',
        'class': 'form-control d-none', 
        'placeholder': 'Dirección completa',
      }
    ),
    show_hidden_initial = True
  )
  active = forms.BooleanField(
    label = '¿Esta operativa la sucursal?',
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'CheckActive',
        'class':'form-check-input',
      }
    )
  )
  class Meta:
    model = BrandOffice
    fields = '__all__'
    exclude = ['restaurant','is_restaurant']
  
  def clean_state(self):
    return self.cleaned_data['state'].lower().capitalize()
  
  def clean_city(self):
    return self.cleaned_data['city'].lower().capitalize()
  
  def clean_parish(self):
    return self.cleaned_data['parish'].lower().capitalize()
  
  def clean_avenue(self):
    return self.cleaned_data['avenue'].lower().capitalize()
  
  def clean_street(self):
    return self.cleaned_data['street'].lower().capitalize()
  
  def clean_full_address(self):
    return self.cleaned_data['full_address'].lower().capitalize()

class CustomInlineFormSet(BaseInlineFormSet):
  def clean(self):
    super().clean()
    for form in self.forms:
      state = form.cleaned_data['state']
      city = form.cleaned_data['city']
      parish = form.cleaned_data['parish']
      avenue = form.cleaned_data['avenue']
      street = form.cleaned_data['street']
      full = state + ", " + city + ", " + parish
      if avenue != None and avenue != '':
        full += ", " + avenue
      if street != None and street != '':
        full += ", " + street
      form.cleaned_data['full_address'] = full
      # Actualizar el valor de la instancia
      form.instance.full_address = full

#  Formulario de los platillos
class DishForm(ModelForm):
  dish_name = forms.CharField(
    label = 'Nombre del platillo:',
    max_length = 500,
    required = True, 
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'registerName',
        'class': 'form-control',
        'placeholder': 'Nombre del platillo'
      }
    )
  )
  description = forms.CharField(
    label = 'Descripción del platillo',
    required= True,
    widget= forms.Textarea(
      attrs={
        'id': 'registerDescription',
        'class':'form-control',
        'rows':5,
        'placeholder': 'Descripción del platillo. Ej: Tomate, queso, etc'
      }
    ) 
  )
  price = forms.FloatField(
    label = 'Precio',
    required = True,
    widget = forms.NumberInput(
      attrs = {
        'id': 'registerPrice',
        'type':'number',
        'step': '0.01',
        'class':'form-control',
        'min':"0.01",
        'placeholder': 'Precio en $'
      }
    )
  )
  tags = forms.CharField(
    label = 'Etiquetas',
    required= False,
    widget = forms.Textarea(
      attrs = {
        'type':'textarea',
        'id': 'registerTags',
        'class':'form-control',
        'rows':1,
        'placeholder': 'Etiquetas del platillo (Opcional)'
      }
    )
  )
  amount = forms.IntegerField(
    min_value = 0,
    label = 'Cantidad disponible (opcional)',
    required = False,
    widget = forms.NumberInput(
      attrs = {
        'type':'number',
        'id': 'registerAmount',
        'class':'form-control',
      }
    ),
    help_text = 'Deje el campo vacio o coloque 0 para indicar que la cantidad es ilimitada',
  )
  active = forms.BooleanField(
    label = 'Mostrar platillo',
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'CheckActive',
        'class':'form-check-input',
      }
    )
  )
  class Meta:
    model = Dish
    fields = '__all__'
    exclude = ['restaurant', 'date_modify']

class MultipleImgForm(ModelForm):
  img = forms.ImageField(
    label = "Imagenes",
    required = True,
    widget= forms.ClearableFileInput(
      attrs = {
        'id':'multipleImg',
        'class':'form-img input-file-img',
        'multiple':True
      }
    ),
    error_messages = {'error':'Seleccione al menos 2 imagenes'}
  )
  class Meta:
    model = ImgDish
    fields = ('img',)

# Formulario del menu
class MenuForm(ModelForm):
  menu_name = forms.CharField(
    label = 'Nombre del menú',
    max_length = 200,
    required = True, 
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'Name_menu',
        'class': 'form-control',
        'placeholder': 'Nombre del menú'
      }
    )
  )
  dishes = forms.ModelMultipleChoiceField(
    queryset = Dish.objects.all(),
    required = True,
    widget = forms.SelectMultiple(
      attrs={
        'name':'dishes',
        'id':'id_dishes',
        'class': 'form-control form-select',
        'multiple':True,
        'required':True
      }
    )
  )
  brands = forms.ModelMultipleChoiceField(
    queryset = BrandOffice.objects.all(),
    required = False,
    widget = forms.SelectMultiple(
      attrs={
        'name':'brands',
        'id':'id_brands',
        'class': 'form-control form-select',
        'multiple':True
      }
    )
  )
  imagen = forms.ImageField(
    required = True, 
    help_text = 'Ingresa una imagen',
    widget = forms.FileInput(
      attrs = {
        'type': 'file',
        'id': 'Menu_img',
        'class': 'form-img input-file-img'
      }
    )
  )
  active = forms.BooleanField(
    label = 'Publicar menú',
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'CheckActive',
        'class':'form-check-input',
      }
    )
  )
  class Meta:
    model = Menu
    fields = ('menu_name','dishes','brands','imagen','active')
    exculde = ['restaurant','promo','discount','imagen_promo']
  
  def __init__(self, restaurant, *args, **kwargs):
    super(MenuForm, self).__init__(*args, **kwargs)
    self.fields['dishes'].queryset = Dish.objects.filter(restaurant=restaurant,active=True)
    self.fields['brands'].queryset = BrandOffice.objects.filter(restaurant=restaurant,active=True)

# Formulario del promo
class PromoForm(ModelForm):
  menu_name = forms.CharField(
    label = 'Nombre de la promoción',
    max_length = 200,
    required = True, 
    widget = forms.TextInput(
      attrs = {
        'type': 'text',
        'id': 'Name_menu',
        'class': 'form-control',
        'placeholder': 'Nombre de la promoción'
      }
    )
  )
  discount = forms.FloatField(
    min_value=0,
    max_value=100,
    required=False,
    widget= forms.NumberInput(
      attrs={
        'id':'Discount',
        'class': 'form-control input-number',
        'placeholder': 'Descuento (%) opcional'
      }
    )
  )
  dishes = forms.ModelMultipleChoiceField(
    queryset = Dish.objects.all(),
    required = True,
    widget = forms.SelectMultiple(
      attrs={
        'name':'dishes',
        'id':'id_dishes',
        'class': 'form-control form-select',
        'multiple':True,
        'required':True
      }
    )
  )
  brands = forms.ModelMultipleChoiceField(
    queryset = BrandOffice.objects.all(),
    required = True,
    widget = forms.SelectMultiple(
      attrs = {
        'name':'brands',
        'id':'id_brands',
        'class': 'form-control form-select',
        'multiple':True
      }
    ),
    help_text = "Selecciona por lo menos una sucursal"
  )
  imagen = forms.ImageField(
    required = True, 
    help_text = 'Ingresa una imagen para el perfil de la promoción',
    widget = forms.FileInput(
      attrs = {
        'type': 'file',
        'id': 'Menu_img',
        'class': 'form-img input-file-img'
      }
    )
  )
  imagen_promo = forms.ImageField(
    required = True, 
    help_text = 'Ingresa la imagen de la promoción',
    widget = forms.FileInput(
      attrs = {
        'type': 'file',
        'id': 'Menu_promo_img',
        'class': 'form-img input-file-img'
      }
    )
  )
  active = forms.BooleanField(
    label = 'Publicar promoción',
    required = False,
    widget = forms.CheckboxInput(
      attrs = {
        'type':'checkbox',
        'id': 'CheckActive',
        'class':'form-check-input',
      }
    )
  )
  class Meta:
    model = Menu
    fields = ('menu_name','discount','dishes','brands','imagen','imagen_promo','active')
    exculde = ['restaurant','promo']
  
  def __init__(self, restaurant, *args, **kwargs):
    super(PromoForm, self).__init__(*args, **kwargs)
    self.fields['dishes'].queryset = Dish.objects.filter(restaurant=restaurant,active=True)
    self.fields['brands'].queryset = BrandOffice.objects.filter(restaurant=restaurant,active=True)
  
class ProfileFormTest(ModelForm):
  class Meta:
    model = Restaurant
    fields = '__all__'
    exculde = []