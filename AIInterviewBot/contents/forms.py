from django import forms

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
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
    )
    cultural_fit_example = forms.CharField(
        label="針對文化契合度的舉例",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
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
        label="為什麼想申請應徵的公司吸引你？",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
    )

    strength = forms.CharField(
        label="你有什麼強項？\n為什麼該公司要選擇你？",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
    )

    example = forms.CharField(
        label="你的強項的實際舉例",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
    )

class RecommendationLetterForm(forms.Form):
    self = forms.CharField(
        label="被推薦人稱呼",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    recommender = forms.CharField(
        label="推薦人稱呼",
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
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
    )

    reason = forms.CharField(
        label="為何被推薦人值得被推薦",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
    )
    
    example = forms.CharField(
        label="推薦理由的實際舉例",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
    )

class ResumeForm(forms.Form):
    personal_experience = forms.CharField(
        label="輸入個人經歷",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':1, 'cols':5})
    )

    skill = forms.CharField(
        label="輸入專長與技能",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':1, 'cols':5})
    )

    enthusiasm = forms.CharField(
        label="輸入職涯熱情所在",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':1, 'cols':5})
    )

    interest = forms.CharField(
        label="工作外的休閒嗜好",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':1, 'cols':5})
    )

    style = forms.CharField(
        label="個人簡介風格",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control','rows':1, 'cols':5})
    )
    
class MockInterviewForm(forms.Form):
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
        widget=forms.Textarea(attrs={'class': 'form-control','rows':4, 'cols':5})
    )

    mode = forms.ChoiceField(
        label="選擇模式",
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input form-check-inline'}),
        choices=(
            ('1', '單選模式'),
            ('2', '複選模式'),
        )
    )
