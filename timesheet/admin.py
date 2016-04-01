from django.contrib import admin
from .models import Client,JobType
from .forms import ClientCreateForm

class ClientModelAdmin(admin.ModelAdmin):
    form = ClientCreateForm
    add_form = ClientCreateForm

    list_display = ('name','color','colorblock')

    def colorblock(self,obj):
        return '<div style="width:50px;height:20px;background-color:%s"> </div>' % obj.color
    colorblock.allow_tags = True
    colorblock.allow_tags = 'Hope you are not color blind'

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','color',)} 
        ),
    )

class JobtypeModelAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Client,ClientModelAdmin)
admin.site.register(JobType,JobtypeModelAdmin)
    
