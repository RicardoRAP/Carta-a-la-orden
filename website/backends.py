from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
  def authenticate(self, request, username=None, password=None, **kwargs):
    class Error_auth:
      def __init__(self, message):
        self.error_message = message

    UserModel = get_user_model()
    find = False
    try:
      user = UserModel.objects.get(email=username)
      find = True
    except UserModel.DoesNotExist:
      try:
        user = UserModel.objects.get(username=username)
        find = True
      except UserModel.DoesNotExist:
        return Error_auth("No se ha encontrado el Email o el Nombre de usuario")
    if find:
      if user.check_password(password):
        return user
      else:
        return Error_auth("Contraseña incorrecta")
    return Error_auth("Problemas en la autenticacíon, actualice la pagina e intente nuevamente")