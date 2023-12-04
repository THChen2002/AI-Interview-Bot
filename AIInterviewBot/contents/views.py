from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from contents.service import ContentsService
from contents.forms import CoverLetterForm, MockInterviewModeForm, MockInterviewForm, RecommendationLetterForm, ResumeForm, SelfIntroductionForm
from contents.models import InterviewQuestion, InterviewRecord, InterviewScore, DashBoard, ContentRecord, ResumeRecord
from django.http import FileResponse, JsonResponse
import os
import json
import uuid,calendar
from datetime import datetime, timedelta
from django.core.files import File
from random import sample
from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model
User = get_user_model()

# 求職信頁面
@login_required(login_url="Login")
def cover_letter(request):
    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            job = form.cleaned_data['job']
            attract = form.cleaned_data['attract']
            strength = form.cleaned_data['strength']
            example = form.cleaned_data['example']
            user_prompt = {
                "role": "user",
                "content": "你現在想要要應徵 " + company + "的" + job  +",這間公司吸引你的原因是" + attract + "而你的強項以及你認為公司為何錄取你的原因是" + strength + "實際的例子有" + example + "請您撰寫一份出色的求職信,並盡可能具備以下3個要點:\n1.開頭精簡、結尾推銷\n2.「關鍵字」在中間的佈局最為重要，可利用重點式說明優勢與經歷，以方便對方閱讀。\n3.「關鍵字」都必須與企業職缺的工作敘述有連結性，沒有連結性的部分可省略"
            }
            messages = ContentsService.get_messages(user_prompt)
            replyMsg = ContentsService.get_reply(messages)
            content = ContentRecord.objects.create(user=request.user, content_type='CL', unit=company, result=replyMsg, is_satisfied=False)
        return JsonResponse({'status': True, 'content_id': content.id})
    else:
        form = CoverLetterForm()
    return render(request, 'contents/cover_letter.html', locals())

# 推薦信頁面
@login_required(login_url="Login")
def recommendation_letter(request):
    if request.method == 'POST':
        form = RecommendationLetterForm(request.POST)
        if form.is_valid():
            self = form.cleaned_data['self']
            recommender = form.cleaned_data['recommender']
            position = form.cleaned_data['position']
            experience = form.cleaned_data['experience']
            reason = form.cleaned_data['reason']
            user_prompt = {
                "role": "user",
                "content": "今天你是" + self + "的推薦人" + recommender + "您要將他推薦到" + position + "，您與推薦人的合作經驗是" + experience + "，您推薦他的原因是推薦人" + reason + "，請您為推薦人撰寫一份推薦信。"
            }
            messages = ContentsService.get_messages(user_prompt)
            replyMsg = ContentsService.get_reply(messages)
            content = ContentRecord.objects.create(user=request.user, content_type='RL', unit=position, result=replyMsg, is_satisfied=False)
        return JsonResponse({'status': True, 'content_id': content.id})
    else:
        form = RecommendationLetterForm()
    return render(request, 'contents/recommendation_letter.html', locals())

# 自我介紹頁面
@login_required(login_url="Login")
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
            content = ContentRecord.objects.create(user=request.user, content_type='SI', unit=company, result=replyMsg, is_satisfied=False)
        return JsonResponse({'status': True, 'content_id': content.id})
    else:
        form = SelfIntroductionForm()
    return render(request, 'contents/self_introduction.html', locals())

#生成結果頁面
@login_required(login_url="Login")
def content_result(request, type):
    if request.method == 'POST':
        content_id = request.POST.get('content_id')
        content = request.POST.get('content')
        is_satisfied = request.POST.get('is_satisfied').lower() == 'true'
        record = ContentRecord.objects.get(id=content_id)
        record.result = content
        record.is_satisfied = is_satisfied
        record.save()
        return JsonResponse({'status': True})
    else:
        content_id = request.GET.get('content_id')
        record = get_object_or_404(ContentRecord, id=content_id)
    return render(request, 'contents/content_result.html', locals())


