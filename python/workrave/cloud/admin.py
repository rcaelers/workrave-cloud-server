from django.contrib import admin
from models import Configuration, State, Statistics, BreakStatistics

class StateAdmin(admin.ModelAdmin):    
    list_display = ('time', 'owner', )
    #list_display_links = ('title',)
    #search_fields = ('title', 'name', 'description')
    
class ConfigurationAdmin(admin.ModelAdmin):    
    list_display = ('created', 'owner', )
    #raw_id_fields = ('user',)
    #list_filter = ('user',)

admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Statistics)
admin.site.register(BreakStatistics)
