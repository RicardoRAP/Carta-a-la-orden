from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.

from .models import *
from .forms import *
from .decorators import *
from .filters import *
import os
import time
import shutil
import urllib.parse
import glob

# Asignacion y Renderizado de las vistas

def Error404(request,exception):
  return render(request,'404.html',status=404)

def CommingSoon(request):
  auth = True
  if not request.user.is_authenticated:
    auth = False
  context = {"auth":auth}
  return render(request, 'comming_soon.html',context)

def Maintenance(request):
  context = {}
  return render(request, 'maintenance.html', context)

def Home(request):
  menus = MenuBrand.objects.all().distinct("brand_id").values_list('brand_id', flat=True)
  states = list(BrandOffice.objects.filter(id__in=menus, active=True, start_schedule__isnull=False, end_schedule__isnull=False).exclude(restaurant__profile_img='restaurants/profile.png').order_by('state').values_list('state', flat=True).distinct())
  alphabet = []
  if len(menus) > 0:
    for state in states:
      if state[0] not in alphabet:
        alphabet.append(state[0])
      alphabet.append(state)
    if request.method == 'POST':
      state_select = request.POST.get('state')
      if state_select != None:
        full_address = request.POST.get('address')
        params = {
          'state_select':state_select,
          'full_address':full_address
        }
        new_url = urllib.parse.urlencode(params)
        return redirect('restaurantes_encontrados/?'+ new_url)
      else:
        messages.error(request,"Seleccione un Estado")
  else:
    alphabet = "No se encuentran restaurantes disponibles" 
  context = {'commensal':True, 'home':True,'alphabet':alphabet}
  return render(request,'home.html', context)

def ListRestaurants(request):
  menus = MenuBrand.objects.all().filter(menu__active=True).distinct("brand_id").values_list('brand_id', flat=True)
  brands = BrandOffice.objects.filter(id__in=menus, active=True, start_schedule__isnull=False, end_schedule__isnull=False).exclude(restaurant__profile_img='restaurants/profile.png')
  print(brands.values_list('state', flat=True).distinct())
  states = list(brands.order_by('state').values_list('state', flat=True).distinct())
  filter_brands = RestaurantsFilter(request.GET, queryset=brands)
  all_restaurant = filter_brands.qs
  alphabet = []
  for state in states:
    if state[0] not in alphabet:
      alphabet.append(state[0])
    alphabet.append(state)
  paginated_filtered = Paginator(all_restaurant, 3)
  page_number = request.GET.get('page')
  restaurant_page_obj = paginated_filtered.get_page(page_number)
  current_page = restaurant_page_obj.number
  total_pages = restaurant_page_obj.paginator.num_pages
  if current_page + 3 <= total_pages:
    if current_page == 1:
      pagination = range(current_page, current_page + 3)
      print(pagination, 1)
    else:
      pagination = range(current_page - 1, current_page + 3)
      print(pagination, 2)
  else:
    if current_page == total_pages:
      if total_pages - 2 == 0:
        pagination = range(1, total_pages + 1)
        print(pagination, 3)
      elif total_pages - 1 == 0:
        pagination = range(1, total_pages + 1)
      else:
        pagination = range(total_pages - 2, total_pages + 1)
        print(pagination, 4)
    elif current_page + 3 - total_pages == 1:
      pagination = range(total_pages - 3, total_pages + 1)
      print(pagination, 5)
    else:
      if total_pages - 2 == 0:
        pagination = range(1, total_pages + 1)
        print(pagination, 6)
      else:
        pagination = range(total_pages - 2, total_pages + 1)
        print(pagination, 7)
  context = {"commensal":True, 'alphabet':alphabet, 'filters':filter_brands, 'all_restaurant':all_restaurant, 'restaurant_page_obj':restaurant_page_obj, 'pagination':pagination}
  return render(request,'list_restaurants.html', context)

