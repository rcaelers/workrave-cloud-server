from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers

from . import models

class ConfigurationSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = models.Configuration
        fields = ('owner', 'created', 'configuration')

        
class StateSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source='owner.username')
    
    class Meta:
        model = models.State
        fields = ('owner', 'created', 'time', 'timezone', 'state')
        depth = 1

        
class BreakStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BreakStatistics
       
        
class StatisticsSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source='owner.username')
    micro_break = BreakStatisticsSerializer()
    rest_break = BreakStatisticsSerializer()
    daily_limit = BreakStatisticsSerializer()
    
    class Meta:
        model = models.Statistics
        fields = ( 'owner', 'created', 'date', 'start_time', 'stop_time', 
                   'total_active_time', 'total_click_movement', 'total_mouse_movement', 
                   'total_movement_time', 'total_clicks', 'total_keystrokes', 
                   'micro_break', 'rest_break', 'daily_limit' )

        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        view_name = 'cloud:user-detail'
        fields = ('url', 'username', 'email')

        
        
