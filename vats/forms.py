from django import forms
from .models import Ticket,Category,WorkNotes,Subcategory



class TicketForm(forms.ModelForm):
    # subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.filter(category__id = self.fields['category']))
    
    class Meta:
        model = Ticket
        fields = ("category", "subcategory", "title","problem_descp")

class TicketUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ("category", "title","problem_descp","assigned_to","priority")


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ("name",)
        
class SubcategoryForm(forms.ModelForm):
    
    class Meta:
        model = Subcategory
        fields = ("category", "name")

class WorkNotesForm(forms.ModelForm):
    
    class Meta:
        model = WorkNotes
        fields = ("ticket","comments")
