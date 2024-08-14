from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ProductoListView,
    ProductoDetailView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoDeleteView
)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
]
###urlpatterns = [
###    path('', ProductoListView.as_view(), name='producto_list'),
###    path('<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),
###    path('nuevo/', ProductoCreateView.as_view(), name='producto_create'),
###    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
###    path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
###]
