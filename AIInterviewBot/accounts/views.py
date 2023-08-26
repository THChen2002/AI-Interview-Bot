from django.shortcuts import render

# Create your views here.

# 首頁
def index(request): 
    return render(request, 'accounts/index.html')