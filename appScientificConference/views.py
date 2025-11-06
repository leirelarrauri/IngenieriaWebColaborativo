from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from .models import Articulo, Autor, Track

# Devuelve el listado de tracks 
def index_tracks(request):
    tracks = get_list_or_404(Track.objects.order_by('nombre'))
    context = {'lista_tracks': tracks }
    return render(request, 'index.html', context)



# Devuelve los datos de un track 
def show_track(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    output = f'Detalles del track: {track.id}, {track.nombre}, {track.descripcion}'
    return HttpResponse(output)

def show_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    articulos = track.articulos.all().order_by('titulo')
    return render(request, 'track.html', {
        'track': track,
        'articulos': articulos
    })
# Devuelve los autores de un artículo
def index_autores_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    output = ', '.join([a.nombre for a in articulo.autores.all()])
    return HttpResponse(output)

# Devuelve los detalles de un autor 
def show_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    output = f'Detalles del autor: {autor.id}, {autor.nombre}, {autor.afiliacion}'
    return HttpResponse(output)

# Devuelve los detalles de un artículo 
def show_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    output = f'Detalles del artículo: {articulo.id}, {articulo.titulo}. Autores: {[a.nombre for a in articulo.autores.all()]}'
    return HttpResponse(output)
