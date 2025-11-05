from django.db import models
# Ejemplo Django
class Track(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    afiliacion = models.CharField(max_length=200, blank=True)

class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    abstract = models.TextField()
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="articulos")
    autores = models.ManyToManyField(Autor, related_name="articulos")
