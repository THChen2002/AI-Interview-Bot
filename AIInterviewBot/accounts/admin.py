from django.contrib import admin
from .models import UserProfile

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
	list_display = ("username" ,"gender" ,"birth_date" ,"degree")
	search_fields=('id','user__username')
admin.site.register(UserProfile, AccountAdmin)