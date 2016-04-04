def get_number_of_weekdays(d1,d2):
    ''' gets the number of weekends between two dates where arg1 is less than arg2 '''
    if d1 > d2:
        return 0
    if d1 == d2:
        return  0 if d1.weekday() > 4 else 1
    total_days = (d2-d1).days + 1
    total_days_copy = total_days
    weekends = 0

    #Processing first partial week
    if d1.weekday() != 0:
        weekends = min(2,7-d1.weekday())
        total_days -= 7 - d1.weekday()

    #Processing complete weeks in between
    weeks = int(total_days/7)
    total_days = total_days%7
    weekends += 2 * weeks

    #Processing last parital week
    if total_days == 6:
        weekends += 1

    return total_days_copy - weekends