def Checkout(request):
  if request.method == "GET":
    name = request.GET.get("name")
    brand = request.GET.get("id")
    url = request.GET.get("url")
    menu_dish = request.GET.get("menu_dish")
    if name != None and brand != None and url != None and menu_dish != None:
      array_menu_dish = menu_dish.split(";")
      restaurant = BrandOffice.objects.get(id=brand)
      pick_up = restaurant.pick_up
      my_delivery = restaurant.my_delivery
      delivery = restaurant.delivery
      if delivery != "" and delivery != " ":
        others = delivery.split(",")
      else:
        others = ""
      o = []
      i = 3
      for other in others:
        o.append([other,i])
        i += 1
      menus = []
      dishes = []
      for m_d in array_menu_dish:
        if m_d != "":
          separated = m_d.split("_")
          menus.append(int(separated[0]))
          dishes.append(int(separated[1]))
      menudish = MenuDish.objects.filter(menu__in=menus,dish__in=dishes).order_by("menu")
      total = 0
      info = []
      for data in menudish:
        data_dish = data.get_data_dish()
        data_menu = data.get_data_menu()
        name_dish = data_dish.dish_name
        price_dish = data_dish.price
        promo_menu = data_menu.promo
        discount_menu = data_menu.discount
        if discount_menu != None and discount_menu != "" and promo_menu == True:
          discount = discount_menu / 100
          total += price_dish - (price_dish * discount)
          price = price_dish - (price_dish * discount)
        else:
          total += price_dish
          price = price_dish
        name_menu = data_menu.menu_name
        if len(info) == 0:
          info.append([name_menu,[[name_dish,price]]])
        else:
          row = 0
          final = False
          for j in info:
            if j[0] == name_menu:
              info[row][1].append([name_dish,price])
              final = True
              break
            row += 1
          if final == False:
            info.append([name_menu,[[name_dish,price]]])
      total = "{:.2f}".format(total)
    else:
      name = None
      pick_up = None
      my_delivery = None
      o = None
      info = None
      total = None 
      url = None
      return redirect('home')
  context = {'name':name, 'pick_up':pick_up, 'my_delivery':my_delivery, 'others':o, 'info':info, 'total':total,'url':url}
  return render(request,'checkout.html', context)

def RestaurantPage(request,name_param):
  principal = Restaurant.objects.get(name=name_param)
  promos = []
  menus = []
  restaurant = principal.brandoffice_set.get(is_restaurant=True)
  name = restaurant.restaurant.name
  img = restaurant.restaurant.profile_img
  delivery = restaurant.delivery
  pk_param = restaurant.id
  if delivery == "" or delivery == " ":
    others = None
  else:
    others = True
  all_menu = Menu.objects.filter(brands__id=pk_param, active=True).distinct()
  for sep in all_menu:
    array_dish_img = []
    for dish in sep.dishes.all().distinct():
      if sep.promo == True and sep.discount != None:
        discount = sep.discount / 100
        price_discount = dish.price - (dish.price * discount)
      else:
        price_discount = None
      array_dish_img.append([dish,price_discount,dish.imgdish_set.filter(order=0)[0], list(dish.imgdish_set.filter(select=True).values_list('img', flat=True))]) 
    if sep.promo == True:
      promos.append([sep,array_dish_img])
    else:
      menus.append([sep,array_dish_img])
  if request.method == "POST":
    names = request.POST.get("names")
    prices = request.POST.get("prices")
    if names == "" or prices == "":
      messages.error(request,"No seleccionado ningun platillo")
    else:
      params = {
        'name':name_param,
        'id':pk_param,
        'menu_dish':names,
        'url':request.get_full_path()
      }
      new_url = urllib.parse.urlencode(params)
      return redirect('/pagando/?' + new_url)
  context = {"commensal":True, 'restaurant':restaurant, 'name':name, 'img':img, 'others':others,'menus':menus, 'promos':promos}
  return render(request,'restaurant.html', context)

