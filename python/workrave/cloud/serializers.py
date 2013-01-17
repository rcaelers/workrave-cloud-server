from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers

from . import models

class ConfigurationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = models.Configuration
        view_name = 'cloud:configuration-detail'
        fields = ('url', 'created', 'owner', 'configuration')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    configuration = serializers.ManyHyperlinkedRelatedField(view_name='cloud:configuration-detail')

    class Meta:
        model = User
        view_name = 'cloud:user-detail'
        fields = ('url', 'username', 'email', 'configuration')

class StateSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')
    
    class Meta:
        model = models.State
        fields = ('url', 'created', 'owner', 'time', 'timezone', 'micro_break', 'rest_break', 'daily_limit')
        depth = 1

        
class StatisticsSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = models.Statistics
        depth = 1
        
