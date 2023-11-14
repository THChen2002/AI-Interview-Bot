from django.contrib import admin
from .models import UserProfile, ProblemReport

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
	list_display = ("id", "username", "email", "degree", "date_joined")
	search_fields=("id", "username")
	list_filter=("gender", "degree", "date_joined")

class ProblemReportAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "type", "created_at")
	list_filter=("type", "user", "created_at")
	
admin.site.register(UserProfile, AccountAdmin)
admin.site.register(ProblemReport, ProblemReportAdmin)