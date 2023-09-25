from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.forms import RegisterForm , LoginForm, ForgotPasswordForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm


# 首頁
@login_required(login_url="Login")
def index(request): 
    return render(request, 'accounts/index.html')

# 登入
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')  # 如果使用者已經登入，直接導向首頁
    
    if request.method == "POST":
        loginForm = LoginForm(request.POST) 
        if loginForm.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            remember_me = request.POST.get("remember_me")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # <-- Here if the remember me is False, that is why expiry is set to 0 seconds. So it will automatically close the session after the browser is closed.
                                                    # else browser session will be as long as the session  cookie time "SESSION_COOKIE_AGE"
                            # 判斷 user 是否為 social account，並檢查 UserProfile 是否存在
                return redirect('/')  # 導向到首頁
        else:
            message = '驗證碼錯誤!'
    else:
        loginForm = LoginForm()

    return render(request, 'accounts/login.html', locals())


# 登出
def log_out(request):
    logout(request)
    return redirect('/')
  
# 註冊
def register(request):
    # 如果使用者已經登入，直接導向首頁
    if request.user.is_authenticated:
        return redirect('/')
    
    registerForm = RegisterForm()
    if request.method == "POST":
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            
            # 儲存 User 物件到資料庫並取得已創建的 User 物件
            user = registerForm.save()

            # 創建 UserProfile 物件
            # profile = UserProfile()
            # profile.user = User.objects.get(id=user.id)
            # profile.user_name = user.username
            # profile.email = user.email

            # profile.save()  # 儲存 UserProfile 物件到資料庫

            # 電子郵件內容樣板
            email_template = render_to_string(
                'accounts/signup_success_email.html',
                {'username': request.user.username}
            )

            email = EmailMessage(
                '註冊成功通知信',  # 電子郵件標題
                email_template,  # 電子郵件內容
                settings.EMAIL_HOST_USER,  # 寄件者
                [request.POST.get("email")]  # 收件者
            )

            email.fail_silently = False
            email.send()

            return HttpResponse('<script>alert("註冊成功！"); window.location.href = "/login";</script>')
        else:
            message = ''
            for error in registerForm.errors:
                message += (error + "\n")
            return HttpResponse('<script>alert("註冊失敗！"'+ message +');</script>')

    return render(request, 'accounts/register.html', locals())

#忘記密碼頁面
def forgot_password(request):
    forgotPasswordForm = ForgotPasswordForm()
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            # 生成一個隨機的密碼重置令牌
            token = default_token_generator.make_token(user)
            # 將令牌和使用者資訊保存到資料庫
            user.reset_password_token = token
            user.save()
            # 發送包含重置連結的電子郵件

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri('/reset/confirm/'+ uidb64 + '/' + token)
            send_mail(
                '密碼重置請求',
                '請點擊以下連結來重置您的密碼: ' + reset_link,
                settings.EMAIL_HOST_USER,  # 寄件者
                [email],
                fail_silently=False,
            )
            return render(request, 'accounts/email_success.html')
        except User.DoesNotExist:
            return render(request, 'accounts/email_error.html')
    return render(request, 'accounts/forgot_password.html', locals())
  
#修改密碼
def change_password(request):
    changePasswordForm = ChangePasswordForm()
    return render(request, 'accounts/change_password.html', locals())

#使用者收信後的連結頁面
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # 顯示密碼重設表單
        form = SetPasswordForm(user=user)
        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                user.reset_password_token = None
                user.save()
                messages.success(request, '您的密碼已成功重設。')
                return redirect('password_reset_complete')
        return render(request, 'accounts/reset_password_confirm.html', {'form': form})
    else:
        # 顯示錯誤訊息
        messages.error(request, '密碼重設連結無效或已過期。')
        return redirect('forgot_password')
    
#密碼重設成功頁面
def password_reset_complete(request):
    return render(request, 'accounts/reset_password_complete.html')
  
#個人檔案頁面
def basic_info(request):
    return render(request, 'basic_info.html', locals())
