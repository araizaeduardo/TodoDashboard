# Instalar django
python3 -m venv venv
source venv/bin/activate
python3 -m pip install Django

# Crear el proyecto Django
django-admin startproject task_dashboard
cd task_dashboard

# Crear la aplicación
python manage.py startapp tasks

# En task_dashboard/settings.py, añadir 'tasks' a INSTALLED_APPS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
]

# En tasks/models.py
from django.db import models

class Task(models.Model):
    TASK_STATES = [
        ('planned', 'Planeada'),
        ('started', 'Comenzada'),
        ('completed', 'Terminada'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=TASK_STATES, default='planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# En tasks/admin.py
from django.contrib import admin
from .models import Task

admin.site.register(Task)

# Crear las migraciones y aplicarlas
python manage.py makemigrations
python manage.py migrate

# Crear un superusuario
python manage.py createsuperuser

# Iniciar el servidor de desarrollo
python manage.py runserver

# Acceder al panel de administración
# Visita http://127.0.0.1:8000/admin/ en tu navegador
# Inicia sesión con las credenciales del superusuario que creaste

# Para detener el servidor, presiona CTRL+C en la terminal# todoDashboard
