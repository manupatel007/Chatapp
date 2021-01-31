from django.contrib import admin
from .models import ChatData
# Register your models here.

class ChatDataAdmin(admin.ModelAdmin):
    pass

admin.site.register(ChatData,ChatDataAdmin)