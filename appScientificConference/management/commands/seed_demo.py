import random
from django.core.management.base import BaseCommand
from django.db import transaction
from appScientificConference.models import Track, Autor, Articulo

TRACKS = [
    ("Computación Cuántica", "Algoritmos y hardware cuántico."),
    ("Neurociencia", "Conexiones mente-tecnología."),
    ("Energías Renovables", "Avances en sostenibilidad."),
]

AUTORES = [
    ("María Torres", "U. Buenos Aires"),
    ("Carlos Peña", "U. Chile"),
    ("Lucía Fernández", "CNRS"),
    ("Jorge Silva", "UC Berkeley"),
]

class Command(BaseCommand):
    help = "Genera datos de demostración"

    def handle(self, *args, **options):
        with transaction.atomic():
            Articulo.objects.all().delete()
            Autor.objects.all().delete()
            Track.objects.all().delete()

            tracks = [Track.objects.create(nombre=n, descripcion=d) for n, d in TRACKS]
            autores = [Autor.objects.create(nombre=n, afiliacion=a) for n, a in AUTORES]

            for i in range(1, 11):
                track = random.choice(tracks)
                articulo = Articulo.objects.create(
                    titulo=f"Estudio Experimental #{i}",
                    abstract="Resumen sintético del estudio y sus implicaciones interdisciplinarias.",
                    track=track,
                )
                seleccion = random.sample(autores, k=random.randint(1, min(2, len(autores))))
                articulo.autores.add(*seleccion)

        self.stdout.write(self.style.SUCCESS("Seed de demostración creada."))