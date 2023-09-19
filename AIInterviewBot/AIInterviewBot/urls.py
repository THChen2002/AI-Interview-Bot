"""AIInterviewBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import accounts.views as accounts

urlpatterns = [
    # 管理後台
    path('admin/', admin.site.urls),

    # ----------套件 start----------
    
    # 驗證碼
    path('captcha/', include('captcha.urls')),

    # ----------套件 end----------

    # ----------accounts start----------

    # 首頁
    path('', accounts.index),
    # 註冊
    path('register/', accounts.register, name='Register'),
    # 忘記密碼頁面
    path('forgot_password/', accounts.forgot_password, name='ForgotPassword'),
    # 個人檔案頁面
    path('basic_info/', accounts.basic_info, name='Basic_info'),

    # ----------accounts end----------
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)