from django.contrib import admin
from .models import Ticket, WorkNotes,Category,Subcategory

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(WorkNotes)