def add_time(start, duration, day=''):

    day = day.lower()
    match(day):
            case 'sunday': day_int = 1
            case 'monday': day_int = 2
            case 'tuesday': day_int = 3
            case 'wednesday': day_int = 4
            case 'thursday': day_int = 5
            case 'friday': day_int = 6
            case 'saturday': day_int = 7
            case _: day_int = -1

    
    #split start by space to get time and foramt
    start = start.split(' ')
    time_str = start[0].strip()
    format_str = start[1].strip()
    
    #split start by : to get hour and min
    start_time = time_str.split(':')
    start_hour_str = start_time[0].strip()
    start_min_str = start_time[1].strip()

    #split duration by : to get hour and min 
    duration = duration.split(':')
    duration_hour_str = duration[0].strip()
    duration_min_str = duration[1].strip()

    #int convertion
    start_hour = int(start_hour_str)
    if(format_str == 'PM'): start_hour += 12
    start_min = int(start_min_str)
    duration_hour = int(duration_hour_str)
    duration_min = int(duration_min_str)

    #calculate end time
    end_min = start_min + duration_min
    hour_add_from_min = int(end_min / 60)
    end_min %= 60
    end_hour = start_hour + duration_hour + hour_add_from_min
    end_day = int(end_hour / 24)
    end_hour %= 24

    end_day_week = (day_int + end_day) % 7
    match(end_day_week):
        case 1: end_day_week_str = 'Sunday'
        case 2: end_day_week_str = 'Monday'
        case 3: end_day_week_str = 'Tuesday'
        case 4: end_day_week_str = 'Wednesday'
        case 5: end_day_week_str = 'Thursday'
        case 6: end_day_week_str = 'Friday'
        case 7: end_day_week_str = 'Saturday'
        case _: end_day_week_str = ''

    end_min_str= ''
    if(end_min < 10): end_min_str += '0'
    end_min_str += str(end_min)

    if(end_hour < 12): 
        end_hour_str = str(end_hour)
        end_format = 'AM'
    elif(end_hour >= 12):
        end_hour -= 12
        end_hour_str = str(end_hour)
        end_format = 'PM'

    if(end_hour == 0): end_hour_str = '12'
    
    new_time = ''
    new_time += end_hour_str + ":" + end_min_str + " " + end_format

    if(day_int != -1):
        new_time += f', {end_day_week_str}'

    if(end_day == 1): new_time += ' (next day)'
    elif(end_day > 1): new_time += f' ({end_day} days later)'

    return new_time

# Example usage:

print(f"{add_time('3:30 PM', '2:12')}'")
print(f"{add_time('2:59 AM', '24:00', 'saturDay')}'")