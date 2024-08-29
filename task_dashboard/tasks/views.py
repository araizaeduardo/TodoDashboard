from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from .models import Task, Tag
from .forms import TaskForm, TaskFilterForm
from calendar import monthrange, HTMLCalendar
from datetime import date, timedelta, datetime

# Create your views here.

class CalendarView(TemplateView):
    model = Task
    template_name = 'tasks/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.kwargs.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, tasks):
        tasks_per_day = tasks.filter(due_date__day=day)
        d = ''
        for task in tasks_per_day:
            d += f'<li>{task.get_html_url}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, tasks):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, tasks)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        tasks = Task.objects.filter(due_date__year=self.year, due_date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, tasks)}\n'
        return cal

def task_list(request):
    tasks = Task.objects.all()
    form = TaskFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data['search']:
            search_query = form.cleaned_data['search']
            tasks = tasks.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        if form.cleaned_data['state']:
            tasks = tasks.filter(state=form.cleaned_data['state'])
        if form.cleaned_data['tags']:
            tasks = tasks.filter(tags__in=form.cleaned_data['tags']).distinct()

    context = {
        'tasks': tasks,
        'form': form,
        'task_states': Task.TASK_STATES,
    }
    return render(request, 'tasks/task_list.html', context)

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por estado
        state = self.request.GET.get('state')
        if state:
            queryset = queryset.filter(state=state)
        
        # Búsqueda
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.search(query)
        
        # Filtro por etiqueta
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['states'] = Task.TASK_STATES
        context['current_state'] = self.request.GET.get('state', '')
        context['query'] = self.request.GET.get('q', '')
        context['tags'] = Tag.objects.all()
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

def change_task_state(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        new_state = request.POST.get('state')
        if new_state in dict(Task.TASK_STATES):
            task.state = new_state
            task.save()
    return redirect('task_list')
