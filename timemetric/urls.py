from django.conf.urls import url,include
from . import views

app_name = 'timemetric'
urlpatterns = [
url(r'^$',views.index,name='index'),
url(r'^oldsheets/$',views.oldsheet,name='oldsheet'),
url(r'^leaves/$',views.render_leave_register,name='leave'),
url(r'^oldsheets/(?P<uid>\d+)/(?P<dt>\d{4}-\d{2}-\d{2})/$',views.render_oldsheet,name='render_oldsheet'),
]
