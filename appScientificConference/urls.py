from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tracks/', views.lista_tracks, name='lista_tracks'),
    path('tracks/<int:track_id>/', views.show_track, name='show_track'),
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autores/<int:autor_id>/', views.show_autor, name='show_autor'),
    path('articulos/', views.lista_articulos, name='lista_articulos'),
    path('articulos/<int:articulo_id>/', views.show_articulo, name='show_articulo'),
    
    # Formularios
    path('articulos/crear/', views.crear_articulo, name='crear_articulo'),
    path('articulos/editar/<int:pk>/', views.editar_articulo, name='editar_articulo'),
    
]