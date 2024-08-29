from django.db import models
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class TaskQuerySet(models.QuerySet):
    def search(self, query):
        return self.annotate(
            search=SearchVector('title', 'description'),
        ).filter(search=query)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    TASK_STATES = [
        ('planned', 'Planeada'),
        ('started', 'Comenzada'),
        ('completed', 'Terminada'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=TASK_STATES, default='planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    objects = TaskQuerySet.as_manager()
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')

    def get_absolute_url(self):
        return reverse('task_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.title