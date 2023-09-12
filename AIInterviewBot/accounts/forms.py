from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class RegisterForm(UserCreationForm):

    username = forms.CharField(
        label="帳號",
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


class LoginForm(forms.Form):

    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    captcha = CaptchaField()

    remember_me = forms.BooleanField(
        label="記住我",
        required=False, 
        widget=forms.CheckboxInput()
    )

# 修改密碼
class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(
        label="舊密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    newpassword1 = forms.CharField(
        label="新密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    newpassword2 = forms.CharField(
        label="新密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


    