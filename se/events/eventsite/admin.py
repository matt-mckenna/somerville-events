# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.contrib import admin
from eventsite.models import Event
 
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_day', 'end_day', 'start_time', 'end_time', 'additional_info']

admin.site.register(Event, EventAdmin)