from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comentario, Tag, Categoria


# FORMULARIO DE REGISTRO EXTENDIDO
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({'class': 'form-control'})
        self.fields["password1"].widget.attrs.update({'class': 'form-control'})
        self.fields["password2"].widget.attrs.update({'class': 'form-control'})


# FORMULARIO DE POST
class PostForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    tags = forms.CharField(
        required=False,
        label="Etiquetas",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Etiquetas separadas por comas (ej: acción, aventura)'
        })
    )

    contenido = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'categoria', 'imagen', 'tags']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join(
                [tag.nombre for tag in self.instance.tags.all()]
            )

    @staticmethod
    def _normalize_tag_name(nombre: str) -> str:
        """
        Normaliza el nombre de la etiqueta: recorta espacios,
        colapsa espacios internos y capitaliza palabras.
        Mantiene acentos (útil en español).
        """
        base = ' '.join(nombre.strip().split())
        # Capitaliza cada palabra (no tocamos acentos)
        return base.title()

    def save(self, commit=True):
        # Parseo y normalización de etiquetas en texto
        tags_str = self.cleaned_data.get('tags', '')
        raw_list = [x for x in (t.strip() for t in tags_str.split(',')) if x]

        norm_list = []
        for nombre in raw_list:
            norm = self._normalize_tag_name(nombre)
            # Permitimos letras, números, espacios, guiones y # (por si usás hashtags)
            # Si querés más restrictivo, ajustar este filtro.
            if not all(ch.isalnum() or ch in " -#" for ch in norm):
                continue
            norm_list.append(norm)

        # Obtenemos la instancia del Post sin guardar m2m aún
        instance = super().save(commit=False)
        instance.contenido = self.cleaned_data.get('contenido', '')

        if commit:
            instance.save()  # garantiza ID
            # Gestionamos relación M2M evitando duplicados (case-insensitive)
            instance.tags.clear()
            for nombre in norm_list:
                existente = Tag.objects.filter(nombre__iexact=nombre).first()
                if existente:
                    tag = existente
                else:
                    tag = Tag.objects.create(nombre=nombre)
                instance.tags.add(tag)

        return instance


# FORMULARIO DE COMENTARIO
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribí tu comentario...',
                'rows': 3
            }),
        }
