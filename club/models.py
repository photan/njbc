from django.db import models
from django.contrib import auth
from django.core.urlresolvers import reverse

def session_prices(play_count, valid_member):
        if play_count < 8: 
            rate=27
        elif play_count < 12 :
            rate=25    
        elif play_count < 15:
            rate=24    
        else:
            rate=23   
        
        if valid_member is True:
           rate=rate - 6

        return rate        

def session_private_prices(participant_count, duration, valid_member):
        if   participant_count == 1 and duration < 1: 
            rate=50
        elif participant_count == 1 and duration >= 1:
            rate=85
        elif participant_count <= 2 and duration >= 1:
            rate=50
        elif participant_count <= 3 and duration >= 1:
            rate=40
        elif participant_count <= 4 and duration >= 1:
            rate=35        
        else:
            rate=35   
        
        if valid_member is True:
           rate=rate - 5

        return rate                

# Create your models here.	
class Person(models.Model):
    sname             = models.CharField(max_length=64,unique=True)
    email             = models.CharField(max_length=128,blank=True)
    phone             = models.CharField(max_length=32,blank=True)
    first_name        = models.CharField(max_length=64)
    last_name         = models.CharField(max_length=64)
    dob               = models.DateField(blank=True, null=True)
    usba_id           = models.CharField(max_length=32,blank=True)
    njbc_id           = models.CharField(max_length=32,blank=True,unique=True)
    njbc_expiry_date  = models.DateField(blank=True, null=True)
    njbc_since        = models.DateField(blank=True, null=True)
    note              = models.CharField(max_length=128,blank=True)
    emergency_contact = models.CharField(max_length=128,blank=True)
    emergency_email   = models.CharField(max_length=128,blank=True)
    emergency_phone   = models.CharField(max_length=32,blank=True)
    sibling_eldest    = models.CharField(max_length=64,blank=True)
    #cdate             = models.DateTimeField()
    #soft_deleted      = models.BooleanField(default=False)
    def __str__(self):
        return "%s.%s-%s" % (self.first_name,self.last_name,self.njbc_id)
    def get_absolute_url(self):
        return reverse('person_detail', args=[str(self.id)])    

    class Meta:
       ordering = ['first_name']    


class private_coaching_rate(models.Model):
    person_count   = models.IntegerField(default=3, blank=False)
    duration_min   = models.IntegerField(default=3, blank=False)
    member_rate    = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    nonmember_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    coach          = models.CharField(max_length=64, blank=False)
    note           = models.CharField(max_length=128, blank=True)
    sibling_discount = 	models.DecimalField(max_digits=6, decimal_places=2, blank=True)
	
class junior_training_rate(models.Model):
    count_min = models.IntegerField(default=3,blank=False)
    member_rate    = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    nonmember_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=False)	
    sibling_discount = 	models.DecimalField(max_digits=6, decimal_places=2, blank=True)

    
class summer_camp_rate(models.Model):
    member_rate    = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    nonmember_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=False)	
    sibling_discount = 	models.DecimalField(max_digits=6, decimal_places=2, blank=True)	
	
class dropin_rate(models.Model):
    member_rate    = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    nonmember_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=False)	
    sibling_discount = 	models.DecimalField(max_digits=6, decimal_places=2, blank=True)		
	
class playpass_rate(models.Model):
    pass_count              = models.IntegerField(default=3,blank=False)
    pass_expiry_month_limit = models.IntegerField(default=3,blank=False)
    adult_rate              = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    junior_rate             = models.DecimalField(max_digits=6, decimal_places=2, blank=False)	
    
class timebase_rate(models.Model):
    time_type       = models.CharField(max_length=32, blank=False)
    individual_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    spouse_rate     = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    junior_rate     = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
		
class Instructor(models.Model):
    sname             = models.CharField(max_length=64,unique=True)
    email             = models.CharField(max_length=128)
    sname             = models.CharField(max_length=64)
    first_name        = models.CharField(max_length=64)
    last_name         = models.CharField(max_length=64)
    usba_id           = models.CharField(max_length=32,blank=True)
    emergency_contact = models.CharField(max_length=128,blank=True)
    emergency_email   = models.CharField(max_length=128,blank=True)
    emergency_phone   = models.CharField(max_length=32,blank=True)
    #soft_deleted      = models.BooleanField(default=False)
    def __str__(self):
        return self.sname	
    def get_absolute_url(self):
        return reverse('instructor_detail', args=[str(self.id)])    
    class Meta:
       ordering = ['first_name']   

class Session(models.Model):
    session_type = models.CharField(max_length=32)
    session_name = models.CharField(max_length=48,unique=True)
    persons_count = models.IntegerField(default=3,blank=True)
    
    start_time   = models.DateTimeField()
    duration_min = models.IntegerField(default=30)
    court        = models.CharField(max_length=8)

    players      = models.ManyToManyField(Person,through="PlayerParticipation",blank=True)
    instructors  = models.ManyToManyField(Instructor,through="InstructorParticipation",blank=True)
    session_note = models.CharField(max_length=128)

    def get_absolute_url(self):
        return reverse('session_detail', args=[str(self.id)])

    def __str__(self):
        return self.session_name

    class Meta:
       ordering = ['-start_time']

class PlayerParticipation(models.Model):
    person       = models.ForeignKey(Person,  on_delete=models.CASCADE)
    session      = models.ForeignKey(Session, on_delete=models.CASCADE)
    start_time   = models.DateTimeField()
    duration_min = models.IntegerField(default=30)
    fee_hour     = models.DecimalField(max_digits=6, decimal_places=2)
    use_sibling_discount = 	models.BooleanField(default=False)
    paid         = models.BooleanField(default=False)
    def __str__(self):
        return self.person.sname + " play in session %04d " % (self.session.id)

class InstructorParticipation(models.Model):
    instructor   = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    session      = models.ForeignKey(Session,    on_delete=models.CASCADE)
    start_time   = models.DateTimeField()
    duration_min = models.IntegerField(default=30)
    cost_hour    = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return self.instructor.sname + " teach in session %04d" % (self.session.id)

#class Bill(models.Model):
#    creation_date   = models.DateTimeField()
#
#    players         = models.ManyToManyField(Person,through="PlayerParticipation")
#    payment_status  = models.CharField(max_length=16)
#    payment_type    = models.CharField(max_length=16)
#    amount_paid     = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
#    recieved_by     = models.CharField(max_length=64)
#    notes           = models.CharField(max_length=128, blank=True)
#    paid            = models.BooleanField(default=False)
#    paid_date       = models.DateField()
#    c



    def get_absolute_url(self):
        return reverse('session_detail', args=[str(self.id)])

    def __str__(self):
        return self.session_name
    
    
    
