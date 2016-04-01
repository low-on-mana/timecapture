import json,datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import TsheetEntry
from . import rendertsheet
# Create your views here

# Relaxation provided to employee in minutes
RELAXATION = 30

def detect_fraud(old_entries,current_entry):
    ''' Returns False if no fraud otherwise an error message '''
    if current_entry['start'] < rendertsheet.DAY_START:
        return 'Cannot put entry before %d ! ' % rendertsheet.DAY_START
    elif current_entry['start'] + current_entry['colspan'] > rendertsheet.DAY_END:
        return 'Cannot put entry past %d !' % rendertsheet.DAY_END

    for old_entry in old_entries:
        if (current_entry['start'] >= old_entry.starthr and current_entry['start'] < old_entry.starthr + old_entry.hours) or \
                (old_entry.starthr >= current_entry['start'] and old_entry.starthr < current_entry['start'] + current_entry['colspan']):
            return 'The timeslot you are trying to fill is already booked'
    return False


def is_valid_entry(old_entries,current_entry,TODAY_DATE):
    ''' Returns True if valid entry otherwise an error message '''
    fraud_res = detect_fraud(old_entries,current_entry)
    if fraud_res != False:
        return fraud_res
    entry_end_datetime = datetime.datetime.combine(TODAY_DATE.date(),datetime.time()) + datetime.timedelta(hours=current_entry['start']+current_entry['colspan'])
    # print('Entry time %s \n comparison time %s' % (entry_end_datetime , TODAY_DATE - datetime.timedelta(minutes=RELAXATION)))
    if entry_end_datetime  - datetime.timedelta(minutes=RELAXATION) > TODAY_DATE:
        return 'You cannot fill entries in future !'
    return True


def is_valid_leave_request(leave_date,USER_PK):
    ''' Returns False if valid leave request otherwise leaves an error message '''
    if leave_date.weekday() > 4:
        return 'Cannot mark leave on a weekend'
    query_res = TsheetEntry.objects.filter(date__range=(leave_date.strftime('%Y-%m-%d 00:00:00'),leave_date.strftime('%Y-%m-%d 23:59:59'))).filter(employee=USER_PK) 
    if query_res:
        return 'There are already some entries marked on that day'
    return False


@login_required
def index(request):
    TODAY_DATE = datetime.datetime.today()+datetime.timedelta(hours=5,minutes=30)
    USER_PK = request.user.id
    if request.method == 'POST':
        if 'tsheet_data' in request.POST:
            tsheet_entries = json.loads(request.POST['tsheet_data'])
            print(tsheet_entries)
            entries_succesfuly_submitted = 0
            
            # Validation logic
            if len(tsheet_entries) > 0:
                entries_submitted_today = TsheetEntry.objects.filter(date__range=(TODAY_DATE.strftime('%Y-%m-%d 00:00:00'),TODAY_DATE.strftime('%Y-%m-%d 23:59:59'))).filter(employee=USER_PK).order_by('starthr')
                # print(entries_submitted_today)

            for tsheet_data in tsheet_entries:
                if tsheet_data['category'] == 'TODAY':
                    entry_validation_res = is_valid_entry(entries_submitted_today,tsheet_data,TODAY_DATE)
                    if entry_validation_res != True:
                        messages.error(request,entry_validation_res)
                        return redirect('timesheet:index')
                    tsheet_obj = TsheetEntry(date=TODAY_DATE.strftime('%Y-%m-%d %H:%M:%S'),
                                             starthr=tsheet_data['start'],
                                             hours=tsheet_data['colspan'],
                                             client=tsheet_data['client'],
                                             jobtype=tsheet_data['jobtype'],
                                             employee=USER_PK,
                                             description=tsheet_data['description'])
                elif tsheet_data['category'] == 'LEAVE':
                    date_from_client = datetime.datetime.strptime(tsheet_data['date'],'%m/%d/%Y')
                    leave_req_res = is_valid_leave_request(date_from_client,USER_PK)
                    if leave_req_res != False:
                        messages.error(request,leave_req_res)
                        return redirect('timesheet:index')
                    tsheet_obj = TsheetEntry(date=date_from_client.strftime('%Y-%m-%d %H:%M:%S'),
                                             starthr=tsheet_data['start'],
                                             hours=tsheet_data['colspan'],
                                             client=tsheet_data['client'],
                                             jobtype=tsheet_data['jobtype'],
                                             employee=USER_PK)
                tsheet_obj.save()
                entries_succesfuly_submitted += 1
        if entries_succesfuly_submitted ==  1:
            messages.success(request,'%d entry successfully submitted!' % entries_succesfuly_submitted)
        elif entries_succesfuly_submitted >  1:
            messages.success(request,'%d entries successfully submitted!' % entries_succesfuly_submitted)
        else:
            messages.error(request,'No entries submitted.')
        return redirect('timesheet:index')
    return rendertsheet.render_timesheet(request,USER_PK,TODAY_DATE,'timesheet/index.html')
