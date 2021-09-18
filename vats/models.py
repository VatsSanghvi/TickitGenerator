from django.db import models
from django.db.models import Q
from django.db.models.base import Model
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext as _
from django.utils import timezone



class Category(models.Model):

    name = models.CharField(_("Category"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")

    def __str__(self):
        return self.name  

class Ticket(models.Model):
    
    status_choice = (
        ("Cancelled","Cancelled"),
        ("Assigned","Assigned"),
        ("In Progress","In Progress"),
        ("Pending","Pending"),
        ("Completed","Completed"),
    )
    group = models.ForeignKey("vats.Category",on_delete=models.SET_NULL,blank=True,null=True)
    title = models.CharField(_("Title"), max_length=50)
    problem_descp = models.TextField(_("Problem Description"), max_length=500)
    created_by = models.ForeignKey("registration.User", related_name=_("Issues"), on_delete=models.CASCADE)
    start_date_time = models.DateTimeField(_("Start Date Time"), auto_now_add=True)
    end_date_time = models.DateTimeField(_("End Date Time"), null=True, blank=True)
    assigned_to = models.ForeignKey("registration.User",related_name=_("Tasks"), on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField(_("Status"), max_length=50,choices=status_choice)
   
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


    def __str__(self):
        return self.title
    
    def is_open(self):
        if self.status == 'Completed' or self.status == 'Cancelled':
            return False
        return True


class WorkNotes(models.Model):
    ticket = models.ForeignKey("vats.Ticket", on_delete=models.CASCADE)
    comments = models.TextField(_("Comments"))
    commented_by = models.ForeignKey("registration.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    

    class Meta:
        verbose_name = _("WorkNotes")
        verbose_name_plural = _("WorkNotess")

    def __str__(self):
        return str(self.ticket.created_by) + " - " + self.comments

    def get_absolute_url(self):
        return reverse("WorkNotes_detail", kwargs={"pk": self.pk})


