from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.shortcuts import render
from .models import Articulo, Autor, Track
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ArticuloForm


#Devuelve la pagina principal
def index(request):
    tracks = Track.objects.all()
    tracks_con_articulo = []

    for track in tracks:
        # Obtiene el primer artículo 
        articulo_destacado = track.articulos.all().order_by('titulo').first()
        tracks_con_articulo.append({
            'track': track,
            'articulo_destacado': articulo_destacado
        })

    return render(request, 'index.html', {
        'tracks_con_articulo': tracks_con_articulo
    })

# Devuelve el listado de tracks 
def lista_tracks(request):
    tracks = get_list_or_404(Track.objects.order_by('nombre'))
    return render(request, 'tracks/tracks.html', {
        'tracks': tracks
    })

# Devuelve el listado de autores 
def lista_autores(request):
    autores = get_list_or_404(Autor.objects.order_by('nombre'))
    return render(request, 'autores/autores.html', {
        'autores': autores
    })

# Devuelve el listado de articulos 
def lista_articulos(request):
    articulos = get_list_or_404(Articulo.objects.order_by('titulo'))
    return render(request, 'articulos/articulos.html', {
        'articulos': articulos
    })

# Devuelve los detalles de un track 
def show_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    articulos = track.articulos.all().order_by('titulo')
    return render(request, 'tracks/track.html', {
        'track': track,
        'articulos': articulos
    })
# Devuelve los detalles de un autor 
def show_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    articulos = autor.articulos.all().order_by('titulo')
    return render(request, 'autores/autor.html', {
        'autor': autor,
        'articulos': articulos
    })

# Devuelve los detalles de un artículo 
def show_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)  
    return render(request, 'articulos/articulo.html', {
        'articulo': articulo,
        'track': articulo.track,
        'autores': articulo.autores.all().order_by('nombre')
    })

# Vistas para crear y editar artículos(formularios)
def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            articulo = form.save()
            return redirect('show_articulo', articulo_id=articulo.id)
    else:
        form = ArticuloForm()
    
    return render(request, 'articulos/form_articulo.html', {'form': form})

def editar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('show_articulo', articulo_id=articulo.id)
    else:
        form = ArticuloForm(instance=articulo)
    
    return render(request, 'articulos/form_articulo.html', {'form': form})  

