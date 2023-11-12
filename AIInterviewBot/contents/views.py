from django.shortcuts import render,redirect
from django.urls import reverse
from contents.service import ContentsService
from contents.forms import CoverLetterForm, MockInterviewModeForm, MockInterviewForm, RecommendationLetterForm, ResumeForm, SelfIntroductionForm
from contents.models import InterviewQuestion, InterviewRecord, InterviewScore
from django.http import FileResponse, JsonResponse
import os
import json
from random import sample

# 自我介紹頁面
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
            user_prompt = {
                "role": "user",
                "content": "你現在即將要面是" + company + "的" + job +"一職,我的個人專長是" + skill1 + "和" + skill2 + "而我與貴公司文化契合點是" + cultural_fit + "實際的例子是" + cultural_fit_example
            }
            messages = ContentsService.get_messages(user_prompt)
            replyMsg = ContentsService.get_reply(messages)
        return render(request, 'contents/self_introduction.html', locals())
    else:
        form = SelfIntroductionForm()
    return render(request, 'contents/self_introduction.html', locals())

# 模擬面試頁面
def mock_interview(request):
    if request.method == 'POST':
        form = MockInterviewModeForm(request.POST)
        if form.is_valid():
            mode = form.cleaned_data['mode']
            return redirect(reverse("MockInterviewMode", kwargs={'mode':mode}))
    else:
        form = MockInterviewModeForm(request.POST)
    return render(request, 'contents/mock_interview.html', locals())

# 模擬面試過程頁面
def mock_interview_mode(request, mode):
    amount = 1
    # 多題模式
    if mode == '2':
        amount = 3
    questions = sample(list(InterviewQuestion.objects.all()), amount)
    form = MockInterviewForm()
    return render(request, 'contents/mock_interview_mode.html', locals())

def mock_interview_result(request):
    if request.method == 'POST':
        records = json.loads(request.POST.get('records'))
        saved_records = []
        for record in records:
            question = record['id']
            answer = record['answer']
            # 創建回答紀錄並存入saved_records
            saved_records.append(InterviewRecord.objects.create(user=request.user, question_id=question, answer=answer))
        # 創建評分紀錄
        interview_score = InterviewScore.objects.create(
            user=request.user,
            professional_score=0,
            professional_suggestion="",
            creative_score=0,
            creative_suggestion="",
            strategy_score=0,
            strategy_suggestion="",
            communication_score=0,
            communication_suggestion="",
            self_learning_score=0,
            self_learning_suggestion="",
            comprehensive_score=0,
            comprehensive_suggestion=""
        )
        # 設定評分紀錄的回答紀錄
        interview_score.records.set(saved_records)
        # messages=[
        #     { 
        #     "role": "system",
        #     "content": "You are an excellent interviewr.\n"
        #     },
        #     {
        #     "role": "user",
        #     "content": "你現在是的面試官,您給予面試者一道問題,題目為" + question + "請你根據以下求職者的回答整理給予綜合評分,同時請依照下方的的5點的評分標準嚴格給予面試者的回答各項目確切分數並回饋。\n\n1.專業能力評分標準：\n0-30分:展示出缺乏基本的領域知識和技能,無法適應相關情境。\n31-60分:擁有基本的專業知識，但在應用和解釋方面可能需要進一步的發展。\n61-90分:具備堅實的領域知識和技能,能夠有效應用於不同情境,並提供有價值的洞察和解決方案。\n91-100分:展現出卓越的專業知識和技能，能夠在複雜的情況下提供創新和高效的解決方案，對領域有深刻的理解。\n\n2.創意能力評分標準：\n0-30分:缺乏創意思維,難以提供新穎或獨特的解決方案。\n31-60分:能夠在某些情境下提出一些創意想法，但可能需要更多的多元思考。\n61-90分:展現出在解決問題時能夠提供創意解決方案，能夠從不同角度思考並提供獨特的見解。\n91-100分:具備高度創意思維,能夠在各種情境下提供極具創新性和實用性的解決方案。\n\n3.策略能力評分標準：\n0-30分:缺乏有效的計劃和目標，難以制定明確的行動步驟。\n31-60分:能夠制定一般的計劃,但可能需要更多的分析和策略性思考。\n61-90分:具備有效的策略思維,能夠考慮多個因素並制定有系統的行動計劃。\n91-100分:展示出卓越的策略能力,能夠在複雜情境下制定高效且有效的長遠計劃和目標。\n\n4.溝通能力評分標準：\n0-30分:表達不清晰,難以有效地傳達信息和意圖。\n31-60分:能夠基本表達想法,但可能需要更多的組織和結構。\n61-90分:具備清晰、適切和有力的溝通技巧,能夠在團隊內外有效地傳達信息。\n91-100分:展現出優秀的溝通能力,能夠以影響力和說服力與他人交流和協作。\n\n5.自主學習能力評分標準：\n0-30分:缺乏持續學習的動機,無法主動探索新知識和技能。\n31-60分:能夠在一些情境下展示出主動學習的態度.但可能需要更積極地提升。\n61-90分:具備持續自我提升的意願,能夠積極地學習新知識和技能。\n91-100分:展現出卓越的自主學習能力,能夠不斷掌握新知識,並將其應用於不同領域。""\n\n面試者的回答:"+ answer 
        #     }
        # ]
        # replyMsg = ContentsService.get_reply_s(messages)
        return JsonResponse({'status': True, 'score_id': interview_score.id})
    else:
        score_id = request.GET.get('score_id')
        # questionScore = InterviewScore.objects.get(id=score_id)
    return render(request, 'contents/mock_interview_result.html', locals())

