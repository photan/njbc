from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader
from django.http import Http404
from django.shortcuts import render

from django import template
from django.views.generic import FormView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.core.urlresolvers import reverse_lazy

import random
import datetime;
import time;
from django.db.models import Avg,Max

from club.forms import *

from .models import *
from django.contrib import messages


class CreateSession(CreateView):
    template_name = 'club/session_create2.html'
    form_class = SessionForm
    model = Session

    # Not typical use to overwrite
    #def get_form(self,**kwargs):
    #    print("At get_form")

    def form_invalid(self,form):
        print("At form_invalid")
        return HttpResponseRedirect('/club/')

    def form_valid(self,form):
        print("At form_valid")
        #return HttpResponseRedirect('/club/')
        return super(SessionCreate,self).form_valid(form)


#------------------------------------------------------------------------------------SESSION        
class SessionCreate(CreateView):
    model = Session
    fields = ['session_name','session_type','start_time','duration_min']

class SessionCreateCustom(CreateView):
    model = Session
    # Do not specify fieds together with form class! It will throw exception
    # fields = ['session_name','session_type','start_time','duration_min']
    form_class = SessionForm
    template_name = 'club/session_create.html'


    # Not typical use to overwrite
    #def get_form(self,**kwargs):
    #    print("At get_form")

    def form_invalid(self,form):
        print("At form_invalid")
        print('error:')
        print(form)
        print(form.cleaned_data)
        return HttpResponseRedirect('/club/')

    def form_valid(self,form):
        print("At form_valid")
        # self.request_user is not valid not avail, do not try as per example
        #print("Request User: %s" % (self.request_user))
        #return HttpResponseRedirect('/club/')
        print(form.cleaned_data)
        ptime_str  = form.cleaned_data['start_time'].strftime('%D') + " " + form.cleaned_data['session_time']
        print("ptime_str: %s" % (ptime_str))
        form.instance.session_type = 'junior_training'
        form.instance.court = 0
        tdata  = "%s: %s-%03d" % (form.instance.session_type,
                                     ptime_str,
                                     random.randint(1,999))

        print("tdata: %s" % (tdata))
        session_name = tdata
        print("session_name: %s" % (session_name))
        form.instance.session_name = session_name
        form.instance.start_time = datetime.datetime.strptime(ptime_str, '%m/%d/%y %H%M')
        print("form.instance.start_time: %s" % (form.instance.start_time))

        if form.cleaned_data['player'] is not None:
           mp1 = PlayerParticipation.objects.create(person=form.cleaned_data['player'],session=form.instance,start_time=form.instance.start_time,fee_hour=15,duration_min=form.cleaned_data['duration_min'])
           mp1.save()

        if form.cleaned_data['instructor'] is not None:
           i1 = InstructorParticipation.objects.create(instructor=form.cleaned_data['instructor'],session=form.instance,start_time=form.instance.start_time,cost_hour=10,duration_min=form.cleaned_data['duration_min'])
           i1.save()
        #print("duration_min: %d" % (duration_min))
        form.save()
        return super(SessionCreateCustom,self).form_valid(form)