def RestaurantBrandPage(request,name_param,pk_param):
  promos = []
  menus = []
  restaurant = BrandOffice.objects.get(id=pk_param)
  name = restaurant.restaurant.name
  img = restaurant.restaurant.profile_img
  delivery = restaurant.delivery
  if delivery == "" or delivery == " ":
    others = None
  else:
    others = True
  all_menu = Menu.objects.filter(brands__id=pk_param, active=True).distinct()
  for sep in all_menu:
    array_dish_img = []
    for dish in sep.dishes.all().distinct():
      if sep.promo == True and sep.discount != None:
        discount = sep.discount / 100
        price_discount = dish.price - (dish.price * discount)
      else:
        price_discount = None
      array_dish_img.append([dish,price_discount,dish.imgdish_set.filter(order=0)[0], list(dish.imgdish_set.filter(select=True).values_list('img', flat=True))]) 
    if sep.promo == True:
      promos.append([sep,array_dish_img])
    else:
      menus.append([sep,array_dish_img])
  if request.method == "POST":
    names = request.POST.get("names")
    prices = request.POST.get("prices")
    if names == "" or prices == "":
      messages.error(request,"No seleccionado ningun platillo")
    else:
      params = {
        'name':name_param,
        'id':pk_param,
        'menu_dish':names,
        'url':request.get_full_path()
      }
      new_url = urllib.parse.urlencode(params)
      return redirect('/pagando/?' + new_url)
  context = {"commensal":True, 'restaurant':restaurant, 'name':name, 'img':img, 'others':others,'menus':menus, 'promos':promos}
  return render(request,'restaurant.html', context)

@unauthenticated_user
def CommensalLogin(request):
  context = {"commensal":True}
  return render(request,'commensal/login.html', context)

@unauthenticated_user
def CommensalRegister(request):
  context = {}
  return render(request,'commensal/register.html', context)

def RestaurantHome(request):
  auth = False
  restaurant = None
  if request.user.is_authenticated and not request.user.is_superuser:
    auth = True
    form = None
    restaurant = Restaurant.objects.get(id=request.user.id)
  else:
    form = CreateRestaurantForm()
    if request.method == 'POST':
      check = request.POST.get('checkbox')
      form = CreateRestaurantForm(request.POST)
      if form.is_valid():
        if check == "cheched":
          user = form.save(commit=False)
          user.full_address = user.state + ', ' + user.city + ', ' + user.parish
          user.save()
          email = form.cleaned_data.get('email')
          folder_user = email
          path_media = 'static/img/restaurants/' + str(folder_user)
          if not os.path.exists(path_media):
            os.mkdir(path_media)

          group = Group.objects.get_or_create(name='Restaurant')
          user.groups.add(group[0])

          BrandOffice.objects.create(restaurant=user, is_restaurant=True, brand_name="Sede principal", state=user.state, city=user.city, parish=user.parish, full_address=user.full_address, active=True)

          messages.success(request,"La cuenta ha sido creada exitosamente, con el siguente correo: " + email)
          return redirect('r-inicio-de-sesion')
        else:
          messages.error(request,"Acepte nuestros terminos y condiciones")
  context = {"commensal":False, 'auth':auth, 'form':form, 'restaurant':restaurant}
  return render(request,'restaurant/home.html', context)

