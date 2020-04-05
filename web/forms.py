# -*- coding: utf-8 -*-
from django import forms
from web.models import *
from django.contrib.auth.models import User

#### REGISTRO SMS FORM ####

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False, label='Nombre')
    last_name = forms.CharField(required=False, label='Apellidos')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_emai(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

class SocioEditForm(forms.ModelForm):
    telefono = forms.CharField(required=False, label=u'Teléfono')
    pueblo = forms.CharField(required=False)
    mostrar_telefono = forms.BooleanField(required=False, label=u'Mostrar Teléfono')
    mostrar_email = forms.BooleanField(required=False)

    class Meta:
        model = Socio
        fields = ('pueblo', 'telefono', 'mostrar_telefono', 'mostrar_email')

class ArticuloForm(forms.ModelForm):

    class Meta:
       model = Articulo
       exclude = ['user', 'activo']
