from django.shortcuts import redirect, render
from .models import  Ticket,Category,Subcategory
from .forms import TicketForm,CategoryForm, TicketUpdateForm,SubcategoryForm
from registration.models import User
from django.conf import settings
from django.core.mail import send_mail


from registration.decorators import manager_required, viewer_required, admin_required, viewernotallowed
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ( DetailView )

def custom_create(request, custom_form, render_page, redirect_url):
    context = {}
    form = custom_form()

    if request.method == "POST":
        form = custom_form(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.status = "Pending"
            ticket.save()
            messages.success(request, 'Your tickit has been created successfully.')
            
            send_mail(
                'Your Ticket has been generated and its waiting for admins approval',#subject
                'Ticket Details :- ' +
                'Category' + str(ticket.category) +
                'Subcategory' + str(ticket.subcategory) + 
                'Title' + str(ticket.title) + 
                'Problem Description' + str(ticket.problem_descp) + 
                'Created by' + str(ticket.created_by) + 
                'Start Date Time' + str(ticket.start_date_time) ,#message
                settings.EMAIL_HOST_USER,#from email
                [User.email],#To email
            )
        
            return redirect(redirect_url)

    context['form'] = form
    return render(request, render_page, context)


@viewer_required
def ticket_create(request):
    
    return custom_create(
        request = request, 
        custom_form = TicketForm, 
        
        render_page = 'vats/ticket_create.html', 
        redirect_url = 'ticket_list'
    )

def ticket_list(request):
    context = {}
    if request.user.role == "Admin":
        context['tickets'] = Ticket.objects.all()
    elif request.user.role == "Viewer":
        context['tickets'] = Ticket.objects.filter(created_by = request.user)
    else :
        request.user.role == "Manager"
        context['tickets'] = Ticket.objects.filter(assigned_to=request.user)

    return render(request, 'vats/ticket_list.html', context)
    

def ticket_list_status(request,status):
    context = {}
    if request.user.role == "Admin":
        context['tickets'] = Ticket.objects.filter(status=status)
    elif request.user.role == "Viewer":
        context['tickets'] = Ticket.objects.filter(created_by = request.user , status=status)
    else :
        request.user.role == "Manager"
        context['tickets'] = Ticket.objects.filter(assigned_to=request.user,status=status)

    return render(request, 'vats/ticket_list.html', context)


def ticket_detail(request, id):
    ticket = Ticket.objects.get(id=id)
    if ticket.created_by == request.user or request.user.role == "Admin" or ticket.assigned_to == request.user  :
        context = {}
        context['ticket'] = ticket
        return render(request, 'vats/ticket_detail.html', context)
    
    else:
        messages.warning(request, 'You are not allowed to access this page.')
        return redirect('home')

@admin_required
def ticket_update(request, id):

    ticket = Ticket.objects.get(id=id)

    form = TicketUpdateForm(instance=ticket)
    form.fields["assigned_to"].queryset = User.objects.filter(role='Manager')
    
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            if ticket.assigned_to != None:
                ticket.status = 'Assigned'
            else:
                ticket.status = 'Pending'
            ticket.save()
            return redirect('ticket_list')
    
    context = {}
    context['form'] = form
    return render(request, "vats/ticket_update.html", context)

@admin_required
def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.delete()
    return redirect('ticket_list')



def custom_category_create(request, custom_form, render_page, redirect_url):
    context = {}
    form = custom_form()

    if request.method == "POST":
        form = custom_form(request.POST)
        if form.is_valid():
            form.save()                     
            messages.success(request, 'Your Category has been created successfully.')
            return redirect(redirect_url)

    context['form'] = form
    return render(request, render_page, context)


@admin_required
def category_create(request):
    return custom_category_create(
        request = request, 
        custom_form = CategoryForm, 
        render_page = 'vats/category_create.html', 
        redirect_url = 'category_list'
    )
@admin_required
def category_list(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request, 'vats/category_list.html', context)


def ticket_completed(request,id):
    ticket = Ticket.objects.get(id=id)
    ticket.status = "Completed"
    ticket.save()
    return redirect('ticket_detail',id)

def ticket_cancelled(request,id):
    
    ticket = Ticket.objects.get(id=id)
    ticket.status = "Cancelled"
    ticket.save()
    return redirect('ticket_detail',id)


def custom_subcategory_create(request, custom_form, render_page, redirect_url):
    context = {}
    form = custom_form()

    if request.method == "POST":
        form = custom_form(request.POST)
        if form.is_valid():
            form.save()                     
            messages.success(request, 'Your Category has been created successfully.')
            return redirect(redirect_url)

    context['form'] = form
    return render(request, render_page, context)

@admin_required
def subcategory_create(request):
    return custom_subcategory_create(
        request = request, 
        custom_form = SubcategoryForm, 
        render_page = 'vats/subcategory_create.html', 
        redirect_url = 'subcategory_list'
    )
@admin_required
def subcategory_list(request):
    context = {}
    context['categories'] = Subcategory.objects.all()
    return render(request, 'vats/subcategory_list.html', context)