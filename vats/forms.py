from django import forms
from .models import Ticket,Category,WorkNotes



class TicketForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ("group", "title","problem_descp")

class TicketUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ("group", "title","problem_descp","assigned_to")


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ("name",)

class WorkNotesForm(forms.ModelForm):
    
    class Meta:
        model = WorkNotes
        fields = ("ticket","comments")
