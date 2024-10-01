from django.urls import path
from .views import home_view, login_view

urlpatterns = [
    path('', home_view, name='home'),  # Página de inicio
    path('login/', login_view, name='login'),  # Página de inicio de sesión
]
