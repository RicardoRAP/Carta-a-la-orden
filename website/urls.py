from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Define las urls del sitio web

urlpatterns = [
  path('', views.Home, name="home"), # Url de la pagina principal
  path('restaurantes_encontrados/', views.ListRestaurants, name="lista-de-restaurantes"), # Url de la pagina de restaurantes encontrados
  path('restaurantes_encontrados/<str:name_param>/', views.RestaurantPage, name="sede-principal"), # Url de la pagina del restaurante 
  path('restaurantes_encontrados/<str:name_param>/<str:pk_param>/', views.RestaurantBrandPage, name="sucursal"), # Url de la pagina de la sucursal del restaurante
  path('pagando/', views.Checkout, name="pagando"), # Url de la pagina donde se paga

  path('inicio-de-sesion/', views.CommensalLogin, name="inicio-de-sesion"), # Url de la pagina de Inicio de sesión de los comensales
  path('registrarse/', views.CommensalRegister, name="registrarse"), # Url de la pagina donde se registran los comensales

  path('mantenimiento/', views.Maintenance, name="mantenimiento"),
  path('proximamente/', views.CommingSoon, name="proximamente"),

  path('afiliacion/', views.RestaurantHome, name="afiliacion"), # Url de la pagina principal de los restaurantes
  path('afiliacion/inicio-de-sesion/', views.RestaurantLogin, name="r-inicio-de-sesion"), # Url de la pagina de Inicio de sesión de los comensales
  path('cerrar-sesion/', views.Logout, name="cerrar-sesion"), # Url para cerrar sesion
  path('perfil/', views.RestaurantProfile, name="perfil"), # Url de la pagina del perfil del restaurante
  path('vista-previa/<str:name_param>/', views.RestaurantPreview, name="vista-sede-principal"), #Vista previa de la pagina de la sede principal
  
  path('perfil/sucursales/', views.RestaurantBrand, name="sucursales"), # Url de la pagina del las sucursales del restaurante
  path('perfil/sucursales/<str:pk_param>/', views.RestaurantUpdateBrand, name="editar-sucursal"), # Url de la pagina para editar una sucursal del restaurante
  path('vista-previa/<str:name_param>/<str:pk_param>/', views.RestaurantBrandPreview, name="vista-sucursal"), # Vista previa de la pagina de la sucursal

  path('perfil/menus/', views.RestaurantMenu, name="menus"), # Url de la pagina del las menus del restaurante
  path('perfil/menus/<str:pk_param>/', views.RestaurantUpdateMenu, name="editar-menu"), # Url de la pagina para editar un menu del restaurante

  path('perfil/platillos/', views.RestaurantDish, name="platillos"), # Url de la pagina del las platillos del restaurante
  path('perfil/platillos/<str:pk_param>/', views.RestaurantUpdateDish, name="editar-platillo"), # Url de la pagina para editar un platillo del restaurante

  path('perfil/promociones/', views.RestaurantPromo, name="promociones"), # Url de la pagina del las promociones del restaurante
  path('perfil/promociones/<str:pk_param>/', views.RestaurantUpdatePromo, name="editar-promo"), # Url de la pagina para editar una promocion del restaurante

  path('cambio_de_contraseña/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name="password_change"), # Url para el cambio de contraseña
  path('cambio_de_contraseña_hecho/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name="password_change_done"), # Url de mensaje de exito al cambiar de contraseña 

  path('reinicio_de_clave/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="reset_password"), # Url para el reinicio de la contraseña
  path('reinicio_de_clave/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name="password_reset_done"), # Url de mensaje de instrucciones a segir para el reiniciar la contraseña
  path('reinicio/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name="password_reset_confirm"), # Url con el formulario para reiniciar la contraseña
  path('reinicio/cambio_de_clave_completado/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"), # Url de mensaje de exito al reiniciar la contraseña 
]