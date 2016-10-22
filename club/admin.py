from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Person)
admin.site.register(Instructor)
admin.site.register(Session)
admin.site.register(PlayerParticipation)
admin.site.register(InstructorParticipation)