# 履歷頁面
@login_required(login_url="Login")
def resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            unit = User.objects.get(id=request.user.id)
            resume = {
                'name' :unit.first_name + unit.last_name,
                'gender' :unit.get_gender_display() if unit.get_gender_display() else '',
                'birth_date' :unit.birth_date.strftime("%Y/%m/%d") if unit.birth_date else '',
                'education': form.cleaned_data['personal_education'],
                'email' :unit.email,
                'personal_experience': form.cleaned_data['personal_experience'],
                'skill': form.cleaned_data['skill'],
                'interest': form.cleaned_data['interest'],
                'style': form.cleaned_data['style'],
            }
            user_prompt = {
                "role": "user",
                "content": "你要完成一份約150字簡單的個人簡介內容開頭無需「個人簡介」四字，你的個人經驗是" + resume['personal_experience'] + "，而你的專長與技能是" + resume['skill'] + "，另外你工作外的休閒嗜好是" + resume['interest']
            }
            messages = ContentsService.get_messages(user_prompt)
            resume['self_introduction'] = ContentsService.get_reply(messages)
            
            # 儲存履歷檔案到使用者對應的資料夾
            folder_path = os.path.join(settings.MEDIA_ROOT, 'resume', request.user.username)
            file_name = f"{str(uuid.uuid4())[:8]}_resume.docx"
            file_path = os.path.join(folder_path, file_name)
            # 確認改使用者的資料夾是否存在，不存在則創建
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            ContentsService.export_resume(resume, file_path)

            # 儲存履歷紀錄
            resume_record = form.save(commit=False)
            resume_record.user = request.user
            resume_record.resume_file = os.path.join('resume', file_path)
            resume_record.save()
            return JsonResponse({'file_name': file_name})
    else:
        form = ResumeForm()
    return render(request, 'contents/resume.html', locals())

# 模擬面試頁面
@login_required(login_url="Login")
def mock_interview_mode(request):
    if request.method == 'POST':
        form = MockInterviewModeForm(request.POST)
        if form.is_valid():
            mode = form.cleaned_data['mode']
            company = form.cleaned_data['company']
            request.session['company'] = company
            return redirect(reverse("MockInterview", kwargs={'mode': mode}))
    else:
        form = MockInterviewModeForm()
    return render(request, 'contents/mock_interview_mode.html', locals())

# 模擬面試過程頁面
@login_required(login_url="Login")
def mock_interview(request, mode):
    amount = 1
    # 多題模式
    if mode == '2':
        amount = 3
    questions = sample(list(InterviewQuestion.objects.all()), amount)
    form = MockInterviewForm()
    return render(request, 'contents/mock_interview.html', locals())

