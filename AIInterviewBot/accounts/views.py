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
