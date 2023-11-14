from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import ProblemReport
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model , authenticate
User = get_user_model()


class RegisterForm(UserCreationForm):

    error_messages = {
        "password_mismatch": _("密碼驗證錯誤，請重新輸入"),
    }

    username = forms.CharField(
        label="帳號",
        error_messages={'unique':'此使用者名稱已被使用'},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("此電子郵件已被註冊過")
       # TODO:跳出email重複錯誤訊息
       return self.cleaned_data

class LoginForm(forms.Form):

    error_messages = {"invalid_login":_("帳號或密碼錯誤")}
    
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    captcha = CaptchaField(
        label="驗證碼",
        error_messages={"invalid": "驗證碼錯誤"}
    )

    remember_me = forms.BooleanField(
        label="保持登入",
        required=False, 
        widget=forms.CheckboxInput()
    )

    def clean_data(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("invalid_login")
        # TODO:跳出帳號/密碼錯誤的訊息
        return self.cleaned_data

# 修改密碼
class ChangePasswordForm(PasswordChangeForm):

    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": _("舊密碼輸入錯誤，請重新輸入"),
        "password_mismatch": _("密碼驗證錯誤，請重新輸入"),
    }
    old_password = forms.CharField(
        label="舊密碼",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )
    new_password1 = forms.CharField(
        label="新密碼",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )
    new_password2 = forms.CharField(
        label="新密碼確認",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

# 忘記密碼
class ForgotPasswordForm(forms.Form):
    
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

# 個人檔案
class PersonalForm(ModelForm):
    class Meta:
        model = User
        fields = ('profile_image', 'gender', 'birth_date', 'degree')
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control', 'id': 'photo', 'accept': 'image/*', 'style': 'display: none;'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'disabled':''}),
            'birth_date': forms.DateInput(attrs={'type':'date', 'class': 'form-control', 'disabled':''}),
            'degree': forms.Select(attrs={'class': 'form-control', 'disabled':''}),
        }


TYPE_CHOICES = (
    ('', '請選擇問題類型'),
    ('A', '帳號問題'),
    ('T', '技術問題'),
    ('O', '其他問題')
)
# 問題回報
class ProblemReportForm(ModelForm):
    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = ProblemReport
        fields = ('type', 'problem')
        widgets = {
            'problem': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'遇到問題了嗎?若無法在幫助中心找到相關的解決方式，請在此簡單敘述您遇到的問題。'}),
        }