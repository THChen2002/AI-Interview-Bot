from django.shortcuts import render
from contents.forms import SelfIntroductionForm
from contents.service import ContentsService


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