from django import forms
from .models import Ticket,Category



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