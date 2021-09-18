from django.contrib import admin
from .models import Ticket, WorkNotes

# Register your models here.
admin.site.register(Ticket)
admin.site.register(WorkNotes)