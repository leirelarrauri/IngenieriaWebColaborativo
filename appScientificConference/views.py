from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Articulo, Autor, Track

# Devuelve el listado de tracks (CORRECTO)
def index_tracks(request):
    tracks = get_list_or_404(Track.objects.order_by('nombre'))
    output = ', '.join([t.nombre for t in tracks])
    return HttpResponse(output)

# Devuelve los datos de un track (CORRECTO)
def show_track(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    output = f'Detalles del track: {track.id}, {track.nombre}, {track.descripcion}'
    return HttpResponse(output)

# Devuelve los autores de un artículo (CORREGIDO)
def index_autores_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    # Usar 'autores' en lugar de 'autor_set' porque la relación se llama 'autores'
    output = ', '.join([a.nombre for a in articulo.autores.all()])
    return HttpResponse(output)

# Devuelve los detalles de un autor (CORREGIDO)
def show_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    output = f'Detalles del autor: {autor.id}, {autor.nombre}, {autor.afiliacion}'
    return HttpResponse(output)

# Devuelve los detalles de un artículo (CORREGIDO)
def show_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    # Corregir el nombre del campo y usar 'autores' en lugar de 'autor_set'
    output = f'Detalles del artículo: {articulo.id}, {articulo.titulo}. Autores: {[a.nombre for a in articulo.autores.all()]}'
    return HttpResponse(output)
