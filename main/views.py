from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, RequestForm
from .models import Request

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('home')

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_instanse = form.save(commit=False)
            request_instanse.user = request.user
            request_instanse.save()
            messages.success(request, 'Request created successfully.')
            return redirect('view_requests')
    else:
        form = RequestForm()
    return render(request, 'create_request.html', {'form': form})

@login_required
def view_requests(request):
    requests = Request.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'view_requests.html', {'requests': requests})

@login_required
def delete_request(request, request_id):
    request_instance = get_object_or_404(Request, id=request_id, user=request.user)
    if request_instance.status == 'Новая':
        request_instance.delete()
        messages.success(request, 'Request deleted successfully.')
    else:
        messages.error(request, 'Cannot delete a request that is not in "New" status.')
    return redirect('view_requests')

# Create your views here.
