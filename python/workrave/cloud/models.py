from django.db import models

class Client(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='+', blank=True, unique=True)
    last_seen = models.DateTimeField()
    uuid = models.CharField(max_length=32, unique=True)

    
class State(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='state', blank=True, unique=True)
    time = models.DateTimeField()
    timezone = models.IntegerField()
    active = models.CharField(max_length=36)
    state = models.TextField()
    
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
    total_active_time = models.IntegerField(default=0)
    total_mouse_movement = models.IntegerField(default=0)
    total_click_movement = models.IntegerField(default=0)
    total_mouse_movement = models.IntegerField(default=0)
    total_movement_time = models.IntegerField(default=0)
    total_clicks =  models.IntegerField(default=0)
    total_keystrokes = models.IntegerField(default=0)

    micro_break = models.ForeignKey('BreakStatistics', related_name='+')
    rest_break = models.ForeignKey('BreakStatistics', related_name='+')
    daily_limit = models.ForeignKey('BreakStatistics', related_name='+')

    def __unicode__(self):
        return '%s' % self.date
    
    class Meta:
        ordering = ('created',)

        
class BreakStatistics(models.Model):
    prompted = models.IntegerField(default=0)
    taken = models.IntegerField(default=0)
    natural_taken = models.IntegerField(default=0)
    skipped = models.IntegerField(default=0)
    postponed = models.IntegerField(default=0)
    unique = models.IntegerField(default=0)
    total_overdue = models.IntegerField(default=0)
        
