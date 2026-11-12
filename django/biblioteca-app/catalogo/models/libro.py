from django.db import models
from .categoria import Categoria

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    autores = models.ManyToManyField('Autor', related_name='libros', blank=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']