class SessionCreatePrivateCustom(CreateView):
    model = Session
    # Do not specify fieds together with form class! It will throw exception
    # fields = ['session_name','session_type','start_time','duration_min']
    form_class = SessionPrivateForm
    template_name = 'club/session_create_private.html'


    # Not typical use to overwrite
    #def get_form(self,**kwargs):
    #    print("At get_form")

    def form_invalid(self,form):
        print("At form_invalid")
        print('error:')
        print(form)
        print(form.cleaned_data)
        return HttpResponseRedirect('/club/')

    def form_valid(self,form):
        print("At form_valid")
        # self.request_user is not valid not avail, do not try as per example
        #print("Request User: %s" % (self.request_user))
        #return HttpResponseRedirect('/club/')
        print(form.cleaned_data)
        ptime_str  = form.cleaned_data['start_time'].strftime('%D') + " " + form.cleaned_data['session_time']
        print("ptime_str: %s" % (ptime_str))
        form.instance.session_type = form.cleaned_data['session_type']
        tdata  = "%s: %s-%03d" % (form.instance.session_type,
                                     ptime_str,
                                     random.randint(1,999))

        print("tdata: %s" % (tdata))
        
        session_name = tdata
        print("session_name: %s" % (session_name))
        form.instance.session_name = session_name
        
        form.instance.start_time = datetime.datetime.strptime(ptime_str, '%m/%d/%y %H%M')
        
        print("form.instance.start_time: %s" % (form.instance.start_time))

       
        mp1 = PlayerParticipation.objects.create(person=form.cleaned_data['player'],session=form.instance,start_time=form.instance.start_time,fee_hour=15,duration_min=form.cleaned_data['duration_min'])
        mp1.save()


        i1 = InstructorParticipation.objects.create(instructor=form.cleaned_data['instructor'],session=form.instance,start_time=form.instance.start_time,cost_hour=10,duration_min=form.cleaned_data['duration_min'])
        i1.save()
        form.save()
        #print("duration_min: %d" % (duration_min))
        return super(SessionCreatePrivateCustom,self).form_valid(form)        



class SessionDetail(UpdateView):
    model = Session    
    form_class = SessionDetailForm
    template_name = 'club/session_detail_form.html'    

    def form_invalid(self,form):
        return HttpResponseRedirect('/club/session/%d/update' % (form.instance.id))

    def form_valid(self,form):
        return HttpResponseRedirect('/club/session/%d/update' % (form.instance.id))    


class SessionList(ListView):
    model = Session
    context_object_name = "session_list"
    paginate_by = 20
    queryset = Session.objects.all()

class SessionUpdate(UpdateView):
    model = Session    
    form_class = SessionUpdateForm
    template_name = 'club/session_update_form.html'

    def form_invalid(self,form):
        print("At form_invalid")
        print('error:')
        print(form)
        print(form.cleaned_data)
        return HttpResponseRedirect('/club/')

    def form_valid(self,form):
        print("At form_valid")
        # self.request_user is not valid not avail, do not try as per example
        #print("Request User: %s" % (self.request_user))
        #return HttpResponseRedirect('/club/')
        print(form.cleaned_data)
        #mp1 = PlayerParticipation.objects.create(person=form.cleaned_data['player'],session=form.instance,start_time=form.instance.start_time,fee_hour=15,duration_min=form.instance.duration_min)
        #mp1.save()

        #print("duration_min: %d" % (duration_min))
        if 'remove_players' in self.request.POST:
            print('Request to remove players:',form.cleaned_data['players'])
            for p in form.cleaned_data['players']:
               print('Delete:', p.sname, p.id, form.instance.id)
               messages.add_message(self.request,messages.SUCCESS, "Player Removed: %s" % (p.sname))
               PlayerParticipation.objects.filter(person=p,session=form.instance).delete()
               form.save()
        elif 'remove_instructors' in self.request.POST:
            print('Request to remove instructors:',form.cleaned_data['instructors'])
            for p in form.cleaned_data['instructors']:
               print('Delete:', p.sname, p.id, form.instance.id)
               messages.add_message(self.request,messages.SUCCESS, "Instructor Removed: %s" % (p.sname))
               InstructorParticipation.objects.filter(instructor=p,session=form.instance).delete()
               form.save()
        elif 'delete_session' in self.request.POST:
            if form.instance.players.count() == 0 and form.instance.instructors.count() == 0:
               print('Delete session')
               messages.add_message(self.request,messages.SUCCESS, "Session Removed: %s" % (form.instance.session_name))
               form.instance.delete()
               return HttpResponseRedirect('/club/session/list')
            else:
               messages.add_message(self.request,messages.INFO, "Unable to remove session that has still has players or instructor: %s" % (form.instance.session_name))
        else:
            ptime_str  = form.cleaned_data['start_time'].strftime('%D') + " " + form.cleaned_data['session_time']
            form.instance.court = 0
            form.instance.start_time = datetime.datetime.strptime(ptime_str, '%m/%d/%y %H%M')
            form.save()
            messages.add_message(self.request,messages.SUCCESS, "Session Update Saved Successfully: %s" % (form.instance.session_name))
                          
        
        return super(SessionUpdate,self).form_valid(form)
                     


