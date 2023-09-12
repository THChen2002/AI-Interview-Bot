from django.shortcuts import render
from accounts.forms import RegisterForm , LoginForm, ChangePasswordForm
from django.contrib.auth.models import User

from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


# 首頁
def index(request): 
    return render(request, 'accounts/index.html')

# 登入
def login(request):
    loginForm = LoginForm()
    return render(request, 'accounts/login.html', locals())
  
# 註冊
def register(request):
    registerForm = RegisterForm()
    return render(request, 'accounts/register.html', locals())

#忘記密碼頁面
def forgot_password(request):
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
    form = ChangePasswordForm()
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
