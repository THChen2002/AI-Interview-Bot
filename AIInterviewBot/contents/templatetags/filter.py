from django import template

register = template.Library()

@register.filter
def get_month_name(datetime):
    if datetime.month == 1:
        return 'Jan'
    elif datetime.month == 2:
        return 'Feb'
    elif datetime.month == 3:
        return 'Mar'
    elif datetime.month == 4:
        return 'Apr'
    elif datetime.month == 5:
        return 'May'
    elif datetime.month == 6:
        return 'Jun'
    elif datetime.month == 7:
        return 'Jul'
    elif datetime.month == 8:
        return 'Aug'
    elif datetime.month == 9:
        return 'Sep'
    elif datetime.month == 10:
        return 'Oct'
    elif datetime.month == 11:
        return 'Nov'
    elif datetime.month == 12:
        return 'Dec'
    else:
        return ''
    