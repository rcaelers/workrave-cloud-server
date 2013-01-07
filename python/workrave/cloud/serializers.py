from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers

from . import models

class ConfigurationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = models.Configuration
        fields = ('created', 'owner', 'configuration')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    configuration = serializers.ManyHyperlinkedRelatedField(view_name='configuration-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'configuration')
