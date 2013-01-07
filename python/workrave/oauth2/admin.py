from django.contrib import admin
from models import Scope, Client, CodeGrant, Token

class ScopeAdmin(admin.ModelAdmin):    
    list_display = ('title', 'name', )
    list_display_links = ('title',)
    search_fields = ('title', 'name', 'description')

class ClientAdmin(admin.ModelAdmin):    
    list_display = ('name', 'user', 'description', )
    raw_id_fields = ('user',)
    list_filter = ('user',)

class CodeGrantAdmin(admin.ModelAdmin):
    list_display = ('create_date', 'user', 'client', 'expires', 'tagline')
    raw_id_fields = ('user', )
    search_fields = ('user', 'access_token', 'refresh_token', 'tagline', 'description')
    ordering = ('-create_date',)
    date_hierarchy = 'create_date'    
    list_filter = ('user',)
        
class TokenAdmin(admin.ModelAdmin):
    list_display = ('create_date', 'user', 'client', 'expires', 'tagline')
    raw_id_fields = ('user', )
    search_fields = ('user', 'access_token', 'refresh_token', 'tagline', 'description')
    ordering = ('-create_date',)
    date_hierarchy = 'create_date'    
    list_filter = ('user',)

admin.site.register(Scope, ScopeAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(CodeGrant, CodeGrantAdmin)
admin.site.register(Token, TokenAdmin)
