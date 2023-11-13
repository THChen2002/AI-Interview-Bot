from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from captcha.fields import CaptchaField, CaptchaTextInput
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth import get_user_model
User = get_user_model()


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

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("此電子郵件已被註冊過")
       return self.cleaned_data

class LoginForm(forms.Form):

    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    captcha = CaptchaField(label="驗證碼")

    remember_me = forms.BooleanField(
        label="保持登入",
        required=False, 
        widget=forms.CheckboxInput()
    )

# 修改密碼
class ChangePasswordForm(PasswordChangeForm):

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

# 問題回報
class ProblemReportForm(forms.Form):
    type = forms.ChoiceField(
        label="選擇模式",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=(
            ('1', '帳號問題'),
            ('2', '技術問題'),
            ('3', '其他問題'),
        )
    )

    problem = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'遇到問題了嗎?若無法在幫助中心找到相關的解決方式，請在此簡單敘述您遇到的問題。'})
    )