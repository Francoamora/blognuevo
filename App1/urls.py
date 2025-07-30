from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Página principal
    path('', views.inicio, name='inicio'),

    # CRUD de posts
    path('crear/', views.crear_post, name='crear_post'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),
    path('editar/<int:post_id>/', views.editar_post, name='editar_post'),
    path('post/<int:post_id>/eliminar/', views.confirmar_eliminacion_post, name='confirmar_eliminacion_post'),

    # Perfil de usuario
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # Filtrado por categoría y etiquetas
    path('categoria/<str:categoria_nombre>/', views.posts_por_categoria, name='posts_por_categoria'),
    path('tags/<str:tag_nombre>/', views.posts_por_tag, name='posts_por_tag'),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('inicio')), name='logout'),
    path('registro/', views.registro, name='registro'),

    # Recuperación de contraseña
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            success_url=reverse_lazy('password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
