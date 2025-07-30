from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages

from .models import Post, Categoria, Comentario, Tag, ImagenPost
from .forms import PostForm, ComentarioForm, CustomUserCreationForm

def inicio(request):
    categoria_id = request.GET.get('categoria')
    fecha        = request.GET.get('fecha')
    busqueda     = request.GET.get('q')
    ordenar      = request.GET.get('orden')
    page         = request.GET.get('page')

    posts = (
        Post.objects
            .annotate(num_comentarios=Count('comentario'))
            .filter(publicado=True)
    )
    if categoria_id and categoria_id.isdigit():
        posts = posts.filter(categoria__id=int(categoria_id))

    if fecha == 'recientes':
        posts = posts.order_by('-fecha_creacion')
    elif fecha == 'antiguos':
        posts = posts.order_by('fecha_creacion')

    if busqueda:
        posts = posts.filter(
            Q(titulo__icontains=busqueda) |
            Q(contenido__icontains=busqueda)
        )

    if ordenar == 'comentarios':
        posts = posts.order_by('-num_comentarios')
    elif ordenar == 'fecha':
        posts = posts.order_by('-fecha_creacion')

    categorias      = Categoria.objects.all()
    tags_destacados = Tag.objects.annotate(total=Count('post')).order_by('-total')[:10]
    paginator       = Paginator(posts, 6)
    pagina          = paginator.get_page(page)

    return render(request, 'inicio.html', {
        'posts': pagina,
        'categorias': categorias,
        'tags_destacados': tags_destacados
    })

def detalle_post(request, post_id):
    post        = get_object_or_404(Post, pk=post_id)
    comentarios = Comentario.objects.filter(post=post).order_by('-fecha_creacion')
    imagenes    = ImagenPost.objects.filter(post=post)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                nuevo_comentario               = form.save(commit=False)
                nuevo_comentario.post          = post
                nuevo_comentario.autor         = request.user
                nuevo_comentario.fecha_creacion = timezone.now()
                nuevo_comentario.save()
                messages.success(request, "Comentario agregado correctamente.")
                return redirect('detalle_post', post_id=post.id)
        else:
            messages.error(request, "Tenés que iniciar sesión para comentar.")
            return redirect('login')
    else:
        form = ComentarioForm()

    return render(request, 'detalle_post.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'imagenes': imagenes
    })

@login_required
def crear_post(request):
    if not request.user.is_staff:
        messages.error(request, "No tenés permisos para crear publicaciones.")
        return redirect('inicio')

    if request.method == 'POST':
        form     = PostForm(request.POST, request.FILES)
        imagenes = request.FILES.getlist('imagenes')

        if form.is_valid():
            contenido = form.cleaned_data.get('contenido', '').strip()
            if not contenido or contenido in ['&nbsp;', '']:
                messages.error(request, "El contenido no puede estar vacío.")
                return render(request, 'crear_post.html', {'form': form})

            try:
                nuevo_post = form.save(commit=False)
                nuevo_post.autor          = request.user
                nuevo_post.fecha_creacion = timezone.now()
                nuevo_post.save()  # obtiene ID

                form.instance = nuevo_post
                form.save()    # guarda relaciones m2m (tags)

                for imagen in imagenes:
                    if hasattr(imagen, 'content_type') and 'image' in imagen.content_type:
                        ImagenPost.objects.create(post=nuevo_post, imagen=imagen)

                messages.success(request, "Publicación creada con éxito.")
                return redirect('detalle_post', post_id=nuevo_post.id)
            except Exception as e:
                messages.error(request, f"Error al crear la publicación: {str(e)}")
        else:
            messages.error(request, "Por favor corregí los errores del formulario.")
    else:
        form = PostForm()

    return render(request, 'crear_post.html', {'form': form})

@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not (request.user.is_staff or request.user == post.autor):
        messages.error(request, "No tenés permisos para editar esta publicación.")
        return redirect('inicio')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.instance = post
            form.save()
            messages.success(request, "Publicación actualizada correctamente.")
            return redirect('detalle_post', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'editar_post.html', {
        'form': form,
        'post': post
    })

@login_required
def confirmar_eliminacion_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not (request.user.is_staff or request.user == post.autor):
        messages.error(request, "No tenés permisos para eliminar esta publicación.")
        return redirect('inicio')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Publicación eliminada correctamente.")
        return redirect('inicio')

    return render(request, 'confirmar_eliminacion_post.html', {'post': post})

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Registro exitoso. ¡Bienvenido!")
            return redirect('inicio')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def perfil_usuario(request):
    posts = Post.objects.filter(autor=request.user).order_by('-fecha_creacion')
    return render(request, 'perfil_usuario.html', {'posts': posts})

def posts_por_categoria(request, categoria_nombre):
    categoria       = get_object_or_404(Categoria, nombre=categoria_nombre)
    posts           = Post.objects.filter(categoria=categoria, publicado=True).order_by('-fecha_creacion')
    paginator       = Paginator(posts, 6)
    posts_paginados = paginator.get_page(request.GET.get('page'))

    # Top 5 últimas noticias
    ultimos_posts = Post.objects.filter(publicado=True).order_by('-fecha_creacion')[:5]

    return render(request, 'posts_por_categoria.html', {
        'categoria': categoria,
        'posts': posts_paginados,
        'ultimos_posts': ultimos_posts,
    })

def posts_por_tag(request, tag_nombre):
    tag_obj = get_object_or_404(Tag, nombre__iexact=tag_nombre)
    posts_qs        = Post.objects.filter(tags=tag_obj, publicado=True).order_by('-fecha_creacion')
    paginator       = Paginator(posts_qs, 6)
    posts_paginados = paginator.get_page(request.GET.get('page'))
    return render(request, 'posts_por_tag.html', {
        'posts': posts_paginados,
        'tag': tag_obj.nombre,
    })
