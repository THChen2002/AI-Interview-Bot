from django import forms
from .models import ResumeRecord
from django.forms import ModelForm

class SelfIntroductionForm(forms.Form):
    company = forms.CharField(
        label="要面試的公司",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    job = forms.CharField(
        label="要面試的職業",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    skill1 = forms.CharField(
        label="個人專長1",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    skill2 = forms.CharField(
        label="個人專長2",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cultural_fit = forms.CharField(
        label="與要面試的公司文化契合點",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5,'style':'resize:none;'})
    )
    cultural_fit_example = forms.CharField(
        label="請列舉文化契合度的實例",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':6, 'cols':5,'style':'resize:none;'})
    )

class CoverLetterForm(forms.Form):
    company = forms.CharField(
        label="想申請的公司名稱",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    job = forms.CharField(
        label="想應徵的職位名稱",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    attract = forms.CharField(
        label="想應徵的公司吸引你的原因？",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5,'style':'resize:none;'})
    )

    strength = forms.CharField(
        label="你有什麼強項？ 為什麼該公司要選擇你？",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':6, 'cols':5,'style':'resize:none;'})
    )

    example = forms.CharField(
        label="請列舉你的強項",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':6, 'cols':5,'style':'resize:none;'})
    )

class RecommendationLetterForm(forms.Form):
    self = forms.CharField(
        label="被推薦人稱呼",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    recommender = forms.CharField(
        label="推薦人職稱",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    position = forms.CharField(
        label="推薦到的單位",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    experience = forms.CharField(
        label="跟推薦人合作的經驗",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5,'style':'resize:none;'})
    )

    reason = forms.CharField(
        label="請列舉值得被推薦原因",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5,'style':'resize:none;'})
    )

STYLE_CHOICES = [
    ('', '請選擇風格'),
    ('1', '簡約'),
    ('2', '專業'),
    ('3', '創意'),
]
class ResumeForm(ModelForm):
    style = forms.ChoiceField(label='簡歷風格', choices=STYLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = ResumeRecord
        fields = ['personal_education', 'personal_experience', 'skill', 'interest', 'style']
        widgets = {
            'personal_education': forms.Textarea(attrs={'class': 'form-control','rows':1, 'cols':5,'style':'resize:none;'}),
            'personal_experience': forms.Textarea(attrs={'class': 'form-control','rows':1, 'cols':5,'style':'resize:none;'}),
            'skill': forms.Textarea(attrs={'class': 'form-control','rows':1, 'cols':5,'style':'resize:none;'}),
            'interest': forms.Textarea(attrs={'class': 'form-control','rows':1, 'cols':5,'style':'resize:none;'}),
        }
        labels = {
            'personal_education': '最高學歷',
            'personal_experience': '個人經歷',
            'skill': '專長與技能',
            'interest': '工作外的休閒嗜好',
        }

    
class MockInterviewModeForm(forms.Form):
    company = forms.CharField(
        label="要面試的公司",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    job = forms.CharField(
        label="要面試的職位",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    self_introduction = forms.CharField(
        label="個人簡歷",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':10, 'cols':5,'style':'resize:none;'})
    )

    mode = forms.ChoiceField(
        label="選擇模式",
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input form-check-inline'}),
        choices=(
            ('1', '單題模式'),
            ('2', '多題模式'),
        )
    )

class MockInterviewForm(forms.Form):
    answer = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4, 
            'cols': 5, 
            'style': 'resize: none; background-color: #FCE9CF; width: 90%; height: 108px; margin-top: -10px; margin-left: -10px;',
            'placeholder': '輸入回答'
        })
    )