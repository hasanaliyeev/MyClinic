from django.contrib import admin

from .models import Schedule, Doctor, Education, Appointment

admin.site.register(Schedule)
admin.site.register(Doctor)
admin.site.register(Education)
admin.site.register(Appointment)
