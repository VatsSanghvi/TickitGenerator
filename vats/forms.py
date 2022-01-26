from django import forms
from .models import Ticket,Category,WorkNotes,Subcategory



class TicketForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ("category", "subcategory", "title","problem_descp")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()
    
class TicketUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ("category","subcategory", "title","problem_descp","created_by","status","assigned_to","priority")
    
    def __init__(self, *args, **kwargs):
        super(TicketUpdateForm,self).__init__(*args, **kwargs)
        self.fields['category'].disabled = True
        self.fields['subcategory'].disabled = True
        self.fields['title'].disabled = True
        self.fields['problem_descp'].disabled = True
        self.fields['created_by'].disabled = True


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
