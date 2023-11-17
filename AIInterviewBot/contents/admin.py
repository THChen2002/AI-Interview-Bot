from django.contrib import admin
from .models import ContentRecord, ResumeRecord, InterviewQuestion, InterviewRecord, InterviewScore, DashBoard

class ContentRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'is_satisfied', 'created_at')

class ResumeRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'personal_education', 'skill', 'interest', 'style', 'created_at')

class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')

class InterviewRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'created_at')

class InterviewScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'professional_score', 'creative_score', 'strategy_score', 'communication_score', 'self_learning_score', 'comprehensive_score', 'created_at')

class DashBoardAdmin(admin.ModelAdmin):
    list_display = ('user', 'professional_score', 'creative_score', 'strategy_score', 'communication_score', 'self_learning_score', 'comprehensive_score')

admin.site.register(ContentRecord, ContentRecordAdmin)
admin.site.register(ResumeRecord, ResumeRecordAdmin)
admin.site.register(InterviewQuestion, InterviewQuestionAdmin)
admin.site.register(InterviewRecord, InterviewRecordAdmin)
admin.site.register(InterviewScore, InterviewScoreAdmin)
admin.site.register(DashBoard, DashBoardAdmin)