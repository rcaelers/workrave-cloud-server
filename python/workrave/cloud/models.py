from django.db import models

class Configuration(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='configuration', blank=True, unique=True)
    configuration = models.TextField()

    class Meta:
        ordering = ('created',)
