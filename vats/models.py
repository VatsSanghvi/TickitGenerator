from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from datetime import timedelta
from twilio.rest import Client
import os

class Category(models.Model):

    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")

    def __str__(self):
        return self.name  


class Subcategory(models.Model):

    category = models.ForeignKey("vats.Category", on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Subcategory")
        verbose_name_plural = _("Subcategorys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Subcategory_detail", kwargs={"id": self.id})

class Ticket(models.Model):
    status_choice = (
        ("Pending","Pending"),                  # Admin     => Approve with assignment, Reject with comment
        ("Assigned","Assigned"),                # Assigned to Manager, Created by Viewer   => Cancel ticket
        ("Scoping","Scoping"),                  # Assigned to Manager, Created by Viewer   => Cancel ticket
        ("In Progress","In Progress"),          # Assigned to Manager, Created by Viewer   => Cancel ticket
        ("Completed","Completed"),
        ("Cancelled","Cancelled"),
        ("Rejected", "Rejected")
    )
    
    # Approve           => admin                                    => from approval to assigned stage
    # Reject            => admin                                    => from approval to Rejected stage
    # Scoping           => Assigned to manager                      => from assigned to Scoping stage
    # In Progress       => Assigned to manager                      => from scoping to in progress stage
    # Completed         => Assigned to manager                      => from in progress to completed stage
    # Cancel Ticket     => Assigned to manager, Created by Viewer   => from (Assigned, Scoping, In progress) to Cancelled stage
    
    priority_choice = (
        ("High","High"),
        ("Moderate","Moderate"),
        ("Low","Low"),
    )
    number = models.CharField(_("Number"), max_length=50, null=True, blank=True)
    category = models.ForeignKey("vats.Category",on_delete=models.CASCADE)
    subcategory = models.ForeignKey("vats.Subcategory",on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50,)
    problem_descp = models.TextField(_("Problem Description"), max_length=500)
    created_by = models.ForeignKey("registration.User", related_name=_("Issues"), on_delete=models.CASCADE)
    priority = models.CharField(_("Priority"), max_length=50,null=True,blank=True,choices=priority_choice)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True,)
    assigned_to = models.ForeignKey("registration.User",related_name=_("Tasks"), on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField(_("Status"), max_length=50,choices=status_choice,null=True,blank=True)
   
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        if not self.number:
            latest = Ticket.objects.all().order_by('number').last()
            if latest:
                number = int(latest.number[3:]) + 1
            else:
                number = 1
            str_zeros = ""
            for _ in range(6 - len(str(number))):
                str_zeros += "0"
            self.number = "TKT" + str_zeros + str(number)
            
        # account_sid = 'ACcad8c9cd24dc3fa5b6c96ce3cb9cee56'
        # auth_token = 'e43dbe58d768be26b75f9321aae75420'
        # client = Client(account_sid, auth_token)

        # message = client.messages.create(
        #                             body='Hello, Your Ticket has been generated kindly check it in your portal',
        #                             from_='+17752567143',
        #                             # to=str(self.created_by.phone_number)
        #                             to='+917048850488'
        #                         )

        # print(message.sid)
        return super(Ticket, self).save(*args, **kwargs)
    
    def is_open(self):
        if self.status == 'Completed' or self.status == 'Cancelled':
            return False
        return True
    
    def get_created_at(self):
        date = self.created_at + timedelta(days=0, hours=5, minutes=30)
        return date
    
    def get_updated_at(self):
        date = self.updated_at + timedelta(days=0, hours=5, minutes=30)
        return date

# class WorkNote(models.Model):

#     ticket = models.ForeignKey("vats.Ticket",related_name="Worknotes", on_delete=models.CASCADE)
#     comment = models.TextField(_("Comments"))
#     commented_by = models.ForeignKey("registration.User", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(_("Created Date/Time"), auto_now_add=True)
    
#     class Meta:
#         verbose_name = _("WorkNote")
#         verbose_name_plural = _("WorkNotes")

#     def __str__(self):
#         return str(self.ticket.created_by) + " - " + self.comments

#     def get_absolute_url(self):
#         return reverse("WorkNote_detail", kwargs={"id": self.id})