# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from web.utils import get_upload_path
from web.utils import get_upload_path_articulo
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

  
# SOCIO extensión de USER

class Socio(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  numsocio = models.IntegerField(blank=True)
  pueblo = models.CharField(max_length=200, blank=True)
  telefono = models.CharField(max_length=30, blank=True)
  avatar = models.ImageField(upload_to='avatares', blank=True)
  mostrar_telefono = models.BooleanField(default=True)
  mostrar_email = models.BooleanField(default=True)
  
  class Meta:
    ordering = ['numsocio',]

  def __str__(self):
    return self.numsocio

# MANDAR CORREO de BIENVENIDA

#def mandar_mensaje_bienvenida(sender, instance, created,  **kwargs):
#  if instance.email:
#    texto = get_template('mail_bienvenida.txt')
#    d = Context({ 'username': instance.username })
#    text_content = texto.render(d)
#    subject = 'Bienvenid@ a Tiempo al Tiempo' 
#    msg = EmailMultiAlternatives(subject, text_content, 'tiempoaltiempotietar@gmail.com', [instance.email])
#    msg.send()

#models.signals.post_save.connect(mandar_mensaje_bienvenida, sender=User)

class SubCategoriaArticulo(models.Model):
  nombre = models.CharField(max_length=100)
  def __str__(self):
    return self.nombre

  class Meta:
    ordering = ['nombre']

# ARTICULOS

class Articulo(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  tipo = models.CharField(max_length=12, choices=(
      ('oferta', 'Oferta'),
      ('demanda', 'Demanda'),
    )
  )
  categoria = models.CharField(max_length=30, choices = (
      ('bienes_alq', 'Bienes Alquiler'),
      ('bienes_comp', 'Bienes Compra'),
      ('clases', 'Clases'),
      ('servicios', 'Servicios')
    )
  )
  subcategoria = models.ForeignKey(SubCategoriaArticulo, on_delete=models.CASCADE)
  nombre = models.CharField(max_length=100) 
  descripcion = models.CharField(max_length=300, blank=True)
  activo = models.BooleanField(default=True)
  fecha = models.DateField(auto_now_add=True)
  imagen = models.ImageField(upload_to=get_upload_path_articulo, blank=True, default="")
  imagen_thumbnail = ImageSpecField(source = 'imagen',
					   processors = [ResizeToFill(60, 60)],
					   format = 'JPEG',
					   options = {'quality': 95})

  def __str__(self):
    return self.nombre

  def delete(self, *args, **kwargs):
    if self.cuenta_set.count() > 0:
      self.activo = False
      self.save()
    else:
      super(Articulo, self).delete(*args, **kwargs)

#CUENTAS

class Cuenta(models.Model):
  comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comprador')
  vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendedor')
  horas = models.FloatField()
  articulo = ChainedForeignKey(Articulo, chained_field="vendedor", chained_model_field="user", auto_choose=True, blank=True)
  fecha = models.DateField()
  imagen = models.ImageField(upload_to=get_upload_path, blank=True, default="")
  imagen_thumbnail = ImageSpecField(source = 'imagen',
					   processors = [ResizeToFill(60, 60)],
					   format = 'JPEG',
					   options = {'quality': 95})
  corregido = models.CharField(max_length=10)

  class Meta:
    ordering = ['-fecha']
  
  def __str__(self):
    return '%s horas de %s a %s'% (self.horas, self.comprador, self.vendedor)

# CORREOS de CUENTAS

def mandar_mensaje(sender, instance, created, **kwargs):
  if created:
    texto = u'''Hola, 

Os informamos que a fecha %s ha quedado registrado un intercambio entre %s(%s) y %s(%s) por valor de %s horas a favor de %s. Puedes comprobar el movimiento en la página de TaT http://tiempoaltiempo.org

Saludos y gracias por mantener vivo Banco del Tiempo Valle del Tiétar''' % (instance.fecha.strftime('%d/%m'), instance.comprador.first_name, instance.comprador.username, instance.vendedor.first_name, instance.vendedor.username, instance.horas, instance.vendedor.first_name)
    send_mail('Aviso intercambio TaT %s/%s' % (instance.comprador.username, instance.vendedor.username), texto, 'bartulo@gmail.com', [instance.vendedor.email, instance.comprador.email])

# CORREO para cuando se produce un error en el registro de cuentas

def mandar_error_cuenta(sender, instance,  **kwargs):
    texto = get_template('mail_error_cuenta.txt')
    d = Context({ 'horas': instance.horas, 'comprador': instance.comprador.first_name, 'num_comprador': instance.comprador.username, 'vendedor':instance.vendedor.first_name, 'num_vendedor': instance.vendedor.username })
    text_content = texto.render(d)
    subject = 'Error en registro de intercambio TaT %s/%s' % (instance.comprador.username, instance.vendedor.username)  
    msg = EmailMultiAlternatives(subject, text_content, 'tiempoaltiempotietar@gmail.com', [instance.vendedor.email, instance.comprador.email])
    msg.send()

models.signals.post_save.connect(mandar_mensaje, sender=Cuenta)
models.signals.pre_delete.connect(mandar_error_cuenta, sender=Cuenta)

# ADMINISTRADORES 

class Admin(models.Model):
  fecha = models.DateField()
  user = models.ManyToManyField(User, blank=True)
  
  def __str__(self):
    return '%s administradores - %s' % (self.adminind_set.all().count(),self.fecha.strftime("%d/%m/%Y"))

# ADMINISTRADORES individuales.

class AdminInd(models.Model):
  administrador = models.ForeignKey(User, on_delete=models.CASCADE)
  horas = models.FloatField()
  entrada = models.ForeignKey(Admin, on_delete=models.CASCADE)

