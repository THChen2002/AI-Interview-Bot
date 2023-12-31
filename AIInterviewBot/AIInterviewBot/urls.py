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
import contents.views as contents

urlpatterns = [
    # 管理後台
    path('admin/', admin.site.urls),

    # ----------套件 start----------
    
    # 驗證碼
    path('captcha/', include('captcha.urls')),
    #django-allauth
    path('accounts/', include('allauth.urls')),

    # ----------套件 end----------

    # ----------accounts start----------

    # 首頁
    path('', accounts.index, name='Index'),
    # 登入
    path('login/', accounts.sign_in, name='Login'),
    # 登出
    path('logout/',accounts.log_out, name='Logout'),
    # 註冊
    path('register/', accounts.register, name='Register'),
    # 忘記密碼頁面
    path('forgot_password/', accounts.forgot_password, name='ForgotPassword'),
    # 個人檔案頁面
    path('personal/', accounts.personal, name='Personal'),
    # 密碼重設確認頁面
    path('reset/confirm/<uidb64>/<token>/', accounts.password_reset_confirm, name='PasswordResetConfirm'),
    # 密碼重設完成頁面
    path('reset/complete/', accounts.password_reset_complete, name='PasswordResetComplete'),
    # 修改密碼
    path('change_password/', accounts.change_password, name='ChangePassword'),
    # 幫助中心
    path('help_center/', accounts.help_center, name='HelpCenter'),
    # 問題回報
    path('problem_report/', accounts.problem_report, name='ProblemReport'),

    # ----------accounts end------------

    # ----------contents start----------
    
    # 自我介紹
    path('self_introduction/', contents.self_introduction, name='SelfIntroduction'),
    # 求職信
    path('cover_letter/', contents.cover_letter, name='CoverLetter'),
    path('<str:type>/result/', contents.content_result, name='ContentResult'),
    # 推薦信
    path('recommendation_letter/', contents.recommendation_letter, name='RecommendationLetter'),
    # 簡歷
    path('resume/', contents.resume, name='Resume'),
    path('api/download_file/', contents.download_file, name='DownloadFile'),
    # 模擬面試
    path('mock_interview_mode/', contents.mock_interview_mode, name='MockInterviewMode'),
    path('mock_interview/<str:mode>/', contents.mock_interview, name='MockInterview'),
    path('mock_interview_result/', contents.mock_interview_result, name='MockInterviewResult'),
    # 儀錶板
    path('dashboard/', contents.dashboard, name='Dashboard'),
    path('api/get_chart_data/', contents.get_chart_data, name='GetChartData'),
    # 歷史紀錄首頁
    path('history/', contents.history, name='History'),
    # 歷史紀錄詳細頁面
    path('history/detail/', contents.history_detail, name='HistoryDetail'),

    # ----------contents end------------
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)