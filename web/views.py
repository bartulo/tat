from django.shortcuts import render
from web.models import *
from web.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
#from django.core.urlresolvers import reverse
#from django.contrib.auth.views import password_reset, password_reset_confirm
from django.views.generic.edit import CreateView

from django.template import loader
from django.db.models import Sum

def calculate_horas(current_user):
  hpos = current_user.vendedor.aggregate(t=Sum('horas'))['t']
  hpos = hpos if hpos != None else 0
  hneg = current_user.comprador.aggregate(t=Sum('horas'))['t']
  hneg = hneg if hneg != None else 0
  adminpos = current_user.adminind_set.aggregate(t=Sum('horas'))['t']
  adminpos = adminpos if adminpos != None else 0
  adminneg = 0
  for i in Admin.objects.filter(user=current_user):
    num_horas = i.adminind_set.aggregate(t=Sum('horas'))['t']
    num_socios = i.user.count()
    adminneg += num_horas/num_socios
  total = hpos + adminpos - hneg - adminneg
  return [hpos, hneg, adminpos, adminneg, total]

class LoginViewMod(LoginView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    current_user = self.request.user
    if current_user.is_authenticated:
      
      horas = calculate_horas(current_user)

      context.update({
        'h_pos': horas[0],
        'h_neg': horas[1],
        'admin_pos': horas[2],
        'admin_neg': horas[3],
        'total': horas[4],
        })
    return context
        
        ### BUSQUEDA POR PALABRA ###
def busqueda_palabra(request):
  if request.method == 'POST':
    palabra = request.POST['palabra']
    tipo = request.POST['tipo']
    art = Articulo.objects.filter(nombre__icontains = palabra).filter(tipo = request.POST['tipo']).distinct('nombre')
    return render(request, 'resultado_palabra.html', {'nombre': 'Resultados', 'articulo': art, 'post': request.POST, 'tipo': tipo})

def resultado_palabra(request):
  if request.method == 'POST':
    palabra = request.POST['palab']
    art = Articulo.objects.filter(nombre__icontains = palabra).filter(tipo = request.POST['tipo'])
    return render(request, 'articulo.html', {'nombre': palabra, 'articulo': art})

def contacto(request):
  return render(request, 'contacto.html')

def novedades(request):
  art = Articulo.objects.filter(tipo = 'oferta').order_by('-fecha')[:10]
  context = {
          'arts': art,
          'tipo': 'Ofertas',
          }
  return render(request, 'novedades.html', context)

def novedades_demandas(request):
  art = Articulo.objects.filter(tipo = 'demanda').order_by('-fecha')[:10]
  return render(request, 'novedades.html', {'arts':art, 'tipo':'Demandas'} )

@login_required
def borrarArticulo(request, pk):
  art = Articulo.objects.get(pk = pk)
  art.delete()
  return HttpResponseRedirect('/')
	
@login_required
def nuevoArticulo(request):
  if request.method == 'POST':
    form = ArticuloForm(request.POST, request.FILES)
    if form.is_valid():
      art = form.save(commit=False)
      art.user = request.user
      art.save()
      return HttpResponseRedirect('/')
  else:
    form = ArticuloForm()
    return render(request, 'nuevo_articulo.html', {'form':form} )
  

@login_required
def edit(request):
   # This body will only run if the user is logged in
   # and the current logged in user will be in request.user
   if request.method == 'POST':
        # formulario enviado
     user_form = UserEditForm(request.POST, instance = request.user)
     perfil_form = SocioEditForm(request.POST, instance = request.user.socio)

     if user_form.is_valid() and perfil_form.is_valid():
            # formulario validado correctamente
        user_form.save()
        perfil_form.save()
        return HttpResponseRedirect('/')

   else:
     edit_form = UserEditForm(instance=request.user)
     socio_form = SocioEditForm(instance=request.user.socio)
     ofertas = request.user.articulo_set.all().filter(tipo='oferta')
     demandas = request.user.articulo_set.all().filter(tipo='demanda')
     return render(request, 'editar.html',
                             {'form':edit_form, 'form_socio':socio_form, 'ofertas':ofertas, 'demandas':demandas})

@login_required
def editar_serv(request, num):
   # This body will only run if the user is logged in
   # and the current logged in user will be in request.user
   if request.method == 'POST':
        # formulario enviado
     art = Articulo.objects.get(pk=num)
     art_form = ArticuloForm(request.POST, request.FILES, instance = art)

     if art_form.is_valid():
            # formulario validado correctamente
        art_form.save()
        return HttpResponseRedirect('/')

   else:
     art = Articulo.objects.get(pk=num)
     art_form = ArticuloForm(instance=art)
     return render(request, 'editar_art.html',
                             {'nombre': art.nombre, 'art_form':art_form})

@login_required
def cuentas(request):
  user = request.user
  horas = calculate_horas(user)
  return render(request, 'cuentas.html', {'horas_pos': horas[0], 'horas_neg': horas[1]})

def busqueda(request):
  def filtro(cat):
    return SubCategoriaArticulo.objects.filter(articulo__tipo = 'oferta', articulo__categoria = cat).distinct()
  return render(request, 'busqueda.html', {'bienes_comp':filtro('bienes_comp'),'bienes_alq':filtro('bienes_alq'),'clases':filtro('clases'),'servicios':filtro('servicios')})

def busqueda_demandas(request):
  def filtro(cat):
    return SubCategoriaArticulo.objects.filter(articulo__tipo = 'demanda', articulo__categoria = cat).distinct()
  return render(request, 'busqueda_demandas.html', {'bienes_comp':filtro('bienes_comp'),'bienes_alq':filtro('bienes_alq'),'clases':filtro('clases'),'servicios':filtro('servicios')})

def resultado(request, cat, subcat):
  if request.method == 'POST':
    articulo = request.POST.get("nombre")
    categoria = request.POST.get("categoria")
    art = Articulo.objects.filter(nombre = articulo, categoria = categoria)
    return render(request, 'articulo.html', {'nombre': articulo, 'articulo': art})
  else:
    subc = SubCategoriaArticulo.objects.get(pk = subcat)
    art = Articulo.objects.filter(tipo = 'oferta', categoria = cat, subcategoria = subc, activo = True).distinct('nombre')
    return render(request, 'resultado.html', {'cat': art[0].get_categoria_display().upper(), 'subcat': subc.nombre, 'articulo': art})

def resultado_demandas(request, cat, subcat):
  if request.method == 'POST':
    articulo = request.POST.get("nombre")
    categoria = request.POST.get("categoria")
    art = Articulo.objects.filter(nombre = articulo, categoria = categoria)
    return render(request, 'articulo.html', {'nombre': articulo, 'articulo': art})
  else:
    subc = SubCategoriaArticulo.objects.get(pk = subcat)
    art = Articulo.objects.filter(tipo = 'demanda', categoria = cat, subcategoria = subc, activo = True).distinct('nombre')
    return render(request, 'resultado.html', {'cat': art[0].get_categoria_display().upper(), 'subcat': subc.nombre, 'articulo': art})

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, uidb64=uidb64, token=token, post_reset_redirect=reverse('login'))


def reset(request):
    return password_reset(request, post_reset_redirect=reverse('login')) 

