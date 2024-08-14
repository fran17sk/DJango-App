from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def home(request):
    return render(request, 'base.html')

class ProductoListView(LoginRequiredMixin,ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'
    login_url = '/login/'

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto_detail.html'
    context_object_name = 'producto'

class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio','categoria','estado']
    success_url = reverse_lazy('producto_list')

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio','categoria','estado']
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')