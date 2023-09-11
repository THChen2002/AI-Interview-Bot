from django.shortcuts import render
from accounts.forms import RegisterForm
from accounts.forms import ChangePasswordForm


# Create your views here.

# 首頁
def index(request): 
    return render(request, 'accounts/index.html')

# 註冊
def register(request):
    registerForm = RegisterForm()
    return render(request, 'accounts/register.html', locals())

#修改密碼
def change_password(request):
    form = ChangePasswordForm()
    return render(request, 'accounts/change_password.html', locals())