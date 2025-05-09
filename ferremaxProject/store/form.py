
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class InicioSesionForm():
   email = forms.EmailField()
   password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
 


class RegistroUsuarioForm(UserCreationForm):
   email = forms.EmailField()
   password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
   password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)

   class Meta: 
    model = User
    fields = ['username','email','password1','password2']
    help_texts = {k:"" for k in fields }


class CantidadProductoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, initial=1, label='Cantidad')

class CantidadProductoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')