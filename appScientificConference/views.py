from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.shortcuts import render
from .models import Articulo, Autor, Track
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ArticuloForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy


#Devuelve la pagina principal
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tracks = Track.objects.all()
        tracks_con_articulo = []

        for track in tracks:
            # Obtiene el primer artículo 
            articulo_destacado = track.articulos.all().order_by('titulo').first()
            tracks_con_articulo.append({
                'track': track,
                'articulo_destacado': articulo_destacado
            })

        context['tracks_con_articulo'] = tracks_con_articulo
        return context

# Devuelve el listado de tracks 
class ListaTracksView(ListView):
    model = Track
    template_name = 'tracks/tracks.html'
    context_object_name = 'tracks'
    ordering = ['nombre']

# Devuelve el listado de autores 
class ListaAutoresView(ListView):
    model = Autor
    template_name = 'autores/autores.html'
    context_object_name = 'autores'
    ordering = ['nombre']

# Devuelve el listado de articulos 
class ListaArticulosView(ListView):
    model = Articulo
    template_name = 'articulos/articulos.html'
    context_object_name = 'articulos'
    ordering = ['titulo']

# Devuelve los detalles de un track 
class ShowTrackView(DetailView):
    model = Track
    template_name = 'tracks/track.html'
    context_object_name = 'track'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulos'] = self.object.articulos.all().order_by('titulo')
        return context

# Devuelve los detalles de un autor 
class ShowAutorView(DetailView):
    model = Autor
    template_name = 'autores/autor.html'
    context_object_name = 'autor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulos'] = self.object.articulos.all().order_by('titulo')
        return context

# Devuelve los detalles de un artículo 
class ShowArticuloView(DetailView):
    model = Articulo
    template_name = 'articulos/articulo.html'
    context_object_name = 'articulo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['track'] = self.object.track
        context['autores'] = self.object.autores.all().order_by('nombre')
        return context

# Vistas para crear y editar artículos(formularios)
class CrearArticuloView(CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'articulos/form_articulo.html'

    def get_success_url(self):
        return reverse_lazy('show_articulo', kwargs={'pk': self.object.pk})

class EditarArticuloView(UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'articulos/form_articulo.html'

    def get_success_url(self):
        return reverse_lazy('show_articulo', kwargs={'pk': self.object.pk})  

