from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

class Category(models.Model):

    name = models.CharField(_("Category"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")

    def __str__(self):
        return self.name  


class Subcategory(models.Model):

    Category = models.ForeignKey("vats.Category", on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(_("Subcategory"), max_length=50)

    class Meta:
        verbose_name = _("Subcategory")
        verbose_name_plural = _("Subcategorys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Subcategory_detail", kwargs={"pk": self.pk})

class Ticket(models.Model):
    
    status_choice = (
        ("Cancelled","Cancelled"),
        ("Assigned","Assigned"),
        ("In Progress","In Progress"),
        ("Pending","Pending"),
        ("Completed","Completed"),
    )
    priority_choice = (
        ("High","High"),
        ("Moderate","Moderate"),
        ("Low","Low"),
    )
    Category = models.ForeignKey("vats.Category",on_delete=models.SET_NULL,blank=True,null=True)
    Subcategory = models.ForeignKey("vats.Subcategory",on_delete=models.SET_NULL,blank=True,null=True)
    title = models.CharField(_("Title"), max_length=50,)
    problem_descp = models.TextField(_("Problem Description"), max_length=500)
    created_by = models.ForeignKey("registration.User", related_name=_("Issues"), on_delete=models.CASCADE)
    priority = models.CharField(_("Priority"), max_length=50,null=True,blank=True,choices=priority_choice)
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


