from django.contrib import admin
from .models import UserProfile

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
	list_display = ("id", "username", "email", "degree", "date_joined")
	search_fields=("id", "username")
	list_filter=("gender", "degree", "date_joined")
admin.site.register(UserProfile, AccountAdmin)