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

    def save(self, commit=True):
        # Parseamos las etiquetas en texto
        tags_str = self.cleaned_data.get('tags', '')
        tags_list = [nombre.strip() for nombre in tags_str.split(',') if nombre.strip()]

        # Obtenemos la instancia sin guardar m2m aún
        instance = super().save(commit=False)
        instance.contenido = self.cleaned_data.get('contenido', '')

        if commit:
            # Guardamos el Post para que obtenga un ID
            instance.save()
            # Ahora sí podemos gestionar la relación many-to-many
            instance.tags.clear()
            for nombre in tags_list:
                if not nombre.replace(' ', '').isalpha():
                    continue
                tag, _ = Tag.objects.get_or_create(nombre=nombre)
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
