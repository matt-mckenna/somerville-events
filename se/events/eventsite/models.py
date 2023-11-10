# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .constants import CATEGORY_TAGS, NEIGHBORHOOD_TAGS

class Event(models.Model):

    name = models.CharField(u'Event Name', max_length=100, help_text=u'Event Name', default='Event')
    start_day = models.DateField(u'Start day of the event', help_text=u'Start date of the event')
    end_day = models.DateField(u'End day of the event', help_text=u'End date of the event', null=True, blank=True)
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'End time', help_text=u'End time', null=True, blank=True)
    additional_info = models.TextField(u'Additoinal Info', help_text=u'Additional info', blank=True, null=True)

    tag1 = models.CharField(
            max_length=20,
            choices=CATEGORY_TAGS,
            help_text=u'Tags', 
            null=True, 
            blank=True)
    
    tag2 = models.CharField(
            max_length=20,
            choices=CATEGORY_TAGS,
            help_text=u'Tags', 
            null=True, 
            blank=True)
    
    tag3 = models.CharField(
            max_length=20,
            choices=CATEGORY_TAGS,
            help_text=u'Tags', 
            null=True, 
            blank=True)
    
    neighborhood = models.CharField(
            max_length=40,
            choices=NEIGHBORHOOD_TAGS,
            help_text=u'Neighborhood', 
            null=True, 
            blank=True)

    class Meta:
        verbose_name = u'Events'
        verbose_name_plural = u'Events'