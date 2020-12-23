from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio,name='index'),
    path('permisos/', views.permisos, name="permisos"),
    path('reporteAgente/', views.reporteAgente.as_view(), name='reporteAgente'),
    path('reporteAgenteACargo/', views.reporteAgentesACargo.as_view(), name="reporteAgenteACargo"),
    path('informacion/', views.informacion, name='informacion'),
    path('homeAgente/', views.homeAgente.as_view(), name='homeAgente'),
    path('new/',views.permiso_new, name='permiso_new'),
    path('<int:pk>/marca/<int:tpermiso>',views.PermisoMarcaView.as_view(),name='permiso_marca'),
    path('<int:pk>/ver/<int:tpermiso>',views.PermisoVerView.as_view(),name='permiso_ver'),
    path('<int:pk>/edit/<int:tpermiso>',views.PermisoEditView.as_view(),name='permiso_edit'),
    path('<int:pk>/delete/<int:tpermiso>',views.PermisoDeleteView.as_view(),name='permiso_delete'),
    path('autoriza_list',views.permiso_aut_list.as_view(),name='permiso_aut_list'),
    path('acepta_list',views.permiso_acepta_list.as_view(),name='permiso_acepta_list'),
    path('<int:pk>/',views.PermisoDetailView.as_view(),name='detail'),
    path('newnew/<int:tpermiso>/',views.PermisoNewView.as_view(),name='newnew'),
]