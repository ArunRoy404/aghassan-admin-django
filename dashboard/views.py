from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
def home(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'dashboard/home.html', {'users': users})

@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'on'
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = is_staff
            user.save()
            messages.success(request, f'User {username} created successfully')
            return redirect('home')
            
    return render(request, 'dashboard/add_user.html')

@user_passes_test(is_admin)
def toggle_admin(request, user_id):
    user = User.objects.get(id=user_id)
    if user == request.user:
        messages.error(request, "You can't change your own status")
    else:
        user.is_staff = not user.is_staff
        user.save()
        status = "Admin" if user.is_staff else "Regular User"
        messages.success(request, f'User {user.username} is now a {status}')
    return redirect('home')

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user == request.user:
        messages.error(request, "You can't delete yourself")
    else:
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted')
    return redirect('home')
