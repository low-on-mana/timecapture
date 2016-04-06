from django import forms
from django.contrib.admin import widgets
from timecapture.models import TimeUser
from timesheet.models import Client,JobType
class MetricInputForm(forms.Form):
    startdate =  forms.DateField(widget=forms.HiddenInput())
    enddate =  forms.DateField(widget=forms.HiddenInput())
    daterange = forms.CharField(label='Date Range')
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    jobtype = forms.ModelMultipleChoiceField(label='Job Type',queryset=JobType.objects.filter(is_miscellaneous=False),
            help_text='Note: Hold ctrl key/drag down to select multiple jobtypes')
    e = forms.ModelMultipleChoiceField(label='Employee',
            queryset=TimeUser.objects.filter(is_active=True),help_text='Note: Only showing active users')


class OldsheetInputForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=TimeUser.objects.filter(is_active=True),
            help_text='Note: Only showing active users')
    date = forms.DateField(widget=widgets.AdminDateWidget())

class LeaveRegisterInputForm(forms.Form):
    startdate =  forms.DateField(widget=forms.HiddenInput())
    enddate =  forms.DateField(widget=forms.HiddenInput())
    daterange = forms.CharField(label='Date Range')

class HourlyMetricInputForm(forms.Form):
    startdate =  forms.DateField(widget=forms.HiddenInput())
    enddate =  forms.DateField(widget=forms.HiddenInput())
    daterange = forms.CharField(label='Date Range')
    e = forms.ModelMultipleChoiceField(label='Employee',
            queryset=TimeUser.objects.filter(is_active=True),help_text='Note: Only showing active users')