# 模擬面試結果頁面
@login_required(login_url="Login")
def mock_interview_result(request):
    if request.method == 'POST':
        records = json.loads(request.POST.get('records'))
        saved_records = []
        messages=[
            { 
            "role": "system",
            "content": "You are an excellent interviewer.\n 需要有以下這些欄位，professional_score,professional_suggestion,creative_score,creative_suggestion,strategy_score,strategy_suggestion,communication_score,communication_suggestion,self_learning_score,self_learning_suggestion,comprehensive_score,comprehensive_suggestion，請用標準的json格式回傳，除了字串內可以換行其餘不要有換行符號"
            },
            {
            "role": "user",
            "content": "你現在是個面試官,您給予面試者一些問題，請你根據以下求職者的回答整理給予綜合評分,同時請依照下方的的5點的評分標準嚴格給予面試者的回答各項目確切分數並回饋。\n\n1.專業能力評分標準：\n0-30分:展示出缺乏基本的領域知識和技能,無法適應相關情境。\n31-60分:擁有基本的專業知識，但在應用和解釋方面可能需要進一步的發展。\n61-90分:具備堅實的領域知識和技能,能夠有效應用於不同情境,並提供有價值的洞察和解決方案。\n91-100分:展現出卓越的專業知識和技能，能夠在複雜的情況下提供創新和高效的解決方案，對領域有深刻的理解。\n\n2.創意能力評分標準：\n0-30分:缺乏創意思維,難以提供新穎或獨特的解決方案。\n31-60分:能夠在某些情境下提出一些創意想法，但可能需要更多的多元思考。\n61-90分:展現出在解決問題時能夠提供創意解決方案，能夠從不同角度思考並提供獨特的見解。\n91-100分:具備高度創意思維,能夠在各種情境下提供極具創新性和實用性的解決方案。\n\n3.策略能力評分標準：\n0-30分:缺乏有效的計劃和目標，難以制定明確的行動步驟。\n31-60分:能夠制定一般的計劃,但可能需要更多的分析和策略性思考。\n61-90分:具備有效的策略思維,能夠考慮多個因素並制定有系統的行動計劃。\n91-100分:展示出卓越的策略能力,能夠在複雜情境下制定高效且有效的長遠計劃和目標。\n\n4.溝通能力評分標準：\n0-30分:表達不清晰,難以有效地傳達信息和意圖。\n31-60分:能夠基本表達想法,但可能需要更多的組織和結構。\n61-90分:具備清晰、適切和有力的溝通技巧,能夠在團隊內外有效地傳達信息。\n91-100分:展現出優秀的溝通能力,能夠以影響力和說服力與他人交流和協作。\n\n5.自主學習能力評分標準：\n0-30分:缺乏持續學習的動機,無法主動探索新知識和技能。\n31-60分:能夠在一些情境下展示出主動學習的態度.但可能需要更積極地提升。\n61-90分:具備持續自我提升的意願,能夠積極地學習新知識和技能。\n91-100分:展現出卓越的自主學習能力,能夠不斷掌握新知識,並將其應用於不同領域。\n不需要都給5為單位的分數，只要是整數分數即可，如83分。"
            }
        ]
        # 包個transaction，避免API請求失敗時，資料庫紀錄不一致(record已建立，但score未建立)
        with transaction.atomic():
            for record in records:
                question_id = record['id']
                question = InterviewQuestion.objects.get(id=question_id).question
                answer = record['answer']
                messages.append({
                    "role": "user",
                    "content": "題目為" + question + "，回答為" + answer
                })
                # 創建回答紀錄並存入saved_records
                saved_records.append(InterviewRecord.objects.create(user=request.user, question_id=question_id, answer=answer))
            replyMsg = ContentsService.get_reply(messages)
            response_data = json.loads(replyMsg)
            # 創建評分紀錄
            interview_score = InterviewScore.objects.create(
                user=request.user,
                unit=request.session.get('company', ''),
                professional_score=response_data['professional_score'],
                professional_suggestion=response_data['professional_suggestion'],
                creative_score=response_data['creative_score'],
                creative_suggestion=response_data['creative_suggestion'],
                strategy_score=response_data['strategy_score'],
                strategy_suggestion=response_data['strategy_suggestion'],
                communication_score=response_data['communication_score'],
                communication_suggestion=response_data['communication_suggestion'],
                self_learning_score=response_data['self_learning_score'],
                self_learning_suggestion=response_data['self_learning_suggestion'],
                comprehensive_score=response_data['comprehensive_score'],
                comprehensive_suggestion=response_data['comprehensive_suggestion'],
            )
            # 設定評分紀錄的回答紀錄
            interview_score.records.set(saved_records)
            return JsonResponse({'status': True, 'score_id': interview_score.id})
    else:
        score_id = request.GET.get('score_id')
        interviewScore = get_object_or_404(InterviewScore, id=score_id)
    return render(request, 'contents/mock_interview_result.html', locals())

# 儀表板頁面
@login_required(login_url="Login")
def dashboard(request):
    dashboard = DashBoard.objects.get(id=request.user.id)
    return render(request, 'contents/dashboard.html', locals())

