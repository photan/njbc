from django.utils.translation import ugettext_lazy as _
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from crispy_forms.layout import Submit, HTML, Button, Field, Div, Fieldset
from crispy_forms.bootstrap import FormActions, TabHolder, Tab

import datetime;

from club.models import Session
from club.models import Person
from club.models import Instructor, PlayerParticipation

COURTS=  (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'))
PERSONS_COUNT =  (('1','1'),('2','2'),('3','3'),('4','4'))

DURATION_MIN = (('30',  '0.5 hour'),
                ('60',  '1.0 hour'),
                ('90',  '1.5 hour'),
                ('120', '2.0 hour'),
                ('150', '2.5 hour'),
                ('180', '3.0 hour'))

SESSION_TIMES =  (('0900','09:00 AM'),
                  ('0930','09:30 AM'),
                  ('1000','10:00 AM'),
                  ('1030','10:30 AM'),
                  ('1100','11:00 AM'),
                  ('1130','11:30 AM'),
                  ('1200','12:00 PM'),
                  ('1230','12:30 PM'),
                  ('1300','01:00 PM'),
                  ('1330','01:30 PM'),
                  ('1400','02:00 PM'),
                  ('1430','02:30 PM'),
                  ('1500','03:00 PM'),
                  ('1530','03:30 PM'),
                  ('1600','04:00 PM'),
                  ('1630','04:30 PM'),
                  ('1700','05:00 PM'),
                  ('1730','05:30 PM'),
                  ('1800','06:00 PM'),
                  ('1830','06:30 PM'),
                  ('1900','07:00 PM'),
                  ('1930','07:30 PM'),
                  ('2000','08:00 PM'),
                  ('2030','08:30 PM'),
                  ('2100','09:00 PM'),
                  )
                                                        
SESSION_TYPES = (('private','Private'),
                 ('summer_camp', 'Summer Camp'),
                 ('junior_training','Junior Training'))                                                        

form_choose_session_type = forms.ChoiceField(required=False, 
                                             choices = (('adhoc','Ad Hoc'),
                                                        ('summer_camp', 'Summer Camp'),
                                                        ('junior_training','Junior Training')),
                                             initial='junior_training',
                                             widget=forms.Select(attrs={'class':'input-block-level'}))

form_choose_duration_min = forms.ChoiceField(required=False, 
                                             choices = (('30',  '0.5 hour'),
                                                        ('60',  '1.0 hour'),
                                                        ('90',  '1.5 hour'),
                                                        ('120', '2.0 hour'),
                                                        ('150', '2.5 hour'),
                                                        ('180', '3.0 hour')),                                                   
                                             initial='session',
                                             widget=forms.Select(attrs={'class':'input-block-level'}))


form_choose_court =         forms.ChoiceField(required=False, 
                                              choices = (('',  '-NA-'),
                                                        ('1', '1'),
                                                        ('2', '2'),
                                                        ('3', '3'),
                                                        ('4', '4'),
                                                        ('5', '5'),
                                                        ('6', '6'),
                                                        ('7', '7')),                                                   
                                             initial='session',
                                             widget=forms.Select(attrs={'class':'input-block-level'}))



form_choose_session_time = forms.ChoiceField(required=False, 
                                             choices = (('0900','09:00 AM'),
                                                        ('0930','09:30 AM'),
                                                        ('1000','10:00 AM'),
                                                        ('1030','10:30 AM'),
                                                        ('1100','11:00 AM'),
                                                        ('1130','11:30 AM'),
                                                        ('1200','12:00 PM'),
                                                        ('1230','12:30 PM'),
                                                        ('1300','01:00 PM'),
                                                        ('1330','01:30 PM'),
                                                        ('1400','02:00 PM'),
                                                        ('1430','02:30 PM'),
                                                        ('1500','03:00 PM'),
                                                        ('1530','03:30 PM'),
                                                        ('1600','04:00 PM'),
                                                        ('1630','04:30 PM'),
                                                        ('1700','05:00 PM'),
                                                        ('1730','05:30 PM'),
                                                        ('1800','06:00 PM'),
                                                        ('1830','06:30 PM'),
                                                        ('1900','07:00 PM'),
                                                        ('1930','07:30 PM'),
                                                        ('2000','08:00 PM'),
                                                        ('2030','08:30 PM'),
                                                        ('2100','09:00 PM'),
                                                        ),
                                                        initial='1000',
                                                        widget=forms.Select(attrs={'class':'input-block-level'}))

class SessionFormOld(forms.ModelForm):
      """Model Session Form"""
      class Meta:
        model = Session
        fields = '__all__'

class SessionDetailForm(forms.ModelForm):
      """Model Session Form"""
      players       = forms.ModelMultipleChoiceField(required=False, queryset=Person.objects.filter(id=1))
      instructors   = forms.ModelMultipleChoiceField(required=False, queryset=Instructor.objects.filter(id=1))

      class Meta:
        model = Session
        fields = ['session_type','session_name','start_time','duration_min',
                  ]

      def __init__(self, *args, **kwargs):
            super(SessionDetailForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'
            self.helper.form_action = ""

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
            
            this_year = datetime.datetime.today().year
            #self.fields['njbc_expiry_date'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+3))
            #self.fields['njbc_since'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+2))

            self.fields['session_type'].widget.attrs['readonly'] = True
            
            self.fields['session_name'].widget.attrs['readonly'] = True

            self.fields['duration_min'].widget = forms.Select(choices=DURATION_MIN)
            self.fields['duration_min'].label = 'Duration'
            self.fields['duration_min'].widget.attrs['readonly'] = True

            self.fields['players'].widget.attrs['readonly'] = True
            self.fields['players'].widget.attrs['size'] = 10
            self.fields['players'].queryset = self.instance.players.all()
            self.fields['instructors'].queryset = self.instance.instructors.all()
            self.fields['instructors'].widget.attrs['readonly'] = True
            self.fields['instructors'].widget.attrs['size'] = 2
            
            # Change the default date formatting
          
            self.fields['start_time'].widget = forms.DateTimeInput(format="%b-%d-%Y  %I:%M %p")
            self.fields['start_time'].widget.attrs['readonly'] = True
            self.fields['start_time'].label = 'Date'

            self.helper.layout = layout.Layout(
              Fieldset(
                'Session',
                'session_type',
                'session_name',
               
                 ),
              Fieldset(
                'Schedule',
                'start_time',
                'duration_min',
                
                'instructors'
                ),
              Fieldset(
                'Players',
                'players'),
                
              FormActions(
                     Submit('edit', 'Edit'),
                     HTML('<a class="btn btn-warning", href= {% url "session_assign_player" object.id %}>Add Player</a>')
                   ),
              )



class SessionUpdateForm(forms.ModelForm):
      players       = forms.ModelMultipleChoiceField(required=False, queryset=Person.objects.filter(id=1))
      instructors   = forms.ModelMultipleChoiceField(required=False, queryset=Instructor.objects.filter(id=1))
      session_time  = form_choose_session_time
     
      """Model Session Form"""
      class Meta:
        model = Session
        fields = ['session_type','session_name','start_time','duration_min']

      def __init__(self, *args, **kwargs):
            super(SessionUpdateForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'
            self.helper.form_action = ""

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-8'
            
            this_year = datetime.datetime.today().year
            #self.fields['njbc_expiry_date'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+3))
            #self.fields['njbc_since'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+2))

            self.fields['session_type'].widget.attrs['readonly'] = True
            self.fields['session_name'].widget.attrs['readonly'] = True
            
            self.fields['duration_min'].widget = forms.Select(choices=DURATION_MIN)
            
            self.fields['players'].queryset = self.instance.players.all()
            self.fields['instructors'].queryset = self.instance.instructors.all()
          
            
            # Change the default date formatting

            self.fields['start_time'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+3))
            self.fields['start_time'].label = 'Date'

            self.helper.layout = layout.Layout(
              Fieldset(
                'Session',
                'session_type',
                'session_name',
                 ),
              Fieldset(
                'Schedule',
                'start_time',
                'session_time',
                'duration_min',
                
                'instructors'
                ),
              Fieldset(
                'Players',
                'players'),
                
              FormActions(
                     Submit('save', 'Save'),
                     Submit('remove_players', 'Remove Players'),
                     Submit('remove_instructors', 'Remove Instructors'),    
                     Submit('delete_session', 'Delete Empty Session'),                 
                     )
              )                
        

class SessionForm(forms.ModelForm):
    player       = forms.ModelChoiceField(required=False, queryset=Person.objects.all(), widget=forms.Select(attrs={'class':'input-block-level'}))
    instructor   = forms.ModelChoiceField(required=False, queryset=Instructor.objects.all(), widget=forms.Select(attrs={'class':'input-block-level'}))
    #session_type = form_choose_session_type
    session_time = form_choose_session_time
    #duration_min = form_choose_duration_min
    #court        = form_choose_court
      
    #start_date = forms.SelectDateWidget()
    class Meta:
        model = Session
        fields =  [  'start_time', 'duration_min']
        

    def __init__(self, *args, **kwargs):
            super(SessionForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_action = ""
            self.helper.form_method = "POST"
            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
            

            this_year = datetime.datetime.today().year
           
            self.fields['start_time'].label  = 'Date'
            self.fields['start_time'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year,this_year+2))

            self.fields['duration_min'].widget = forms.Select(choices=DURATION_MIN)
            self.fields['duration_min'].label = 'Duration'
            self.fields['duration_min'].initial = 90

            
          
            self.helper.layout = layout.Layout(
                layout.Fieldset(    
                    _("Create New Session"),
                    layout.Field('start_time'),

                    layout.Field('session_time'),
                    layout.Field('duration_min'),
                    layout.Field('player'),
                    layout.Field('instructor'),
                    ),
                layout.Fieldset(_(" ")),
                bootstrap.FormActions(
                    layout.Submit("submit",_("Save")),
                    )
                )


class SessionPrivateForm(forms.ModelForm):
    player       = forms.ModelChoiceField(required=False, queryset=Person.objects.all(), widget=forms.Select(attrs={'class':'input-block-level'}))
    instructor   = forms.ModelChoiceField(required=False, queryset=Instructor.objects.all(), widget=forms.Select(attrs={'class':'input-block-level'}))
    #session_type = form_choose_session_type
    session_time = form_choose_session_time
    #duration_min = form_choose_duration_min
    #court        = form_choose_court
      
    #start_date = forms.SelectDateWidget()
    class Meta:
        model = Session
        fields =  [ 'session_type', 'start_time', 'duration_min']
        

    def __init__(self, *args, **kwargs):
            super(SessionPrivateForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_action = ""
            self.helper.form_method = "POST"
            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'

            self.fields['session_type'].widget = forms.Select(choices=SESSION_TYPES)
            self.fields['session_type'].initial = 'private'

            this_year = datetime.datetime.today().year
            self.fields['start_time'].label  = 'Date'
            self.fields['start_time'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year,this_year+2))
           
            self.fields['duration_min'].widget = forms.Select(choices=DURATION_MIN)
            self.fields['duration_min'].initial = 60

            #self.fields['persons_count'].widget = forms.Select(choices=PERSONS_COUNT)
            #self.fields['persons_count'].initial = 1
            #self.fields['court'].widget = forms.Select(choices=COURTS)
            
            self.helper.layout = layout.Layout(
                layout.Fieldset(    
                    _("Create New Private Session"),
                    layout.Field('session_type'),
                    layout.Field('start_time'),

                    layout.Field('session_time'),
                    layout.Field('duration_min'),
                    layout.Field('player'),
                    layout.Field('instructor'),
                    ),
                layout.Fieldset(_(" ")),
                bootstrap.FormActions(
                    layout.Submit("submit",_("Save")),
                    )
                )


class SessionAssignPlayerForm(forms.ModelForm):
    player       = forms.ModelChoiceField(required=False, queryset=Person.objects.all(), widget=forms.Select(attrs={'class':'input-block-level'}))
    class Meta:
        model = Session
        fields =  []
        

    def __init__(self, *args, **kwargs):
            super(SessionAssignPlayerForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_action = ""
            self.helper.form_method = "POST"

          
            self.helper.layout = layout.Layout(
                layout.Fieldset(    
                    _("Assign Player"),
                    layout.Field('player'),
                    ),
                layout.Fieldset(_(" ")),
                bootstrap.FormActions(
                    layout.Submit("submit",_("Add")),
                    )
                )

class SessionAssignPlayersForm(forms.ModelForm):
    players_list       = forms.ModelMultipleChoiceField(required=False, queryset=Person.objects.all())
    class Meta:
        model = Session
        fields =  []
        

    def __init__(self, *args, **kwargs):
            super(SessionAssignPlayersForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_action = ""
            self.helper.form_method = "POST"

            self.fields['players_list'].widget.attrs['size'] = 15
            self.helper.layout = layout.Layout(
                layout.Fieldset(    
                    _("Assign Player"),
                    layout.Field('players_list'),
                    ),
                layout.Fieldset(_(" ")),
                bootstrap.FormActions(
                    layout.Submit("submit",_("Add Players")),
                    )
                )            

class SessionAssignInstructorForm(forms.ModelForm):
    instructor   = forms.ModelChoiceField(required=False, queryset=Instructor.objects.all(), widget=forms.Select(attrs={'class':'input-block-level'}))
    class Meta:
        model = Session
        fields =  []
        

    def __init__(self, *args, **kwargs):
            super(SessionAssignInstructorForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_action = ""
            self.helper.form_method = "POST"

          
            self.helper.layout = layout.Layout(
                layout.Fieldset(    
                    _("Assign Instructor"),
                    layout.Field('instructor'),
                    ),
                layout.Fieldset(_(" ")),
                bootstrap.FormActions(
                    layout.Submit("submit",_("Add")),
                    )
                )



class PersonDetailForm2(forms.ModelForm):
      """Model Session Form"""
      class Meta:
        model = Person
        fields = ['first_name', 'last_name','email','phone','sibling_eldest',
                  'emergency_contact','emergency_email','emergency_phone',
                  'njbc_expiry_date','njbc_since','usba_id'
                  ]

      def __init__(self, *args, **kwargs):
            super(PersonForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-4'
            
            self.helper.form_action = ""
            self.helper.form_method = "POST"
            

          
            self.helper.layout = layout.Layout(
              TabHolder(
                Tab('Basic Information',
                   Field('first_name'),
                   Field('last_name')),                
                Tab('Contact',
                    'email',
                    'phone'),                
                Tab('Emergency Contact',
                    'emergency_contact',
                    'emergency_email',
                    'emergency_phone'),
                Tab('NJBC Membership',
                    'njbc_expiry_date',
                    'njbc_since'),
                Tab('Sibling Association',
                    'sibling_eldest'),
                Tab('USBA Membership',
                    'usba_id')),
                FormActions(
                     Submit('save', 'Save changes'),
                     Button('cancel', 'Cancel'))
                )
            #self.helper.layout = layout.Layout(
            #  'sname','email'
            #    )

class PersonForm(forms.ModelForm):
      """Model Session Form"""
      class Meta:
        model = Person
        fields = ['first_name', 'last_name','email','phone','sibling_eldest',
                  'emergency_contact','emergency_email','emergency_phone',
                  'njbc_id','njbc_expiry_date','njbc_since','usba_id'
                  ]

      def __init__(self, *args, **kwargs):
            super(PersonForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'
            self.helper.form_action = ""

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
            
            this_year = datetime.datetime.today().year
            self.fields['njbc_expiry_date'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+3))
            self.fields['njbc_since'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+2))

            #MultiWidgetField('field_name', ))
            self.helper.layout = layout.Layout(
              TabHolder(
                Tab('Basic Information',
                   Field('first_name'),
                   Field('last_name')),                
                Tab('Contact',
                    'email',
                    'phone'),                
                Tab('Emergency Contact',
                    'emergency_contact',
                    'emergency_email',
                    'emergency_phone'),
                Tab('Sibling Association',
                    'sibling_eldest'),
                Tab('NJBC Membership',
                    'njbc_id',
                    'njbc_expiry_date',
                    'njbc_since'),
                Tab('USBA Membership',
                    'usba_id')),
                FormActions(
                     Submit('save', 'Save'),
                     Button('cancel', 'Cancel'))
                )
            #self.helper.layout = layout.Layout(
            #  'sname','email'
            #    )

class PersonEditForm(forms.ModelForm):
      """Model Session Form"""
      class Meta:
        model = Person
        fields = ['first_name', 'last_name','email','phone','sibling_eldest',
                  'emergency_contact','emergency_email','emergency_phone',
                  'njbc_expiry_date','njbc_since','usba_id'
                  ]

      def __init__(self, *args, **kwargs):
            super(PersonEditForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'
            self.helper.form_action = ""

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
            
            this_year = datetime.datetime.today().year
            self.fields['njbc_expiry_date'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+3))
            self.fields['njbc_since'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+2))


            #MultiWidgetField('field_name', ))
            self.helper.layout = layout.Layout(
              TabHolder(
                Tab('Basic Information',
                   Field('first_name'),
                   Field('last_name')),                
                Tab('Contact',
                    'email',
                    'phone'),                
                Tab('Emergency Contact',
                    'emergency_contact',
                    'emergency_email',
                    'emergency_phone'),
                Tab('Sibling Association',
                    'sibling_eldest'),
                Tab('NJBC Membership',
                    'njbc_expiry_date',
                    'njbc_since'),
                Tab('USBA Membership',
                    'usba_id')),
                FormActions(
                     Submit('save', 'Update Changes'),
                     HTML('<a class="btn btn-warning", href= {% url "player_delete" object.id %}>Delete</a>'))
                )
            #self.helper.layout = layout.Layout(
            #  'sname','email'
                
class PersonDetailForm(forms.ModelForm):
      """Model Session Form"""
      class Meta:
        model = Person
        fields = ['first_name', 'last_name','email','phone','sibling_eldest',
                  'emergency_contact','emergency_email','emergency_phone',
                  'njbc_expiry_date','njbc_since','usba_id'
                  ]

      def __init__(self, *args, **kwargs):
            super(PersonDetailForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'
            self.helper.form_action = ""

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
            
            this_year = datetime.datetime.today().year
            #self.fields['njbc_expiry_date'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+3))
            #self.fields['njbc_since'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+2))

            self.fields['first_name'].widget.attrs['readonly'] = True
            
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['phone'].widget.attrs['readonly'] = True

            self.fields['emergency_contact'].widget.attrs['readonly'] = True
            self.fields['emergency_email'].widget.attrs['readonly'] = True
            self.fields['emergency_phone'].widget.attrs['readonly'] = True
            self.fields['sibling_eldest'].widget.attrs['readonly'] = True
            self.fields['usba_id'].widget.attrs['readonly'] = True
            

            
            # Change the default date formatting
            self.fields['njbc_since'].label = "Member Since"
            self.fields['njbc_expiry_date'].widget = forms.DateInput(format="%b-%d-%Y")
            self.fields['njbc_since'].widget = forms.DateInput(format="%b-%d-%Y")
            self.fields['njbc_expiry_date'].widget.attrs['readonly'] = True
            self.fields['njbc_since'].widget.attrs['readonly'] = True

            self.fields['njbc_expiry_date'].label = 'Expiry Date'

            self.fields['usba_id'].label = 'USBA ID'
            #MultiWidgetField('field_name', ))
            self.helper.layout = layout.Layout(
              TabHolder(
                Tab('Basic Information',
                   Field('first_name'),
                   Field('last_name',readonly=True)),                
                Tab('Contact',
                    'email',
                    'phone'),                
                Tab('Emergency Contact',
                    'emergency_contact',
                    'emergency_email',
                    'emergency_phone'),
                Tab('Sibling Association',
                    'sibling_eldest'),
                Tab('NJBC Membership',
                    'njbc_expiry_date',
                    'njbc_since'),
                Tab('USBA Membership',
                    'usba_id')),
                FormActions(
                     Submit('edit', 'Edit'))
                )
            #self.helper.layout = layout.Layout(
            #  'sname','email'
            #    )


#---------------------------------------------------Instructor
class InstructorDetailForm2(forms.ModelForm):
      """Model Session Form"""
      class Meta:
        model = Instructor
        fields = ['first_name','last_name','email',
                  'emergency_contact','emergency_email','emergency_phone',
                  'usba_id'
                 ]

      def __init__(self, *args, **kwargs):
            super(InstructorForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
          
            self.helper.layout = layout.Layout(
              TabHolder(
                Tab('Basic Information',
                   Field('first_name'),
                   Field('last_name')),                
                Tab('Contact',
                    'email'),                
                Tab('Emergency Contact',
                    'emergency_contact',
                    'emergency_email',
                    'emergency_phone'),
                Tab('USBA Membership',
                    'usba_id')),
                FormActions(
                     Submit('save', 'Save changes'))
                )


class InstructorForm(forms.ModelForm):
      """Model Session Form"""
      class Meta:
        model = Instructor
        fields = ['first_name','last_name','email',
                  'emergency_contact','emergency_email','emergency_phone',
                  'usba_id'
                  ]

      def __init__(self, *args, **kwargs):
            super(InstructorForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'
            self.helper.form_action = ""

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
            
            this_year = datetime.datetime.today().year

            #MultiWidgetField('field_name', ))
            self.helper.layout = layout.Layout(
              TabHolder(
                Tab('Basic Information',
                   Field('first_name'),
                   Field('last_name')),                
                Tab('Contact',
                    'email'),                
                Tab('Emergency Contact',
                    'emergency_contact',
                    'emergency_email',
                    'emergency_phone'),
                Tab('USBA Membership',
                    'usba_id')),
                FormActions(
                     Submit('save', 'Save'),
                     Button('cancel', 'Cancel'))
                )
            #self.helper.layout = layout.Layout(
            #  'sname','email'
            #    )

class InstructorEditForm(forms.ModelForm):
      """Model Session Form"""
      class Meta:
        model = Instructor
        fields = ['first_name','last_name','email',
                  'emergency_contact','emergency_email','emergency_phone',
                  'usba_id'
                  ]

      def __init__(self, *args, **kwargs):
            super(InstructorEditForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'
            self.helper.form_action = ""

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
            
            #MultiWidgetField('field_name', ))
            self.helper.layout = layout.Layout(
              TabHolder(
                Tab('Basic Information',
                   Field('first_name'),
                   Field('last_name')),                
                Tab('Contact',
                    'email'),                
                Tab('Emergency Contact',
                    'emergency_contact',
                    'emergency_email',
                    'emergency_phone'),
                Tab('USBA Membership',
                    'usba_id')),
                FormActions(
                     Submit('save', 'Update Changes'))
                )
                
class InstructorDetailForm(forms.ModelForm):
      """Model Session Form"""
      class Meta:
        model = Instructor
        fields = ['first_name','last_name','email',
                  'emergency_contact','emergency_email','emergency_phone',
                  'usba_id'
                 ]
                  
      def __init__(self, *args, **kwargs):
            super(InstructorDetailForm,self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            #self.helper.form_tag = False
            self.helper.form_method = 'POST'
            self.helper.form_action = ""

            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
            
            this_year = datetime.datetime.today().year
            #self.fields['njbc_expiry_date'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+3))
            #self.fields['njbc_since'].widget = forms.SelectDateWidget(attrs={'style': 'width: 20%; display: inline-block;'},years=range(this_year-10,this_year+2))

            self.fields['first_name'].widget.attrs['readonly'] = True
            
            self.fields['email'].widget.attrs['readonly'] = True
          
            self.fields['emergency_contact'].widget.attrs['readonly'] = True
            self.fields['emergency_email'].widget.attrs['readonly'] = True
            self.fields['emergency_phone'].widget.attrs['readonly'] = True
            
            self.fields['usba_id'].widget.attrs['readonly'] = True
                     
            self.fields['usba_id'].label = 'USBA ID'
            #MultiWidgetField('field_name', ))
            self.helper.layout = layout.Layout(
              TabHolder(
                Tab('Basic Information',
                   Field('first_name'),
                   Field('last_name',readonly=True)),                
                Tab('Contact',
                    'email'),                
                Tab('Emergency Contact',
                    'emergency_contact',
                    'emergency_email',
                    'emergency_phone'),
                Tab('USBA Membership',
                    'usba_id')),
                FormActions(
                     Submit('edit', 'Edit'))
                )

