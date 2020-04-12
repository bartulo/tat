from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.LoginViewMod.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
#    path('passwordReset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#    path('passwordResetConfirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset'),
    path('passwordResetDone/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('cuentas/', views.cuentas, name='cuentas'),
    path('contacto/', views.contacto, name='contacto'),
    path('busqueda/', views.busqueda, name='busqueda'),
    path('busquedaDemandas/', views.busqueda_demandas, name='busqueda_demandas'),
    path('busquedaPalabra/', views.busqueda_palabra, name='busqueda_palabra'),
    path('resultadoPalabra/', views.resultado_palabra, name='resultado_palabra'),
    path('editar/<num>', views.editar_serv, name='editar_serv'),
    path('editar/', views.edit, name='editar'),
    path('novedades/', views.novedades, name='novedades'),
    path('novedadesDemandas/', views.novedades_demandas, name='novedades_demandas'),
    path('nuevoArticulo/', views.nuevoArticulo, name='nuevo_articulo'),
    path('borrarArticulo/<pk>', views.borrarArticulo, name='borrar_articulo'),
    path('resultado/<cat>/<subcat>', views.resultado, name='resultado'),
    path('resultadoDemandas/<cat>/<subcat>', views.resultado_demandas, name='resultado_demandas'),
]
