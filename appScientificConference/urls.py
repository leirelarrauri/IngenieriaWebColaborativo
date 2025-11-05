from django.urls import path
from . import views

urlpatterns = [
    path('tracks/', views.index_tracks, name='index_tracks'),
    path('tracks/<int:track_id>/', views.show_track, name='show_track'),
    path('articulos/<int:articulo_id>/autores/', views.index_autores_articulo, name='index_autores_articulo'),
    path('autores/<int:autor_id>/', views.show_autor, name='show_autor'),
    path('articulos/<int:articulo_id>/', views.show_articulo, name='show_articulo'),
]