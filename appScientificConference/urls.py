from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tracks/', views.ListaTracksView.as_view(), name='lista_tracks'),
    path('tracks/<int:pk>/', views.ShowTrackView.as_view(), name='show_track'),
    path('autores/', views.ListaAutoresView.as_view(), name='lista_autores'),
    path('autores/<int:pk>/', views.ShowAutorView.as_view(), name='show_autor'),
    path('articulos/', views.ListaArticulosView.as_view(), name='lista_articulos'),
    path('articulos/<int:pk>/', views.ShowArticuloView.as_view(), name='show_articulo'),
    
    # Formularios
    path('articulos/crear/', views.CrearArticuloView.as_view(), name='crear_articulo'),
    path('articulos/editar/<int:pk>/', views.EditarArticuloView.as_view(), name='editar_articulo'),
    
]