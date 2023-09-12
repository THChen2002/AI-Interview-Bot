from django.shortcuts import render
from accounts.forms import RegisterForm , LoginForm

# Create your views here.

# 首頁
def index(request): 
    return render(request, 'accounts/index.html')

# 註冊
def register(request):
    registerForm = RegisterForm()
    return render(request, 'accounts/register.html', locals())

# 登入
def login(request):
    loginForm = LoginForm()
    return render(request, 'accounts/login.html', locals())