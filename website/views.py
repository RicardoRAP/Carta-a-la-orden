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
import os
import time
import shutil
import urllib.parse

# Asignacion y Renderizado de las vistas

def Error404(request,exception):
  return render(request,'404.html')

def Home(request):
  menus = MenuBrand.objects.all().distinct("brand_id").values_list('brand_id', flat=True)
  if len(list(menus)) > 0:
    states = list(BrandOffice.objects.filter(id__in=menus, active=True, start_schedule__isnull=False, end_schedule__isnull=False).exclude(restaurant__profile_img='restaurants/profile.png').order_by('state').values_list('state', flat=True).distinct())
    alphabet = []
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
    messages.error(request,"No hay restaurantes disponibles")
  context = {"commensal":True,'alphabet':alphabet}
  return render(request,'home.html', context)