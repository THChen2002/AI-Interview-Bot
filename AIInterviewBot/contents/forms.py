from django import forms

class SelfIntroductionForm(forms.Form):
    company = forms.CharField(
        label="要面試的公司",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    job = forms.CharField(
        label="要面試的職業",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    skill1 = forms.CharField(
        label="個人專長1",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    skill2 = forms.CharField(
        label="個人專長2",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cultural_fit = forms.CharField(
        label="與要面試的公司文化契合點",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cultural_fit_example = forms.CharField(
        label="針對文化契合度的舉例",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
    )


class MockInterviewForm(forms.Form):
    company = forms.CharField(
        label="要面試的公司",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    job = forms.CharField(
        label="要面試的職業",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    experience= forms.CharField(
        label="個人經歷",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    question = forms.CharField(
        label="問題",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    answer = forms.CharField(
        label="回答",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )



class RecommendationLetterForm(forms.Form):
    referee = forms.CharField(
        label="被推薦人稱呼",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    referrer = forms.CharField(
        label="推薦人的稱呼",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    job = forms.CharField(
        label="推薦到的單位",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    experience = forms.CharField(
        label="跟被推薦人的合作經驗",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    reason = forms.CharField(
        label="為何被推薦人值得被推薦",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    example = forms.CharField(
        label="推薦理由的實際舉例",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
class CoverLetter(forms.Form):
    company = forms.CharField(
        label="想申請的公司名稱",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    job = forms.CharField(
        label="想應徵的職稱名稱",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    reason = forms.CharField(
        label="為什麼想申請應徵的公司吸引你?",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    strengths = forms.CharField(
        label="你有什麼強項?為什麼該公司要選擇你?",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    example = forms.CharField(
        label="你強項實際舉例",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )