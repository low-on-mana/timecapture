import datetime,calendar
from django.shortcuts import render
from timecapture.models import TimeUser
from timecapture.commons import get_number_of_weekdays
from .models import JobType, Client, TsheetEntry

DAY_START = 9
DAY_END = 23
EXPECTED_WORK_HRS = 40
EXTRA_WORK_CAPACITY = 80
WORKING_DAYS = 5
HOURS_PER_LEAVE = int(EXPECTED_WORK_HRS/WORKING_DAYS)


def render_monthly_timesheet(request,userpk,date,htmlfile):
    ''' Renders monthly timesheet '''
    month_day = date.day - 1
    td = datetime.timedelta(days=1)
    month_dates = [date - td*month_day]
    mday = month_dates[-1] + td
    #Loop until get next of this month
    while mday.day != 1:
        month_dates.append(mday)
        mday = month_dates[-1] + td
    total_workable_hrs = get_number_of_weekdays(month_dates[0],month_dates[-1])*HOURS_PER_LEAVE
    tsheet_old_sql_entries = TsheetEntry.objects.filter(date__range=(month_dates[0].strftime('%Y-%m-%d'),(month_dates[-1]).strftime('%Y-%m-%d 23:59:59'))).filter(employee=userpk).order_by('starthr')

    tsheet_old_map = []
    tsheet_helper = []
    for month_date in month_dates:
        tsheet_old_map.append({'date':month_date,'data':[]})
        tsheet_helper.append(DAY_START)

    hours_worked_this_month = 0

    for tsheet_old_entry in tsheet_old_sql_entries:
        hours_worked_this_month += tsheet_old_entry.hours
        tsheet_mday = tsheet_old_entry.date.day - 1
        if tsheet_old_entry.starthr == tsheet_helper[tsheet_mday]:
            tsheet_old_map[tsheet_mday]['data'].append(tsheet_old_entry)
            tsheet_helper[tsheet_mday] += tsheet_old_entry.hours
        else:
            tsheet_old_map[tsheet_mday]['data'].extend((tsheet_old_entry.starthr - tsheet_helper[tsheet_mday]) * [None])
            tsheet_helper[tsheet_mday] = tsheet_old_entry.starthr
            tsheet_old_map[tsheet_mday]['data'].append(tsheet_old_entry)
            tsheet_helper[tsheet_mday] += tsheet_old_entry.hours

    for tsheet_data in tsheet_old_map:
        if tsheet_data['data']:
            tsheet_last_obj = tsheet_data['data'][-1]
            tsheet_data['data'].extend((DAY_END - tsheet_last_obj.starthr - tsheet_last_obj.hours)*[None] )
    client_dict = {}
    jobtypes = JobType.objects.all()
    for client in Client.objects.all():
        client_dict[client.name] = client.color

    return render(request,htmlfile,
            {'clients': client_dict, 'jobtypes':jobtypes, 'month_day':month_day,
                'tsheet_old_map':tsheet_old_map,'username':TimeUser.objects.get(pk=userpk),
                'markedhrs':hours_worked_this_month,'totalhrs':total_workable_hrs})

def render_timesheet(request,userpk,date,htmlfile):
    ''' Renders weekly timesheet '''
    week_day = date.weekday()
    td = datetime.timedelta(days=1) 
    week_dates = [date - td*week_day]
    for wday in range(1,7):
        week_dates.append(week_dates[-1]+td)

    tsheet_old_sql_entries = TsheetEntry.objects.filter(date__range=(week_dates[0].strftime('%Y-%m-%d'),(week_dates[-1]).strftime('%Y-%m-%d 23:59:59'))).filter(employee=userpk).order_by('starthr')
   
    tsheet_old_map = []
    tsheet_helper = []

    for i in range(0,7):
        tsheet_old_map.append({'date':week_dates[i],'data':[]})
        tsheet_helper.append(DAY_START)

    hours_worked_this_week = 0
    for tsheet_old_entry in tsheet_old_sql_entries:
        hours_worked_this_week += tsheet_old_entry.hours
        tsheet_wday = tsheet_old_entry.date.weekday()
        if tsheet_old_entry.starthr == tsheet_helper[tsheet_wday]:
            tsheet_old_map[tsheet_wday]['data'].append(tsheet_old_entry)
            tsheet_helper[tsheet_wday] += tsheet_old_entry.hours
        else:
            tsheet_old_map[tsheet_wday]['data'].extend((tsheet_old_entry.starthr - tsheet_helper[tsheet_wday]) * [None])
            tsheet_helper[tsheet_wday] = tsheet_old_entry.starthr
            tsheet_old_map[tsheet_wday]['data'].append(tsheet_old_entry)
            tsheet_helper[tsheet_wday] += tsheet_old_entry.hours


    for tsheet_data in tsheet_old_map:
        if tsheet_data['data']:
            tsheet_last_obj = tsheet_data['data'][-1]
            tsheet_data['data'].extend((DAY_END - tsheet_last_obj.starthr - tsheet_last_obj.hours)*[None] )
    
    client_dict = {}
    miscellaneous_client = ()
    jobtypes = JobType.objects.all()

    for client in Client.objects.all():
        if client.id == 1:
            miscellaneous_client = (client.name,client.color,HOURS_PER_LEAVE,jobtypes[0].name)
        client_dict[client.name] = client.color

    if hours_worked_this_week > EXPECTED_WORK_HRS:
        green_progress_fill = 100
        red_progress_fill = int(((hours_worked_this_week-EXPECTED_WORK_HRS)*100)/EXTRA_WORK_CAPACITY)
    else:
        green_progress_fill = int((hours_worked_this_week*100)/EXPECTED_WORK_HRS)
        red_progress_fill = 0

    if hours_worked_this_week < EXPECTED_WORK_HRS:
        hrs_left_reach_target = int((hours_worked_this_week * 100) / EXPECTED_WORK_HRS)
    else:
        hrs_left_reach_target = 0
    return render(request,htmlfile,
            {'clients': client_dict, 'jobtypes':jobtypes, 'week_day':week_day,
             'tsheet_old_map':tsheet_old_map, 'app_name':request.resolver_match.app_name,
             'miscellaneous_client':miscellaneous_client, 'hours_worked_this_week':hours_worked_this_week,
             'green_progress_fill':green_progress_fill, 'red_progress_fill':red_progress_fill,
             'hrs_left_reach_target':hrs_left_reach_target })
