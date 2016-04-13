from django.contrib import admin
from .models import Client,JobType

class ClientModelAdmin(admin.ModelAdmin):
    list_display = ('name','color','colorblock','is_active')

    def colorblock(self,obj):
        return '<div style="width:50px;height:20px;background-color:%s"> </div>' % obj.color
    colorblock.allow_tags = True
    colorblock.allow_tags = 'Hope you are not color blind'

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','color','is_active')} 
        ),
    )

class JobtypeModelAdmin(admin.ModelAdmin):
    list_display = ('name','is_miscellaneous',)

admin.site.register(Client,ClientModelAdmin)
admin.site.register(JobType,JobtypeModelAdmin)
    
