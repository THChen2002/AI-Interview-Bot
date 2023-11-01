from django.shortcuts import render,redirect
from django.urls import reverse
from contents.service import ContentsService
from contents.forms import CoverLetterForm, MockInterviewForm, RecommendationLetterForm, ResumeForm, SelfIntroductionForm

def self_introduction(request):
    if request.method == 'POST':
        form = SelfIntroductionForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            job = form.cleaned_data['job']
            skill1 = form.cleaned_data['skill1']
            skill2 = skill1 = form.cleaned_data['skill2']
            cultural_fit = form.cleaned_data['cultural_fit']
            cultural_fit_example = form.cleaned_data['cultural_fit_example']
            messages=[
                { 
                "role": "system",
                "content": "You are an excellent interviewee and want to apply for work or school."
                },
                {
                "role": "user",
                "content": "你現在即將要面是" + company + "的" + job +"一職,我的個人專長是" + skill1 + "和" + skill2 + "而我與貴公司文化契合點是" + cultural_fit + "實際的例子是" + cultural_fit_example
                }
            ]
            replyMsg = ContentsService.get_reply(messages)
        return render(request, 'contents/self_introduction.html', locals())
    else:
        form = SelfIntroductionForm()
    return render(request, 'contents/self_introduction.html', locals())

def mock_interview(request):
    if request.method == 'POST':
        form = MockInterviewForm(request.POST)
        if form.is_valid():
            mode = form.cleaned_data['mode']
            return redirect(reverse("MockInterviewMode", kwargs={'mode':mode}))
    else:
        form = MockInterviewForm(request.POST)
    return render(request, 'contents/mock_interview.html', locals())

def mock_interview_mode(request, mode):
    return render(request, 'contents/mock_interview_mode.html', locals())

def MockInterviewQuestionForm(request):
    if request.method == 'POST':
        form = MockInterviewQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']
            messages=[
                { 
                "role": "system",
                "content": "You are an excellent interviewr.\n"
                },
                {
                "role": "user",
                "content": "你現在是的面試官,您給予面試者一道問題,題目為" + question + "請你根據以下求職者的回答整理給予綜合評分,同時請依照下方的的5點的評分標準嚴格給予面試者的回答各項目確切分數並回饋。\n\n1.專業能力評分標準：\n0-30分:展示出缺乏基本的領域知識和技能,無法適應相關情境。\n31-60分:擁有基本的專業知識，但在應用和解釋方面可能需要進一步的發展。\n61-90分:具備堅實的領域知識和技能,能夠有效應用於不同情境,並提供有價值的洞察和解決方案。\n91-100分:展現出卓越的專業知識和技能，能夠在複雜的情況下提供創新和高效的解決方案，對領域有深刻的理解。\n\n2.創意能力評分標準：\n0-30分:缺乏創意思維,難以提供新穎或獨特的解決方案。\n31-60分:能夠在某些情境下提出一些創意想法，但可能需要更多的多元思考。\n61-90分:展現出在解決問題時能夠提供創意解決方案，能夠從不同角度思考並提供獨特的見解。\n91-100分:具備高度創意思維,能夠在各種情境下提供極具創新性和實用性的解決方案。\n\n3.策略能力評分標準：\n0-30分:缺乏有效的計劃和目標，難以制定明確的行動步驟。\n31-60分:能夠制定一般的計劃,但可能需要更多的分析和策略性思考。\n61-90分:具備有效的策略思維,能夠考慮多個因素並制定有系統的行動計劃。\n91-100分:展示出卓越的策略能力,能夠在複雜情境下制定高效且有效的長遠計劃和目標。\n\n4.溝通能力評分標準：\n0-30分:表達不清晰,難以有效地傳達信息和意圖。\n31-60分:能夠基本表達想法,但可能需要更多的組織和結構。\n61-90分:具備清晰、適切和有力的溝通技巧,能夠在團隊內外有效地傳達信息。\n91-100分:展現出優秀的溝通能力,能夠以影響力和說服力與他人交流和協作。\n\n5.自主學習能力評分標準：\n0-30分:缺乏持續學習的動機,無法主動探索新知識和技能。\n31-60分:能夠在一些情境下展示出主動學習的態度.但可能需要更積極地提升。\n61-90分:具備持續自我提升的意願,能夠積極地學習新知識和技能。\n91-100分:展現出卓越的自主學習能力,能夠不斷掌握新知識,並將其應用於不同領域。""\n\n面試者的回答:"+ answer 
                }
            ]
            replyMsg = ContentsService.get_reply_s(messages)
        return render(request, 'contents/mock_interview.html', locals())
    else:
        form = MockInterviewQuestionForm(request.POST)
    return render(request, 'contents/mock_interview.html', locals())


def recommendation_letter(request):
    if request.method == 'POST':
        form = RecommendationLetterForm(request.POST)
        if form.is_valid():
            referee = form.cleaned_data['referee']
            referrer = form.cleaned_data['referrer']
            department = form.cleaned_data['department']
            experience = form.cleaned_data['experience']
            reason = form.cleaned_data['reason']
            example = form.cleaned_data['example']
            messages=[
                {
                "role": "system",
                "content": "You are an excellent interviewee and want to apply for work or school."
                },
                {
                "role": "user",
                "content": "今天你是" + referee + "的推薦人" + referrer + "您要將他推薦到" + department + "，您與推薦人的合作經驗是" + experience + "，您推薦他的原因是推薦人" + reason + "實際的例子有" + example + "，請您為推薦人撰寫一份推薦信。"
                },
            ]
            replyMsg = ContentsService.get_reply_s(messages)
        return render(request, 'contents/self_introduction.html', locals())
    else:
        form = SelfIntroductionForm()
    return render(request, 'contents/self_introduction.html', locals())


def cover_letter(request):
    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            job = form.cleaned_data['job']
            reason = form.cleaned_data['reason']
            strengths = form.cleaned_data['strengths']
            example = form.cleaned_data['example']
            messages=[
                {
                "role": "system",
                "content": "You are an excellent interviewee and want to apply for work or school."
                },
                {
                "role": "user",
                "content": "你現在想要要應徵 " + company + "的"+ job  +",這間公司吸引你的原因是" + reason + "而你的強項以及你認為公司為何錄取你的原因是" + strengths + "實際的例子有" + example + "請您撰寫一份出色的求職信,並盡可能具備以下3個要點:\n1.開頭精簡、結尾推銷\n2.「關鍵字」在中間的佈局最為重要，可利用重點式說明優勢與經歷，以方便對方閱讀。\n3.「關鍵字」都必須與企業職缺的工作敘述有連結性，沒有連結性的部分可省略"
                },
            ]
            replyMsg = ContentsService.get_reply_s(messages)
        return render(request, 'contents/self_introduction.html', locals())
    else:
        form = SelfIntroductionForm()
    return render(request, 'contents/self_introduction.html', locals())

def resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
    else:
        form = ResumeForm()
    return render(request, 'contents/resume.html', locals())

def dashboard(request):
    return render(request, 'contents/dashboard.html', locals())

