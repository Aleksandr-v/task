from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'status', 'date')
    fields = ('sender', 'body', 'status')


admin.site.register(Message, MessageAdmin)
