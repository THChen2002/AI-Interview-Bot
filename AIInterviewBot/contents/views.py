from django.shortcuts import render
from contents.forms import SelfIntroductionForm
def self_introduction(request):
    form = SelfIntroductionForm()
    return render(request, 'contents/self_introduction.html', locals())