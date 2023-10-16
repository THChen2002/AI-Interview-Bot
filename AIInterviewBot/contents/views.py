from django.shortcuts import render
from contents.service import ContentsService
from contents.forms import CoverLetterForm, MockInterviewForm, RecommendationLetterForm, ResumeForm, SelfIntroductionForm

def self_introduction(request):
    if request.method == 'POST':
        form = SelfIntroductionForm(request.POST)
        messages=[{
            "role": "user",
            "content": "嗨你好"
        }]
        replyMsg = ContentsService.get_reply_s(messages)
        return render(request, 'contents/self_introduction.html', locals())
    else:
        form = SelfIntroductionForm()
    return render(request, 'contents/self_introduction.html', locals())

def cover_letter(request):
    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
    else:
        form = CoverLetterForm()
    return render(request, 'contents/cover_letter.html', locals())

def recommendation_letter(request):
    if request.method == 'POST':
        form = RecommendationLetterForm(request.POST)
    else:
        form = RecommendationLetterForm()
    return render(request, 'contents/recommendation_letter.html', locals())

def resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
    else:
        form = ResumeForm()
    return render(request, 'contents/resume.html', locals())

def mock_interview(request):
    if request.method == 'POST':
        form = MockInterviewForm(request.POST)
    else:
        form = MockInterviewForm()
    return render(request, 'contents/mock_interview.html', locals())
