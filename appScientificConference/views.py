from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from .models import Articulo, Autor, Track


#Devuelve la pagina principal
def index(request):
    # Obtener todos los tracks ordenados
    tracks = Track.objects.all().order_by('nombre')
    
    # Crear una lista de tuplas (track, articulo_destacado)
    tracks_con_articulo = []
    
    for track in tracks:
        # Eliges el primer articulo ordenado por titulo
        articulo_destacado = track.articulos.order_by('titulo').first()
        
        tracks_con_articulo.append({
            'track': track,
            'articulo_destacado': articulo_destacado
        })
    
    context = {
        'tracks_con_articulo': tracks_con_articulo
    }
    return render(request, 'index.html', context)

# Devuelve el listado de tracks 
def lista_tracks(request):
    tracks = get_list_or_404(Track.objects.order_by('nombre'))
    return render(request, 'tracks.html', {
        'lista_tracks': tracks
    })

# Devuelve el listado de autores 
def lista_autores(request):
    autores = get_list_or_404(Autor.objects.order_by('nombre'))
    return render(request, 'autores.html', {
        'lista_autores': autores
    })

# Devuelve el listado de articulos 
def lista_articulos(request):
    articulos = get_list_or_404(Articulo.objects.order_by('nombre'))
    return render(request, 'articulos.html', {
        'lista_articulos': articulos
    })

# Devuelve los detalles de un track 
def show_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    articulos = get_list_or_404(track.articulos.all().order_by('titulo'))
    return render(request, 'track.html', {
        'track': track,
        'articulos': articulos
    })
# Devuelve los detalles de un autor 
def show_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    articulos = autor.articulos.all().order_by('titulo')
    return render(request, 'autor.html', {
        'autor': autor,
        'articulos': articulos
    })

# Devuelve los detalles de un artículo 
def show_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    track = get_object_or_404(Track, pk=articulo.track.id)
    autores = get_list_or_404(articulo.autores.all().order_by('titulo'))    
    return render(request, 'articulo.html', {
        'articulo': articulo,
        'track': track,
        'autores': autores
    })
