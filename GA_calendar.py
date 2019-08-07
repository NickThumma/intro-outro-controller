#calendar from:
#https://www.kippmetroatlanta.org/wp-content/uploads/KIPP-Metro-Atlanta-Schools-Calendar-SY19-20.pdf
from datetime import date
import holidays

empty_calendar = holidays.HolidayBase()

school_calendar = holidays.US( state='GA')
days_off = {}
 
#2019
 
#end of summer break
for day in range(1,8):
    days_off[date(2019, 8, day)] = 'Summer Break'
   
#first day of school
days_off[date(2019, 8, 8)] = 'First Day'
   
#half days
for month, day in [(8,9), (8,30), (9,27), (11,8), (12,13), (12,20)]:
    days_off[date(2019, month, day)] = 'Half Day'
 
#labor day
days_off[date(2019, 9, 2)] = 'Labor Day'
 
#fall break
days_off[date(2019, 10, 11)] = 'Fall Break'
 
#indigenous people's day
days_off[date(2019, 10, 14)] = "Indigenous People's Day"
   
#teacher professional learning day
days_off[date(2019, 10, 15)] = 'Teacher Professional Learning Day'
 
#thanksgiving
for day in range(25, 30):
    days_off[date(2019, 11, day)] = 'Thanksgiving Break'
   
#winter break
for day in range(23, 32):
    days_off[date(2019, 12, day)] = 'Winter Break'
   
#TODO: 2020 (inc. winter break)
   
school_calendar.append(days_off)
 
for year in [2019, 2020]:
    for month in range(8,13):
        if month in (1, 3, 7, 8, 10, 12):
            days_in_month = 31
        elif month == 2:
            if year%4 == 0 and not (year%100 == 0 and not year%400 == 0):
                days_in_month = 29
            else:
                days_in_month = 28
        else:
            days_in_month = 30
           
        for day in range(1,days_in_month+1):
            if date(year, month, day).weekday() > 4:
                school_calendar.append({date(year, month, day):'Weekend'})