#歷史紀錄頁面
@login_required(login_url="Login")
def history(request):
    cover_letter_records = ContentRecord.objects.filter(user=request.user, content_type='CL')
    recommendation_letter_records = ContentRecord.objects.filter(user=request.user, content_type='RL')
    self_introduction_records = ContentRecord.objects.filter(user=request.user, content_type='SI')
    resume_records = ResumeRecord.objects.filter(user=request.user)
    mock_interview_records = InterviewScore.objects.filter(user=request.user)
    date_filter = request.GET.get('date')
    # 獲取選擇的頁籤(預設為cover_letter)
    selected_tab = request.GET.get('tab', 'cover_letter')
    # 獲取排序方式(預設為desc)
    order = request.GET.get('order', 'desc')
    if order == 'desc':
        cover_letter_records = cover_letter_records.order_by('-created_at')
        recommendation_letter_records = recommendation_letter_records.order_by('-created_at')
        self_introduction_records = self_introduction_records.order_by('-created_at')
        resume_records = resume_records.order_by('-created_at')
        mock_interview_records = mock_interview_records.order_by('-created_at')

    if date_filter:
        today = datetime.now().date()
        start_date, end_date = None, None

        if date_filter == 'today':
            start_date = today
            end_date = start_date + timedelta(days=1)
        elif date_filter == 'week':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=7)
        elif date_filter == 'month':
            start_date = today.replace(day=1)
            _, last_day = calendar.monthrange(start_date.year, start_date.month)
            end_date = start_date.replace(day=last_day)
        elif date_filter == 'year':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)

        cover_letter_records = cover_letter_records.filter(created_at__date__range=[start_date, end_date])
        recommendation_letter_records = recommendation_letter_records.filter(created_at__date__range=[start_date, end_date])
        self_introduction_records = self_introduction_records.filter(created_at__date__range=[start_date, end_date])
        resume_records = resume_records.filter(created_at__date__range=[start_date, end_date])
        mock_interview_records = mock_interview_records.filter(created_at__date__range=[start_date, end_date])

    return render(request, 'contents/history.html', locals())

# 歷史紀錄詳細頁面
@login_required(login_url="Login")
def history_detail(request):
    type = request.GET.get('type')
    record_id = request.GET.get('id')
    history = True
    # 取得該筆紀錄
    if type == 'MI':
        interviewScore = InterviewScore.objects.get(id=record_id)
        return render(request, 'contents/mock_interview_result.html', locals())
    elif type == 'R':
        record = ResumeRecord.objects.get(id=record_id)
        file_name = os.path.basename(record.resume_file.path)
        form = ResumeForm(instance=record)
        return render(request, 'contents/resume.html', locals())
    else:
        record = ContentRecord.objects.get(id=record_id)
    return render(request, 'contents/history_detail.html', locals())

# 取得儀表板資訊
def get_chart_data(request):
    chart_type = request.GET.get('type')
    dashboard = DashBoard.objects.get(id=request.user.id)
    if chart_type == 'line':
        data = {
            'labels': [record.created_at.strftime("%m/%d") for record in dashboard.score_records.all()],
            'datasets': [
                {
                    'label': '專業能力',
                    'data': [record.professional_score for record in dashboard.score_records.all()],
                    'borderWidth': 1,
                }, 
                {
                    'label': '創意能力',
                    'data': [record.creative_score for record in dashboard.score_records.all()],
                    'borderWidth': 1,
                },
                {
                    'label': '策略能力',
                    'data': [record.strategy_score for record in dashboard.score_records.all()],
                    'borderWidth': 1,
                },
                {
                    'label': '溝通能力',
                    'data': [record.communication_score for record in dashboard.score_records.all()],
                    'borderWidth': 1,
                },
                {
                    'label': '自主學習能力',
                    'data': [record.self_learning_score for record in dashboard.score_records.all()],
                    'borderWidth': 1,
                },
                {
                    'label': '綜合能力',
                    'data': [record.comprehensive_score for record in dashboard.score_records.all()],
                    'borderWidth': 1,
                }
            ]
        }
    elif chart_type == 'radar':
        data = {
            'labels': ['專業能力', '創意能力', '策略能力', '溝通能力', '自主學習能力'],
            'datasets': [{
                'label': '專業能力',
                'data': [dashboard.professional_score, dashboard.creative_score, dashboard.strategy_score, dashboard.communication_score, dashboard.self_learning_score],
            }]
        }
    return JsonResponse({'data': data})

# 下載檔案
def download_file(request):
    file_name = request.POST.get('file_name')
    file_path = os.path.join(settings.MEDIA_ROOT, 'resume', request.user.username, file_name)
    # file_name = os.path.basename(file_path)
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response