from django.shortcuts import render
from accounts.forms import RegisterForm

# Create your views here.

# 首頁
def index(request): 
    return render(request, 'accounts/index.html')

# 註冊
def register(request):
    registerForm = RegisterForm()
    return render(request, 'accounts/register.html', locals())