@unauthenticated_user
def RestaurantLogin(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    if " " in email or " " in password:
      messages.error(request,"Hay un espacio en alguno de los campos")
    else:
      if email != "" and password != "":
        restaurant = authenticate(request, username=email, password=password)
        try:
          messages.error(request,restaurant.error_message)
        except:
          if restaurant is not None:
            login(request,restaurant)
            return redirect('perfil')
          else:
            messages.error(request,"No existe el usuario")
      else:
        messages.error(request,"Hay por lo menos un campo vacio")
  context = {"commensal":False}
  return render(request,'restaurant/login.html', context)

@login_required(login_url='r-inicio-de-sesion')
def Logout(request):
  group = request.user.groups.all()
  logout(request)
  print(group)
  if len(group) >= 1:
    if 'Restaurant' in group[0].name:
      return redirect('afiliacion')
  return redirect('home')

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantProfile(request):
  restaurant = Restaurant.objects.get(id=request.user.id)
  brand_restaurant = restaurant.brandoffice_set.filter(is_restaurant=True)
  username = restaurant.username
  phone = restaurant.phone
  start_schedule_r = restaurant.start_schedule
  end_schedule_r = restaurant.end_schedule
  pick_up_r = restaurant.pick_up
  my_delivery_r = restaurant.my_delivery
  delivery_r = restaurant.delivery
  old_img = restaurant.profile_img
  ex_delivery = restaurant.external_delivery
  ot_services = restaurant.others_services
  show = 'False'
  alarm = "on"
  if ex_delivery or ot_services:
    show = 'True'
  if username != None and phone != None and start_schedule_r != None and end_schedule_r != None and (pick_up_r or my_delivery_r or ex_delivery or ot_services) and old_img != None and str(old_img) not in "restaurants/profile.png":
    if (ex_delivery or ot_services) and delivery_r != "":
      if len(delivery_r.replace(" ","")) > 0:
        alarm = "off"
    else:
      alarm = "off"
  form = ProfileForm(instance=restaurant)
  if request.method == 'POST':
    form = ProfileForm(data=request.POST,files=request.FILES,instance=restaurant)
    start_schedule = request.POST.get("start_schedule")
    end_schedule = request.POST.get("end_schedule")
    if not (start_schedule >= end_schedule):
      if form.is_valid():
        if form.ValidateEmail(request.user.id):
          if form.NormalizeUsarname():
            profile = form.save(commit=False)
            brand_restaurant.update(
              start_schedule = request.POST.get("start_schedule"),
              end_schedule = request.POST.get("end_schedule"),
              pick_up = profile.pick_up,
              my_delivery = profile.my_delivery,
              external_delivery = profile.external_delivery,
              others_services = profile.others_services,
              delivery = request.POST.get("delivery"),
              state = request.POST.get("state"),
              city = request.POST.get("city"),
              parish = request.POST.get("parish"),
              avenue = request.POST.get("avenue"),
              street = request.POST.get("street"),
              full_address = request.POST.get("full_address")
            )
            profile.save()
            messages.success(request,"Los cambios se han guardado con éxito.")
            restaurant.refresh_from_db()
            if (request.FILES.get("profile_img") != None and "restaurants/profile.png" not in str(old_img)):
              try:
                os.remove(str(old_img.path))
              except:
                pass
            redirect("perfil")
          else:
            messages.error(request,"El formato del nombre de usuario es invalido. Recuerde que puede usar '_' , '.' y '&'.")
        else:
          messages.error(request,"Ese correo ya existe.")
      else:
        messages.error(request,"Ha ocurrido un error.")
        print(form.errors)
    else:
      messages.error(request,"El comienzo del horario no puede ser mayor o igual al final del horario.")
  photo = str(restaurant.profile_img)
  img = 'None'
  if photo != 'None' and 'restaurant/profile.png' not in photo:
    img = os.path.join('img', photo)
  context = {"commensal":False, 'tab':'profile', 'form':form, 'img':img, 'show':show, 'alarm':alarm}
  return render(request,'restaurant/profile.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantPreview(request,name_param):
  principal = Restaurant.objects.get(name=name_param)
  promos = []
  menus = []
  restaurant = principal.brandoffice_set.get(is_restaurant=True)
  name = restaurant.restaurant.name
  img = restaurant.restaurant.profile_img
  delivery = restaurant.delivery
  pk_param = restaurant.id
  if delivery == "" or delivery == " ":
    others = None
  else:
    others = True
  all_menu = Menu.objects.filter(brands__id=pk_param, active=True).distinct()
  for sep in all_menu:
    array_dish_img = []
    for dish in sep.dishes.all().distinct():
      if sep.promo == True and sep.discount != None:
        discount = sep.discount / 100
        price_discount = dish.price - (dish.price * discount)
      else:
        price_discount = None
      array_dish_img.append([dish,price_discount,dish.imgdish_set.filter(order=0)[0], list(dish.imgdish_set.filter(select=True).values_list('img', flat=True))]) 
    if sep.promo == True:
      promos.append([sep,array_dish_img])
    else:
      menus.append([sep,array_dish_img])
  context = {"commensal":True, 'restaurant':restaurant, 'name':name, 'img':img, 'others':others,'menus':menus, 'promos':promos}
  return render(request,'restaurant/preview.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantBrand(request):
  # Crear Sucursales
  AddBrandFormSet = inlineformset_factory(
    parent_model = Restaurant, 
    model = BrandOffice, 
    form = BrandForm,
    formset = CustomInlineFormSet,
    help_texts = None,
    extra = 1,
    can_delete = False,
    max_num = 1,
  )
  restaurant = Restaurant.objects.get(id=request.user.id)
  addform = AddBrandFormSet(queryset=BrandOffice.objects.none(), instance=restaurant)
  if request.method == 'POST':
    addform = AddBrandFormSet(data=request.POST, instance=restaurant)
    if addform.is_valid():
      addform.save()
      time.sleep(1)
      restaurant.refresh_from_db()
      return redirect('sucursales')
    else:
      messages.error(request,"Error")
  brands = restaurant.brandoffice_set.filter(is_restaurant=False)
  brands_filter = BrandFilter(request.GET, queryset=brands)
  brands = brands_filter.qs
  brand_restaurant = restaurant.brandoffice_set.filter(is_restaurant=True)
  menus = Menu.objects.filter(brands__id=brand_restaurant[0].id, promo=False)
  promos = Menu.objects.filter(brands__id=brand_restaurant[0].id, promo=True)
  all_menus = Menu.objects.filter(brands__id=brand_restaurant[0].id)
  unque_dish = []
  for r_menudish in all_menus:
    md = MenuDish.objects.filter(menu=r_menudish.id)
    for d in md:
      if d.dish.id not in unque_dish:
        unque_dish.append(d.dish.id)
  sede_info = [menus.count(), len(unque_dish), promos.count()]
  info = []
  for brand in brands:
    brand_all_menus = Menu.objects.filter(brands=brand.id).distinct()
    amount_menus = brand_all_menus.filter(promo=False).count()
    amount_promos = brand_all_menus.filter(promo=True).count()
    distint_dishes = []
    for brand_menu_dishes in brand_all_menus:
      brand_dishes = brand_menu_dishes.menudish_set.distinct('dish').all()
      for bdishes in brand_dishes:
        if bdishes.dish.id not in distint_dishes:
          distint_dishes.append(bdishes.dish.id)
    info.append([amount_menus,len(distint_dishes),amount_promos, brand])
  amount = brands.count()
  limit = False
  auth = True
  if restaurant.plan == "Plan Básico":
    if amount >= 3:
      limit = True
  elif restaurant.plan == "Plan Plata":
    if amount >= 6:
      limit = True
  elif restaurant.plan == "Plan Oro":
    if amount >= 11:
      limit = True
  if limit:
    addform = None
  context = {"commensal":False, 'update':False, 'auth':auth, 'limit':limit, 'tab':'brand', 'brands':info, 'filters':brands_filter, 'add_brand':addform, 'info_sede':sede_info}
  return render(request,'restaurant/brand-office.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantUpdateBrand(request, pk_param):
  # Editar sucursal
  brand = BrandOffice.objects.get(id=pk_param)
  ex_delivery = brand.external_delivery
  ot_services = brand.others_services
  full = brand.full_address
  show = 'False'
  if ex_delivery or ot_services:
    show = 'True'
  form = BrandForm(instance=brand)
  if request.method == 'POST':
    if 'brand_name' in request.POST:
      form = BrandForm(request.POST, instance=brand)
      if form.is_valid():
        form.save()
        time.sleep(1)
        brand.refresh_from_db()
        return redirect('sucursales')
    elif 'Delete' in request.POST:
      brand.delete()
      time.sleep(1)
      return redirect('sucursales')
  context = {"commensal":False, 'update':True, 'tab':'brand', 'form':form, 'show':show, 'full':full,'item':brand}
  return render(request,'restaurant/update-brand-office.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantBrandPreview(request,name_param,pk_param):
  promos = []
  menus = []
  restaurant = BrandOffice.objects.get(id=pk_param)
  name = restaurant.restaurant.name
  img = restaurant.restaurant.profile_img
  delivery = restaurant.delivery
  if delivery == "" or delivery == " ":
    others = None
  else:
    others = True
  all_menu = Menu.objects.filter(brands__id=pk_param, active=True).distinct()
  for sep in all_menu:
    array_dish_img = []
    for dish in sep.dishes.all().distinct():
      if sep.promo == True and sep.discount != None:
        discount = sep.discount / 100
        price_discount = dish.price - (dish.price * discount)
      else:
        price_discount = None
      array_dish_img.append([dish,price_discount,dish.imgdish_set.filter(order=0)[0], list(dish.imgdish_set.filter(select=True).values_list('img', flat=True))]) 
    if sep.promo == True:
      promos.append([sep,array_dish_img])
    else:
      menus.append([sep,array_dish_img])
  context = {"commensal":True, 'restaurant':restaurant, 'name':name, 'img':img, 'others':others,'menus':menus, 'promos':promos}
  return render(request,'restaurant/preview.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantMenu(request):
  restaurant = Restaurant.objects.get(id=request.user.id)
  alarm = "on"
  dishes = restaurant.dish_set.all()
  if len(dishes) > 0:
    alarm = "off"
  # Crear Menu
  if request.method == 'POST':
    form = MenuForm(request.user.id, data=request.POST, files=request.FILES)
    if form.is_valid:
      select_brand = request.POST.getlist("brands")
      img = request.FILES.get('imagen')
      if len(select_brand) > 0:
        f = form.save(commit=False)
        f.restaurant = restaurant
        if img != None:
          f.imagen = img
        f.save()
        form.save_m2m()
        restaurant.refresh_from_db()
        return redirect('menus')
      else:
        messages.error(request,"Selecione por lo menos una sucursal o la sede principal.")
    else:
      messages.error(request,form.errors)
  else:
    form = MenuForm(request.user.id)
  menus = restaurant.menu_set.filter(promo=False)
  menu_filter = MenuFilter(request.GET, queryset=menus, current_user=request)
  menus = menu_filter.qs
  context = {"commensal":False, 'update':False, 'tab':'menu', 'alarm':alarm, 'menus':menus, 'filters':menu_filter, 'form':form}
  return render(request,'restaurant/menu.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantUpdateMenu(request, pk_param):
  menu = Menu.objects.get(id=pk_param)
  restaurant = menu.restaurant
  # Editar Menu
  print()
  form = MenuForm(restaurant, instance=menu)
  if request.method == 'POST':
    if 'menu_name' in request.POST:
      form = MenuForm(restaurant, data=request.POST, files=request.FILES, instance=menu)
      if form.is_valid:
        select_brand = request.POST.getlist("brands")
        if len(select_brand) > 0:
          old_img = str(menu.imagen.path)
          form.save()
          if (old_img != str(menu.imagen.path)):
            try:
              os.remove(old_img)
            except:
              pass
          return redirect('menus')
        else:
          messages.error(request,"Selecione por lo menos una sucursal o la sede principal.")
      else:
        messages.error(request,"Error")
    elif 'Delete' in request.POST:
      old_img = menu.imagen
      menu.delete()
      if (old_img != None and 'icon/front-page.png' not in str(old_img)):
        try:
          os.remove(str(old_img.path))
        except:
          pass
      time.sleep(1)
      return redirect('menus')
  context = {"commensal":False, 'update':True, 'tab':'menu', 'form':form, 'item':menu}
  return render(request,'restaurant/update-menu.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantDish(request):
  # Crear platillos
  restaurant = Restaurant.objects.get(id=request.user.id)
  addform = DishForm()
  addimgform = MultipleImgForm()
  if request.method == 'POST':
    addform = DishForm(request.POST)
    files = request.FILES.getlist("img")
    if addform.is_valid():
      if len(files) >= 2:
        f = addform.save(commit=False)
        f.restaurant = request.user.restaurant
        f.save()
        j = 0
        for i in files:
          ImgDish.objects.create(dish=f,img=i,select=True,order=j,folder=f.id)
          j += 1
        time.sleep(1)
        restaurant.refresh_from_db()
        return redirect('platillos')
      else:
        messages.error(request,"Debe seleccionar por lo menos 2 imagenes")
    else:
      messages.error(request,addform.errors)
  dishes = restaurant.dish_set.all()
  dish_filter = DishFilter(request.GET, queryset=dishes)
  dishes = dish_filter.qs
  dishes_imgs = []
  for d in dishes:
    dishes_imgs.append([d,d.imgdish_set.all().filter(order=0)[0]])
  context = {"commensal":False, 'update':False, 'tab':'dish', 'dishes':dishes_imgs, 'filters':dish_filter,'add_dish':addform, 'add_img':addimgform}
  return render(request,'restaurant/dish.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantUpdateDish(request, pk_param):
  # Editar sucursal
  dish = Dish.objects.get(id=pk_param)
  form = DishForm(instance=dish)
  all_dish_imgs = dish.imgdish_set.all()
  dish_imgs = all_dish_imgs.filter(select=True)
  if request.method == 'POST':
    if 'updateSelect' in request.POST:
      update_img = request.POST.get("updateSelect")
      newselect = str(update_img)
      newselect = newselect.split(",")
      if len(newselect) >= 2:
        dish_imgs.update(select=False,order=None)
        j = 0
        for updateselect in newselect:
          separed_info = updateselect.split("_")
          img_id = separed_info[0]
          all_dish_imgs.filter(id=int(img_id)).update(select=True,order=j)
          j += 1
        dish.refresh_from_db()
        messages.success(request,"Se han actualizado las imagenes exitosamente")
        redirect('platillos/' + str(pk_param) + "/")
      else:
        messages.error(request,"Debe seleccionar por lo menos 2 imagenes","error_img")
    if 'upload-img' in request.POST:
      files = request.FILES.getlist("upload-img")
      if len(files) > 0:
        all_img_order = all_dish_imgs.order_by('-order')
        last_order = all_img_order[0].order
        k = int(last_order) + 1
        for m in files:
          ImgDish.objects.create(dish=dish,img=m,select=True,order=k,folder=pk_param)
          k += 1
        dish.refresh_from_db()
        messages.success(request,"Se han montado y seleccionado las imagenes exitosamente")
      else:
        messages.error(request,"Debe seleccionar por lo menos una imagen","error_upload_img")
    if 'dish_name' in request.POST:
      form = DishForm(request.POST, instance=dish)
      if form.is_valid():
        f = form.save(commit=False)
        date_now = timezone.now()
        f.date_modify = timezone.localtime(date_now).strftime("%Y-%m-%d %T")
        f.save()
        time.sleep(1)
        dish.refresh_from_db()
        return redirect('platillos')
    elif 'Delete' in request.POST:
      folder = dish_imgs[0].folder
      email = Restaurant.objects.get(id=dish.restaurant.id).email
      menus_dish = MenuDish.objects.filter(dish=pk_param)
      m = []
      if len(menus_dish) > 0:
        for menu_d in menus_dish:
          m.append(menu_d.menu.id)
        menus_dishes = MenuDish.objects.filter(menu__in=m).order_by("menu")
        exclude_dish = menus_dishes.exclude(dish=pk_param)
        e = []
        for exclu_dish in exclude_dish:
          e.append(exclu_dish.menu.id)
        for m_d in menus_dishes:
          if m_d not in exclude_dish and m_d.menu.id not in e:
            menu_delete = dish.restaurant.menu_set.get(id=m_d.menu.id)
            old_img = menu_delete.imagen
            menu_delete.delete()
            if (old_img != None and 'icon/front-page.png' not in str(old_img)):
              try:
                os.remove(str(old_img.path))
              except:
                pass
      dish.delete()
      time.sleep(1)
      folder_path = os.path.join("./static/img/restaurants/", str(email) + '/dishes/' + str(folder) + '/')
      try:
        shutil.rmtree(folder_path)
      except:
        pass
      time.sleep(1)
      return redirect('platillos')
  context = {"commensal":False, 'update':True, 'tab':'dish', 'form':form,'dish_imgs':dish_imgs,'item':dish, 'all_imgs':all_dish_imgs}
  return render(request,'restaurant/update-dish.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantPromo(request):
  restaurant = Restaurant.objects.get(id=request.user.id)
  alarm = "on"
  dishes = restaurant.dish_set.all()
  if len(dishes) > 0:
    alarm = "off"
  # Crear Promo
  if request.method == 'POST':
    form = PromoForm(request.user.id, data=request.POST, files=request.FILES)
    if form.is_valid:
      select_brand = request.POST.getlist("brands")
      if len(select_brand) > 0:
        img = request.FILES.get('imagen')
        img_promo =  request.FILES.get('imagen_promo')
        f = form.save(commit=False)
        f.restaurant = restaurant
        f.promo = True
        if img != None:
          f.imagen = img
        f.imagen_promo = img_promo
        f.save()
        form.save_m2m()
        restaurant.refresh_from_db()
        return redirect('promociones')
      else:
        messages.error(request,"Selecione por lo menos una sucursal o la sede principal.")
    else:
      messages.error(request,form.errors)
  else:
    form = PromoForm(request.user.id)
  promos = restaurant.menu_set.filter(promo=True)
  promos_filter = PromoFilter(request.GET, queryset=promos, current_user=request)
  promos = promos_filter.qs
  context = {"commensal":False, 'update':False, 'tab':'promo', 'alarm':alarm, 'promos':promos, 'filters':promos_filter, 'form':form}
  return render(request,'restaurant/promo.html', context)

@login_required(login_url='r-inicio-de-sesion')
@allowed_users(allowed_roles=['Restaurant'])
def RestaurantUpdatePromo(request, pk_param):
  promo = Menu.objects.get(id=pk_param)
  restaurant = promo.restaurant
  # Editar Promo
  if request.method == 'POST':
    print(request.POST)
    if 'menu_name' in request.POST:
      form = PromoForm(restaurant, request.POST, request.FILES, instance=promo)
      if form.is_valid:
        old_img = str(promo.imagen.path)
        old_promo_img = str(promo.imagen_promo.path)
        form.save()
        if (old_img != str(promo.imagen.path) and old_img != None):
          try:
            os.remove(old_img)
          except:
            pass
        if (old_promo_img != str(promo.imagen_promo.path) and old_promo_img != None):
          try:
            os.remove(old_promo_img)
          except:
            pass
        return redirect('promociones')
      else:
        messages.error(request,"Error")
    elif 'Delete' in request.POST:
      old_img = promo.imagen
      old_promo_img = str(promo.imagen_promo.path)
      promo.delete()
      if (old_img != None and 'icon/front-page.png' not in str(old_img)):
        try:
          os.remove(str(old_img.path))
        except:
          pass
      if (old_promo_img != None):
        try:
          os.remove(old_promo_img)
        except:
          pass
      time.sleep(1)
      return redirect('promociones')
  else:
    form = PromoForm(restaurant, instance=promo)
  context = {"commensal":False, 'update':True, 'tab':'promo', 'form':form, 'item':promo}
  return render(request,'restaurant/update-promo.html', context)
