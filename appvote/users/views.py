from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if all([username, firstname, email, password1, password2]):
            if User.objects.filter(username=username).exists():
                return render(request, 'registration/register.html', {
                    'error': 'Bu username allaqachon band.'
                })
            if password1 != password2:
                return render(request, 'registration/register.html', {
                    'error': 'Parollar bir xil emas.'
                })
            
            # Foydalanuvchi yaratish
            User.objects.create_user(
                username=username,
                first_name=firstname,
                email=email,
                password=password1
            )

            # Avtomatik login
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user)
                redirect_url = request.GET.get('next', 'main:home')
                return redirect(redirect_url)
            else:
                return render(request, 'registration/register.html', {
                    'error': 'Login qilishda xatolik.'
                })
        else:
            return render(request, 'registration/register.html', {
                'error': 'Barcha maydonlarni to‘ldiring.'
            })
    return render(request, 'registration/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_url = request.GET.get('next', 'main:home')
                return redirect(redirect_url)
            else:
                return render(request, 'registration/login.html', {
                    'error': 'Login yoki parol noto‘g‘ri.'
                })
        else:
            return render(request, 'registration/login.html', {
                'error': 'Barcha maydonlarni to‘ldiring.'
            })
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('main:home')
