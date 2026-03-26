from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('task_list')

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('task_list')

    return render(request, 'register.html')


def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == "POST":
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            owner=request.user
        )
        return redirect('task_list')

    return render(request, 'task_form.html')



@login_required
def task_update(request, id):
    task = Task.objects.get(id=id, owner=request.user)

    if request.method == "POST":
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('task_list')

    return render(request, 'task_form.html', {'task': task})


@login_required
def task_delete(request, id):
    task = Task.objects.get(id=id, owner=request.user)
    task.delete()
    return redirect('task_list')