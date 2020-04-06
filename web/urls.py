from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cuentas/', views.cuentas, name='cuentas'),
    path('contacto/', views.contacto, name='contacto'),
    path('busqueda/', views.busqueda, name='busqueda'),
    path('busquedaDemandas/', views.busqueda_demandas, name='busqueda_demandas'),
    path('busquedaPalabra/', views.busqueda_palabra, name='busqueda_palabra'),
    path('resultadoPalabra/', views.resultado_palabra, name='resultado_palabra'),
    path('editar/(?P<num>\d+)', views.editar_serv, name='editar_serv'),
    path('editar/', views.edit, name='editar'),
    path('novedades/', views.novedades, name='novedades'),
    path('novedadesDemandas/', views.novedades_demandas, name='novedades_demandas'),
    path('nuevoArticulo/', views.nuevoArticulo, name='nuevo_articulo'),
    path('borrarArticulo/(?P<pk>\d+)', views.borrarArticulo, name='borrar_articulo'),
    path('resultado/(?P<cat>\w+)/(?P<subcat>\d+)', views.resultado, name='resultado'),
    path('resultadoDemandas/(?P<cat>\w+)/(?P<subcat>\d+)', views.resultado_demandas, name='resultado_demandas'),
]
