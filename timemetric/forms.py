from django import forms
from django.contrib.admin import widgets
from timecapture.models import TimeUser
from timesheet.models import Client,JobType
class MetricInputForm(forms.Form):
    startdate =  forms.DateField(widget=forms.HiddenInput())
    enddate =  forms.DateField(widget=forms.HiddenInput())
    daterange = forms.CharField()
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    jobtype = forms.ModelMultipleChoiceField(queryset=JobType.objects.all(),help_text='Note: Hold ctrl key/drag down to select multiple jobtypes')
    employee = forms.ModelMultipleChoiceField(queryset=TimeUser.objects.filter(is_active=True),help_text='Note: Only showing active users')


class OldsheetInputForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=TimeUser.objects.filter(is_active=True),help_text='Note: Only showing active users')
    date = forms.DateField(widget=widgets.AdminDateWidget())

class LeaveRegisterInputForm(forms.Form):
    date = forms.DateField(widget=widgets.AdminDateWidget(),help_text='Note: Widget will only consider month and year')
