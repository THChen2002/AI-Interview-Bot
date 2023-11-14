from django.db import models
from django.utils import timezone
from django.conf import settings
User = settings.AUTH_USER_MODEL

# 生成結果紀錄
class ContentRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CONTENT_TYPE_CHOICES = (
        ('CL', '求職信'),
        ('RL', '推薦信'),
        ('R', '履歷'),
        ('SI', '自我介紹'),
        ('MI', '模擬面試'),
    )
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    result = models.TextField()
    is_satisfied = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

# 模擬面試題庫
class InterviewQuestion(models.Model):
    question = models.CharField(max_length=1000)

    def __str__(self):
        return self.question

# 模擬面試回答紀錄
class InterviewRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + "-" + self.question.question

# 模擬面試評分紀錄
class InterviewScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    records = models.ManyToManyField(InterviewRecord)
    # 專業能力
    professional_score = models.PositiveIntegerField()
    professional_suggestion = models.TextField()
    # 創意能力
    creative_score = models.PositiveIntegerField()
    creative_suggestion = models.TextField()
    # 策略能力
    strategy_score = models.PositiveIntegerField()
    strategy_suggestion = models.TextField()
    # 溝通能力
    communication_score = models.PositiveIntegerField()
    communication_suggestion = models.TextField()
    # 自主學習能力
    self_learning_score = models.PositiveIntegerField()
    self_learning_suggestion = models.TextField()
    # 綜合能力
    comprehensive_score = models.PositiveIntegerField()
    comprehensive_suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 個人儀表板
class DashBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @property
    def score_records(self):
        return InterviewScore.objects.filter(user=self.user)

    @property
    def registration_days(self):
        return (timezone.now() - self.user.date_joined).days

    @property
    def professional_score(self):
        return InterviewScore.objects.filter(user=self.user).aggregate(models.Avg('professional_score'))['professional_score__avg']
    
    @property
    def creative_score(self):
        return InterviewScore.objects.filter(user=self.user).aggregate(models.Avg('creative_score'))['creative_score__avg']
    
    @property
    def strategy_score(self):
        return InterviewScore.objects.filter(user=self.user).aggregate(models.Avg('strategy_score'))['strategy_score__avg']
    
    @property
    def communication_score(self):
        return InterviewScore.objects.filter(user=self.user).aggregate(models.Avg('communication_score'))['communication_score__avg']
    
    @property
    def self_learning_score(self):
        return InterviewScore.objects.filter(user=self.user).aggregate(models.Avg('self_learning_score'))['self_learning_score__avg']
    
    @property
    def comprehensive_score(self):
        return InterviewScore.objects.filter(user=self.user).aggregate(models.Avg('comprehensive_score'))['comprehensive_score__avg']