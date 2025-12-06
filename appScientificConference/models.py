from django.db import models

class Track(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    afiliacion = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to='img',blank=True,null=True,verbose_name='Image')

    def __str__(self):
        return self.nombre


class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    abstract = models.TextField()
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="articulos")
    autores = models.ManyToManyField(Autor, related_name="articulos")

    def __str__(self):
        return self.titulo
