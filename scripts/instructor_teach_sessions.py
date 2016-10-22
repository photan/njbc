from club.models import *
from django.utils import timezone
from django.utils.timezone import utc
import pytz as tz
import datetime

def run():
     instructor = Instructor.objects.get(sname='thomas')
     print(instructor.first_name + ' ' + instructor.last_name)
     est = tz.timezone('America/New_York')
     for num in (range(14,26)):
        session = Session.objects.get(session_name="junior_training_jul%02d" % (num))
        stime = datetime.datetime.strptime('Jul %d 2016 4:00PM' % (num), '%b %d %Y %I:%M%p')
        print(session)
        print("stime:"),
        print(stime)
        cmd = 'InstructorParticipation.objects.create(instructor=instructor,session=session,cost_hour=8, start_time=stime.replace(tzinfo=utc),duration_min=60)'
        print(cmd)
        p = eval(cmd)
        p.save()
        
#    for num in (range(1,32)):
#       stime = datetime.datetime.strptime('Jul %d 2016 4:00PM' % (num), '%b %d %Y %I:%M%p')
#      est = tz.timezone('America/New_York')
#       cmd = 'Session(session_type="junior training",session_name="junior_training_jul%02d" ,start_time=stime,duration_min=60)' % (num)
#       print (cmd)
#       sa = Session(session_type="junior training",session_name="junior_training_jul%02d" % (num) ,start_time=stime.replace(tzinfo=utc),duration_min=60)
#       sa.save()      
