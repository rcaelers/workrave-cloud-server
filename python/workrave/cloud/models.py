from django.db import models

class State(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='state', blank=True, unique=True)
    time = models.DateTimeField()
    timezone = models.IntegerField()

    class Meta:
        ordering = ('created',)
    
class Configuration(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='configuration', blank=True, unique=True)
    configuration = models.TextField()

    class Meta:
        ordering = ('created',)

class Statistics(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='statistics', blank=False, unique=False)
    date = models.DateField(blank=True,null=True)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    total_active_time = models.IntegerField()
    total_mouse_movement = models.IntegerField()
    total_click_movement = models.IntegerField()
    total_mouse_movement = models.IntegerField()
    total_movement_time = models.IntegerField()
    total_clicks =  models.IntegerField()
    total_keystrokes = models.IntegerField()

    micro_break = models.ForeignKey('BreakStatistics', related_name='+')
    rest_break = models.ForeignKey('BreakStatistics', related_name='+')
    daily_limit = models.ForeignKey('BreakStatistics', related_name='+')

    class Meta:
        ordering = ('created',)
    
class BreakStatistics(models.Model):
    prompted = models.IntegerField()
    taken = models.IntegerField()
    natural_taken = models.IntegerField()
    skipped = models.IntegerField()
    postponed = models.IntegerField()
    unique = models.IntegerField()
    total_overdue = models.IntegerField()
        
