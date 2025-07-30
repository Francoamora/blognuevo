from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = RichTextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='imagenes_post/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class ImagenPost(models.Model):
    post = models.ForeignKey(Post, related_name='galeria', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='galeria_post/')
    descripcion = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )

    def __str__(self):
        return f"Imagen de {self.post.titulo}"


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.username} en {self.post.titulo}"
