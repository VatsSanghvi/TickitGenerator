from django import forms
from .models import Ticket,Category,WorkNotes,Subcategory



class TicketForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ("Category", "title","problem_descp")

class TicketUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ("Category", "title","problem_descp","assigned_to","priority")


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ("name",)
        
class SubcategoryForm(forms.ModelForm):
    
    class Meta:
        model = Subcategory
        fields = ("name",)

class WorkNotesForm(forms.ModelForm):
    
    class Meta:
        model = WorkNotes
        fields = ("ticket","comments")