# 推薦信頁面
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
            user_prompt = {
                "role": "user",
                "content": "今天你是" + referee + "的推薦人" + referrer + "您要將他推薦到" + department + "，您與推薦人的合作經驗是" + experience + "，您推薦他的原因是推薦人" + reason + "實際的例子有" + example + "，請您為推薦人撰寫一份推薦信。"
            }
            messages = ContentsService.get_messages(user_prompt)
            replyMsg = ContentsService.get_reply_s(messages)
        return render(request, 'contents/recommendation_letter.html', locals())
    else:
        form = RecommendationLetterForm()
    return render(request, 'contents/recommendation_letter.html', locals())

# 求職信頁面
def cover_letter(request):
    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            job = form.cleaned_data['job']
            reason = form.cleaned_data['reason']
            strengths = form.cleaned_data['strengths']
            example = form.cleaned_data['example']
            user_prompt = {
                "role": "user",
                "content": "你現在想要要應徵 " + company + "的" + job  +",這間公司吸引你的原因是" + reason + "而你的強項以及你認為公司為何錄取你的原因是" + strengths + "實際的例子有" + example + "請您撰寫一份出色的求職信,並盡可能具備以下3個要點:\n1.開頭精簡、結尾推銷\n2.「關鍵字」在中間的佈局最為重要，可利用重點式說明優勢與經歷，以方便對方閱讀。\n3.「關鍵字」都必須與企業職缺的工作敘述有連結性，沒有連結性的部分可省略"
            }
            messages = ContentsService.get_messages(user_prompt)
            replyMsg = ContentsService.get_reply_s(messages)
        return render(request, 'contents/cover_letter.html', locals())
    else:
        form = CoverLetterForm()
    return render(request, 'contents/cover_letter.html', locals())

# 履歷頁面
def resume(request):
    output_path = ContentsService.export_resume()
    return download_file(output_path)
    if request.method == 'POST':
        form = ResumeForm(request.POST)
    else:
        form = ResumeForm()
    return render(request, 'contents/resume.html', locals())

# 儀表板頁面
def dashboard(request):
    return render(request, 'contents/dashboard.html', locals())

# 下載檔案
def download_file(file_path):
    file_name = os.path.basename(file_path)
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response