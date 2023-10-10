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


    