class SessionAssignPlayer2(UpdateView):
    model = Session
    # Do not specify fieds together with form class! It will throw exception
    # fields = ['session_name','session_type','start_time','duration_min']
    form_class = SessionAssignPlayerForm
    template_name = 'club/session_assign_player.html'

    def form_invalid(self,form):
        print("At form_invalid")
        print('error:')
        print(form)
        print(form.cleaned_data)
        return  super(SessionAssignPlayer,self).form_invalid(form)

    def form_valid(self,form):
        print("At form_valid")
        # self.request_user is not valid not avail, do not try as per example
        #print("Request User: %s" % (self.request_user))
        #return HttpResponseRedirect('/club/')
        print(form.cleaned_data)
        
        if len(PlayerParticipation.objects.filter(person=form.cleaned_data['player'],session=form.instance)) < 1:
            mp1 = PlayerParticipation.objects.create(person=form.cleaned_data['player'],session=form.instance,start_time=form.instance.start_time,fee_hour=15,duration_min=form.instance.duration_min)
            mp1.save()
            messages.add_message(self.request,messages.SUCCESS,"New Player Assigned: %s" % (form.cleaned_data['player'].sname))
        else:
            messages.add_message(self.request,messages.INFO,"Player is already assigned for the session: %s" % (form.cleaned_data['player'].sname))
        
        return super(SessionAssignPlayers,self).form_valid(form)


class SessionAssignPlayer(UpdateView):
    model = Session
    # Do not specify fieds together with form class! It will throw exception
    # fields = ['session_name','session_type','start_time','duration_min']
    form_class = SessionAssignPlayersForm
    template_name = 'club/session_assign_player.html'

    def form_invalid(self,form):
        print("At form_invalid")
        print('error:')
        print(form)
        print(form.cleaned_data)
        return  super(SessionAssignPlayer,self).form_invalid(form)

    def form_valid(self,form):
        print("At form_valid")
        # self.request_user is not valid not avail, do not try as per example
        #print("Request User: %s" % (self.request_user))
        #return HttpResponseRedirect('/club/')
        print(form.cleaned_data)
        
        for player in form.cleaned_data['players_list']:               
            if len(PlayerParticipation.objects.filter(person=player,session=form.instance)) < 1:
                print("Add Player:", player)
                mp1 = PlayerParticipation.objects.create(person=player,session=form.instance,start_time=form.instance.start_time,fee_hour=15,duration_min=form.instance.duration_min)
                mp1.save()
                messages.add_message(self.request,messages.SUCCESS,"New Player Assigned: %s" % (player.sname))
                form.save()
            else:
                messages.add_message(self.request,messages.INFO,"Player is already assigned for the session: %s" % (player.sname))
        
        return super(SessionAssignPlayer,self).form_valid(form)



class SessionAssignInstructor(UpdateView):
    model = Session
    # Do not specify fieds together with form class! It will throw exception
    # fields = ['session_name','session_type','start_time','duration_min']
    form_class = SessionAssignInstructorForm
    template_name = 'club/session_assign_instructor.html'

    def form_invalid(self,form):
        print("At form_invalid")
        print('error:')
        print(form)
        print(form.cleaned_data)
        return HttpResponseRedirect('/club/')

    def form_valid(self,form):
        print("At form_valid")
        # self.request_user is not valid not avail, do not try as per example
        #print("Request User: %s" % (self.request_user))
        #return HttpResponseRedirect('/club/')
        print(form.cleaned_data)
     
        i1 = InstructorParticipation.objects.create(instructor=form.cleaned_data['instructor'],session=form.instance,start_time=form.instance.start_time,cost_hour=10,duration_min=form.instance.duration_min)
        i1.save()
        #print("duration_min: %d" % (duration_min))
        return super(SessionAssignInstructor,self).form_valid(form)



