from django.utils.translation import ugettext_lazy as _
from django.db import models

class Client(models.Model):
    name = models.CharField(_('name'), max_length=30)
    color = models.CharField(_('color'), max_length=30,default='Blue')

    def __str__(self):
        return self.name

class JobType(models.Model):
    name = models.CharField(_('name'), max_length=30)

    def __str__(self):
        return self.name

class TsheetEntry(models.Model):
    date= models.DateTimeField(_('date'),db_index=True)
    starthr = models.PositiveSmallIntegerField(_('starthr'))
    hours = models.PositiveSmallIntegerField(_('hours'))
    client = models.CharField(_('client'), max_length=30)
    jobtype = models.CharField(_('jobtype'),max_length=30)
    employee = models.IntegerField(_('employee'))
    description = models.CharField(_('description'),max_length=150,blank=True)

    def __str__(self):
        return '%s %s %s %s %s' % (self.date,self.starthr,self.hours,self.client,self.jobtype)
