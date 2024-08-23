from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ProductoListView,
    ProductoDetailView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoDeleteView,
    SucursalListView,
    SucursalCreateView,
    SucursalDeleteView,
    SucursalUpdateView,
    SucursalDetailView,
    DepositosListView,
    DepositoCreateView,
    DepositoUpdateView,
    DepositoDeleteView,
    DepositoDetailView,
    ProductoXDepositoListView,
    ProductoXDepositoCreateView,
    ProductoXDepositoUpdateView,
    ProductoXDepositoDeleteView,
    ProductoXDepositoDetailView,

)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/detail/<int:pk>/',ProductoDetailView.as_view(), name='producto_detail'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
    path('sucursales/',SucursalListView.as_view(),name='sucursal_list'),
    path('sucursales/nuevo/',SucursalCreateView.as_view(),name='sucursal_create'),
    path('sucursales/eliminar/<int:pk>',SucursalDeleteView.as_view(),name='sucursal_delete'),
    path('sucursales/editar/<int:pk>',SucursalUpdateView.as_view(),name='sucursal_update'),
    path('sucursales/detail/<int:pk>/',SucursalDetailView.as_view(), name='sucursal_detail'),
    path('depositos/',DepositosListView.as_view(), name='depositos_list'),
    path('depositos/nuevo',DepositoCreateView.as_view(), name='deposito_create'),
    path('depositos/editar/<int:pk>/',DepositoUpdateView.as_view(), name='deposito_update'),
    path('depositos/delete/<int:pk>/',DepositoDeleteView.as_view(), name='deposito_delete'),
    path('depositos/detail/<int:pk>/',DepositoDetailView.as_view(), name='deposito_detail'),
    path('productos_list/', ProductoXDepositoListView.as_view(), name='productos_list'),
    path('productos_list/nuevo/', ProductoXDepositoCreateView.as_view(), name='producto_list_create'),
    path('productos_list/detail/<int:pk>/',ProductoXDepositoDetailView.as_view(), name='producto_list_detail'),
    path('productos_list/editar/<int:pk>/', ProductoXDepositoUpdateView.as_view(), name='producto_list_update'),
    path('productos_list/eliminar/<int:pk>/', ProductoXDepositoDeleteView.as_view(), name='producto_list_delete'),]


###urlpatterns = [
###    path('', ProductoListView.as_view(), name='producto_list'),
###    path('<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),
###    path('nuevo/', ProductoCreateView.as_view(), name='producto_create'),
###    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
###    path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
###]
