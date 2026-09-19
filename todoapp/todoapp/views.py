from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Task

def task_list(req):
    task = Task.objects.all().order_by('-created_at')
    return render(req, 'todo/task_list.html', {'task':task})

def task_create(req):
    if req.method == 'POST':
        title = req.POST.get('title','').strip()
        discription = req.POST.get('description','').strip()
        if title:
            Task.objects.create(title=title, description=discription)
            return redirect(reverse('task_list'))
        error = "Title cannot be empty"
        return render(req, 'todo/task_form.html', {'error':error})
    return render(req, 'todo/task_form.html')

def task_update(req, pk):
    task = get_object_or_404(Task, pk=pk)
    if req.method == 'POST':
        title = req.POST.get('title', '').strip()
        description = req.POST.get('description', '').strip()
        completed = req.POST.get('completed') == 'on'
        if title:
            task.title = title
            task.description = description
            task.completed = completed
            task.save()
            return redirect(reverse('task_list'))
        return render(req, 'todo/task_form.html', {'task':task, 'error':'Title cannot be empty'})
    return render(req, 'todo/task_form.html')

def task_delete(req, pk):
    task = get_object_or_404(Task, pk=pk)
    if req.method == "POST":
        task.delete()
        return redirect(reverse('task_list'))
    return render(req, 'todo/task_comfirm_delete.html', {'task':task})

def task_toggle_complete(req, pk):
    task = get_object_or_404(Task, pk=pk)
    if req.method == "POST":
        task.completed = not task.completed
        task.save()
    return redirect('task_list')