class SessionDelete(DeleteView):
    model = Session    
    success_url = reverse_lazy('session_list')


#----------------------------------------------------------------------------------Player/Instructor 
class PlayerCreate(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'club/player_form.html'
   #field = []


class PlayerCreateCustom(CreateView):
    model = Person
    # Do not specify fieds together with form class! It will throw exception
    # fields = ['sname']
    form_class = PersonForm
    template_name = 'club/player_create.html'


    # Not typical use to overwrite
    #def get_form(self,**kwargs):
    #    print("At get_form")

    def form_invalid(self,form):
        print("At form_invalid")
        print(form)
        print(form.cleaned_data)
        return HttpResponseRedirect('/club/')

    def form_valid(self,form):
        print("At form_valid")

        # self.request_user is not valid not avail, do not try as per example
        #print("Request User: %s" % (self.request_user))
        #return HttpResponseRedirect('/club/')
        print(form.cleaned_data)

        result = Person.objects.all().aggregate(Max('njbc_id'))
        njbc_id_raw = result.get('njbc_id__max','1000')
        print("new njbc_id_raw:", njbc_id_raw)
        njbc_id= int(njbc_id_raw) + 1
        form.instance.njbc_id = njbc_id;
        form.instance.sname = "%s.%s-%s" % (form.instance.first_name,form.instance.last_name,form.instance.njbc_id)
        # ptime_str  = form.cleaned_data['start_time'].strftime('%D') + " " + form.cleaned_data['session_time']
        # print("ptime_str: %s" % (ptime_str))
        # form.instance.session_type = 'junior_training'
        # form.instance.court = 0
        # tdata  = "%s: %s-%03d" % (form.instance.session_type,
        #                              ptime_str,
        #                              random.randint(1,999))

        # print("tdata: %s" % (tdata))
        # session_name = tdata
        # print("session_name: %s" % (session_name))
        # form.instance.session_name = session_name
        # form.instance.start_time = datetime.datetime.strptime(ptime_str, '%m/%d/%y %H%M')
        # print("form.instance.start_time: %s" % (form.instance.start_time))

        # form.save()
        # mp1 = PlayerParticipation.objects.create(person=form.cleaned_data['player'],session=form.instance,start_time=form.instance.start_time,fee_hour=15,duration_min=form.cleaned_data['duration_min'])
        # mp1.save()


        # i1 = InstructorParticipation.objects.create(instructor=form.cleaned_data['instructor'],session=form.instance,start_time=form.instance.start_time,cost_hour=10,duration_min=form.cleaned_data['duration_min'])
        # i1.save()
        # #print("duration_min: %d" % (duration_min))
        
        
        #form.instance.person_type = form.cleaned_data['person_type']
        return super(PlayerCreateCustom,self).form_valid(form)


class PlayerDetail(UpdateView):
    model = Person
    form_class = PersonDetailForm
    template_name = 'club/player_detail.html'    

    def form_invalid(self,form):
        return HttpResponseRedirect('/club/player/%d/update' % (form.instance.id))

    def form_valid(self,form):
        return HttpResponseRedirect('/club/player/%d/update' % (form.instance.id))    


class PlayerList(ListView):
    model = Person
    template_name = 'club/player_list.html'
    context_object_name = "persons"
    paginate_by = 20
    queryset = Person.objects.all()

class PlayerSiblings(DetailView):
    model = Person
    template_name = 'club/player_siblings.html'

    def get_context_data(self, **kwargs):
        context = super(PlayerSiblings,self).get_context_data(**kwargs)
        person = self.get_object()
        print("person:", person)
        print("sibling_eldest:",person.sibling_eldest)
        #siblings = Person.objects.filter(sibling_eldest=person.sibling_eldest).exclude(pk=person.pk)
        siblings = Person.objects.filter(sibling_eldest=person.sibling_eldest)
        print("siblings:",siblings)
        context['siblings'] = siblings
        
        return context

class PlayerPlayedSessions(DetailView):
    model = Person
    template_name = 'club/player_played_sessions.html'

    class PartDetails:
       def __init__(self, x):
         self.x  = x

    def is_least_cost_among_sibling(self, month_0, today, my_total, person):
        siblings = Person.objects.filter(sibling_eldest=person.sibling_eldest).exclude(pk=person.pk)
        person_cheapest = None
        smallest_total = None
        for splayer in siblings:
            print("Checking sibling:", splayer.sname)
            valid_member = False
            junior_participations_cost = 0
            private_participations_cost = 0
            junior_count=0
            junior_time=0
            private_count=0
            private_time=0
            if splayer.njbc_expiry_date is not None:
               valid_member = splayer.njbc_expiry_date > datetime.datetime.today().date()
            junior_participations = splayer.playerparticipation_set.filter(start_time__range=[month_0,today],session__session_type='junior_training').order_by('-start_time')
            
            for p in junior_participations:
                junior_time = junior_time + p.duration_min/60
                junior_count = junior_count + 1

            junior_rate = session_prices(junior_count,valid_member)
            junior_participations_cost =  junior_rate * junior_time


            private_participations = splayer.playerparticipation_set.filter(start_time__range=[month_0,today],session__session_type='private').order_by('-start_time')
            for p in private_participations:
                players_count  = p.session.players.count()
                private_rate   = session_private_prices(players_count,p.duration_min,valid_member)
                private_total  = (p.duration_min/60.0) * private_rate
                private_participations_cost = private_participations_cost + private_total
                private_count = junior_count + 1


            grand_total = junior_participations_cost + private_participations_cost
            print("Cost of %s: %f" % (splayer.sname, grand_total))

            if smallest_total is None:
                person_cheapest = splayer
                smallest_total = grand_total
            elif grand_total < smallest_total:
                person_cheapest = splayer
                smallest_total = grand_total

        if my_total == smallest_total:
            if person.pk < person_cheapest.pk:
                return True
            else:
                return False
        elif my_total < smallest_total:
            return True
        else:
            return False
        

    def get_context_data(self, **kwargs):
        context = super(PlayerPlayedSessions,self).get_context_data(**kwargs)
        person = self.get_object()

        # Today
        # This week
        # This month
        # Last month
        # Last played session month
        # Known sibling
        
        # Start of week
        # day = '12/Oct/2013'
        # dt = datetime.strptime(day, '%d/%b/%Y')
        # start = dt - timedelta(days=dt.weekday())

        # Start of month
        # Start of old month and less that First of new month - 1

        # Start of last 3 month
        # Start of old month and less that First of new month - 1
        play_record = {}
        today         = datetime.datetime.today().date()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        month_0       = today.replace(day=1)
        month_1       = month_0.replace(month=month_0.month-1)
        month_2       = month_0.replace(month=month_0.month-3)

        valid_member = False
        if person.njbc_expiry_date is not None:
           valid_member = person.njbc_expiry_date > datetime.datetime.today().date()

        participations_month = person.playerparticipation_set.filter(start_time__range=[month_0,today],session__session_type='junior_training').order_by('-start_time')
        total_time = 0
        for p in participations_month:
            total_time = total_time + p.duration_min

        total_time_private = 0
        participations_private_month_total = 0
        participations_private_month_total_count = 0
        participations_private_month = person.playerparticipation_set.filter(start_time__range=[month_0,today],session__session_type='private').order_by('-start_time')
        for p in participations_private_month:
            p_session = p.session
            p.participations_private_month_persons_count = p_session.players.count()
            participations_private_month_rate   = session_private_prices(p.participations_private_month_persons_count,p.duration_min,valid_member)
            p.participations_private_month_rate = participations_private_month_rate
            
            p.session_id = p.session.pk
            p.participations_private_month_total = (p.duration_min/60.0) * participations_private_month_rate
            participations_private_month_total = participations_private_month_total +  p.participations_private_month_total
            participations_private_month_total_count = participations_private_month_total_count + 1
            total_time_private = total_time_private + p.duration_min
        
        


        participations_month_count  = len(participations_month)
        participations_month_member = valid_member
        participations_month_rate   = session_prices(participations_month_count,valid_member)
        participations_month_total  = (total_time/60.0) * participations_month_rate   

       
        
        grand_total = participations_month_total + participations_private_month_total
        
        #participations_month_1_count  = len(participations_month_1)
        #participations_month_1_member = valid_member
        #participations_month_1_rate   = session_prices(participations_month_1_count,valid_member)
        #participations_month_1_total  = participations_month_1_count * participations_month_1_rate
        
        
        if len(person.sibling_eldest) > 0:
           if self.is_least_cost_among_sibling(month_0,today,grand_total,person) is True:
              print("Sibling discount: TRUE")
              context['sibling_discount'] = True
              context['sibling_price'] = grand_total *0.95



        
        #for pl in participations_list:
        #    pl.primary_instructor = "LCW"
        #    sessions_list.append(pl)

        # Context
        # this_week_session_total
        # sibiling_list
        # sibling_discount_enabled
        # sibling_bills
        # paid

        context['today']   = today
        # context['month_0'] = month_0
        # context['month_1'] = month_1    
        # context['month_2'] = month_2

        # context['participations_month_0'] = participations_month_0
        # context['participations_month_0_count'] = participations_month_0_count
        # context['participations_month_0_rate'] = participations_month_0_rate
        # context['participations_month_0_member'] = participations_month_0_member
        # context['participations_month_0_total'] = participations_month_0_total        

        # context['participations_month_1'] = participations_month_1
        # context['participations_month_1_count'] = participations_month_1_count
        # context['participations_month_1_rate'] = participations_month_1_rate
        # context['participations_month_1_member'] = participations_month_1_member
        # context['participations_month_1_total'] = participations_month_1_total

        # context['participations_month_2'] = participations_month_2
        # context['participations_private_month_2'] = participations_private_month_2
        # context['participations_month_2_count'] = participations_month_2_count
        # context['participations_month_2_rate'] = participations_month_2_rate
        # context['participations_month_2_member'] = participations_month_2_member
        # context['participations_month_2_total'] = participations_month_2_total
        
       
        play_record['month'] = month_0
        play_record['participations_month'] = participations_month
        play_record['participations_month_count' ] = participations_month_count
        play_record['participations_month_rate'] = participations_month_rate
        play_record['participations_month_member'] =participations_month_member
        play_record['participations_month_total'] = participations_month_total
        play_record['participations_month_total_time'] = total_time/60.0



        play_record['participations_private_month'] = participations_private_month
        play_record['participations_private_month_total'] = participations_private_month_total
        play_record['participations_private_month_total_count'] = participations_private_month_total_count
        play_record['participations_private_month_total_time'] = total_time/60.0
        play_record['total_time_private'] = total_time_private
        context['grand_total'] = grand_total
        context['play_record'] = play_record
        context['person']   = person


        return context


class PlayerUpdate(UpdateView):
    model = Person    
    form_class = PersonEditForm
    template_name = 'club/player_update.html'
        

class PlayerDelete(DeleteView):
    model = Person    
    template_name = 'club/player_confirm_delete.html'
    success_url = reverse_lazy('player_list')




#----------------------------------------------------------------------------------Instructor 
class InstructorCreate(CreateView):
    model = Instructor
    # Do not specify fieds together with form class! It will throw exception
    # fields = ['sname']
    form_class = InstructorForm
    template_name = 'club/instructor_create.html'


    # Not typical use to overwrite
    #def get_form(self,**kwargs):
    #    print("At get_form")

    def form_invalid(self,form):
        print("At form_invalid")
        print(form)
        print(form.cleaned_data)
        return HttpResponseRedirect('/club/')

    def form_valid(self,form):
        print("At form_valid")
        print(form.cleaned_data)
        form.instance.sname = "%s.%s" % (form.instance.first_name,form.instance.last_name)
        return super(InstructorCreate,self).form_valid(form)


class InstructorDetail(UpdateView):
    model = Instructor
    form_class = InstructorDetailForm
    template_name = 'club/instructor_detail.html'    

    def form_invalid(self,form):
        return HttpResponseRedirect('/club/instructor/%d/update' % (form.instance.id))

    def form_valid(self,form):
        return HttpResponseRedirect('/club/instructor/%d/update' % (form.instance.id))    


class InstructorList(ListView):
    model = Instructor
    template_name = 'club/instructor_list.html'
    context_object_name = "instructors"
    paginate_by = 20
    queryset = Instructor.objects.all()


class InstructorTeachedSessions(DetailView):
    model = Instructor
    template_name = 'club/instructor_teached_sessions.html'

    class PartDetails:
       def __init__(self, x):
         self.x  = x

    def get_context_data(self, **kwargs):
        context = super(InstructorPlayedSessions,self).get_context_data(**kwargs)
        instructor = self.get_object()

        today         = datetime.datetime.today().date()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        month_0       = today.replace(day=1)
        month_1       = month_0.replace(month=month_0.month-1)
        month_2       = month_0.replace(month=month_0.month-3)

        p1 = InstructorPlayedSessions.PartDetails(1)
        p2 = InstructorPlayedSessions.PartDetails(2)
        p3 = InstructorPlayedSessions.PartDetails(3)
        plist = []
        plist.append(p1)
        plist.append(p2)
        plist.append(p3)

        participations_month_0 = instructor.instructorparticipation_set.filter(start_time__range=[month_0,today],session__session_type='junior_training').order_by('-start_time')
        participations_month_1 = instructor.instructorparticipation_set.filter(start_time__range=[month_1,month_0],session__session_type='junior_training').order_by('-start_time')
        participations_month_2 = instructor.instructorparticipation_set.filter(start_time__range=[month_2,month_1],session__session_type='junior_training').order_by('-start_time')
        participations_private_month_2 = instructor.instructorparticipation_set.filter(start_time__range=[month_2,month_1],session__session_type='private').order_by('-start_time')
        
        
        valid_member = False
        if instructor.njbc_expiry_date is not None:
           valid_member = instructor.njbc_expiry_date > datetime.datetime.today().date()


        participations_month_0_count  = len(participations_month_0)
        participations_month_0_member = valid_member
        participations_month_0_rate   = session_prices(participations_month_0_count,valid_member)
        participations_month_0_total  = participations_month_0_count * participations_month_0_rate   
        
        participations_month_1_count  = len(participations_month_1)
        participations_month_1_member = valid_member
        participations_month_1_rate   = session_prices(participations_month_1_count,valid_member)
        participations_month_1_total  = participations_month_1_count * participations_month_1_rate
        
        
        participations_month_2_count  = len(participations_month_2)
        participations_month_2_member = valid_member
        participations_month_2_rate   = session_prices(participations_month_2_count,valid_member)
        participations_month_2_total  = participations_month_2_count * participations_month_2_rate

        context['plist']   = plist
        context['today']   = today
        context['month_0'] = month_0
        context['month_1'] = month_1    
        context['month_2'] = month_2

        context['participations_month_0'] = participations_month_0
        context['participations_month_0_count'] = participations_month_0_count
        context['participations_month_0_rate'] = participations_month_0_rate
        context['participations_month_0_member'] = participations_month_0_member
        context['participations_month_0_total'] = participations_month_0_total        

        context['participations_month_1'] = participations_month_1
        context['participations_month_1_count'] = participations_month_1_count
        context['participations_month_1_rate'] = participations_month_1_rate
        context['participations_month_1_member'] = participations_month_1_member
        context['participations_month_1_total'] = participations_month_1_total

        context['participations_month_2'] = participations_month_2
        context['participations_private_month_2'] = participations_private_month_2
        context['participations_month_2_count'] = participations_month_2_count
        context['participations_month_2_rate'] = participations_month_2_rate
        context['participations_month_2_member'] = participations_month_2_member
        context['participations_month_2_total'] = participations_month_2_total
        
        return context


class InstructorUpdate(UpdateView):
    model = Instructor    
    form_class = InstructorEditForm
    template_name = 'club/instructor_update.html'
        

class InstructorDelete(DeleteView):
    model = Instructor    
    template_name = 'club/instructor_confirm_delete.html'
    success_url = reverse_lazy('instructor_list')



#----------------------------------------------------------------------------------OLD STUFF

def index(request):
    context = {
    }
    return render(request, 'club/base.html', context)


def sessions(request):
    latest_session_list = Session.objects.all()
    template = loader.get_template('club/sessions.html')
    context = {
        'latest_session_list': latest_session_list,
    }
    return HttpResponse(template.render(context, request))

def session_create(request):
    context = {
    }
    return render(request, 'club/session_create.html', context)


# ...
def detail(request, session_id):
    try:
        session = Session.objects.get(pk=session_id)
        players_list = session.players.all()
        instructors_list = session.instructors.all()
        
    except SessionPart.DoesNotExist:
        raise Http404("Session does not exist")
    return render(request, 'club/detail.html', {'session': session,
                                                'players_list':players_list,
                                                'instructors_list':instructors_list})


    
def players(request):
    try:
        players_list = Instructor.objects.all()
    except Instructor.DoesNotExist:
        raise Http404("Player does not exist")
    return render(request, 'club/players.html', {'players_list': players_list})


def instructors(request):
    try:
        instructors_list = Instructor.objects.all()
    except Instructor.DoesNotExist:
        raise Http404("instructor does not exist")
    return render(request, 'club/instructors.html', {'instructors_list': instructors_list})


def person_lessons(request, person_id):
    try:
        person = Instructor.objects.get(pk=person_id)
        person_lessons = person.playerparticipation_set.all().order_by('start_time')
        total=0
        for pl in person_lessons:
            pl.total = (pl.fee_hour * pl.duration_min)/60
            pl.duration = pl.duration_min/60
            total = pl.total + total
    except ValidationError:
        raise Http404("Instructor does not exist")
    return render(request, 'club/person_lessons.html', {'person': person,
                                                        'person_lessons':person_lessons,
                                                        'total':total})

def person_edit(request, person_id):
    try:
        person = Instructor.objects.get(pk=person_id)
        person_lessons = person.playerparticipation_set.all().order_by('start_time')
        total=0
        for pl in person_lessons:
            pl.total = (pl.fee_hour * pl.duration_min)/60
            pl.duration = pl.duration_min/60
            total = pl.total + total
    except ValidationError:
        raise Http404("Instructor does not exist")
    return render(request, 'club/person_lessons.html', {'person': person,
                                                        'person_lessons':person_lessons,
                                                        'total':total})
                                                        
def instructor_lessons(request, instructor_id):
    try:
        instructor = Instructor.objects.get(pk=instructor_id)
        instructor_lessons = instructor.instructorparticipation_set.all().order_by('start_time')
        total=0
        for ll in instructor_lessons:
            ll.total = (ll.cost_hour * ll.duration_min)/60
            ll.duration = ll.duration_min/60
            total = ll.total + total
    except ValidationError:
        raise Http404("Instructor does not exist")
    return render(request, 'club/instructor_lessons.html', {'instructor': instructor,
                                                        'instructor_lessons':instructor_lessons,
                                                        'total':total})
