from django import forms
from django.contrib.auth.models import User
from .models import Task, Tag

class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'state', 'tags', 'due_date', 'priority', 'assigned_to']

class TaskFilterForm(forms.Form):
    search = forms.CharField(required=False)
    state = forms.ChoiceField(choices=[('', 'All')] + Task.TASK_STATES, required=False)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    # Campo de ordenación
    order_by = forms.ChoiceField(
        choices=[
            ('created_at', 'Fecha de creación'),
            ('due_date', 'Fecha de vencimiento'),
            ('priority', 'Prioridad')
        ],
        required=False
    )

    # Campo de fecha de vencimiento
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    # Campo de prioridad
    priority = forms.ChoiceField(
        choices=[('', 'Todas')] + Task.PRIORITY_CHOICES,
        required=False
    )

    # Campo de rango de fechas para filtrar tareas
    date_range_start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label='Fecha de inicio'
    )
    date_range_end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label='Fecha de fin'
    )

    # Campo para filtrar por usuario asignado
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label="Todos los usuarios"
    )