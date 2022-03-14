from django.shortcuts import redirect, render
from .models import  Ticket,Category,Subcategory #,WorkNote
from .forms import TicketForm,CategoryForm, TicketUpdateForm,SubcategoryForm, TicketApproveForm, TicketRejectForm
from registration.models import User
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from tickit import settings


from registration.decorators import manager_required, viewer_required, admin_required, viewernotallowed
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
@viewer_required
def ticket_create(request):
    context = {}
    form = TicketForm()
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.status = "Pending"
            
            ticket.save()
            messages.success(request, 'Your tickit has been created successfully.')
            
            html_message = render_to_string('vats/email_template.html', {'context': ticket})
            message = EmailMessage('New Ticket Generated', html_message, settings.EMAIL_HOST_USER, [request.user.email])
            message.content_subtype = 'html'
            try:
                message.send()
            except Exception as e:
                print("Error",e)
        
            return redirect('ticket_list')

    context['form'] = form
    return render(request, 'vats/ticket_create.html', context)

@login_required
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
    
@login_required
def ticket_list_status(request, status):
    context = {}
    context['status'] = status
    if request.user.role == "Admin":
        context['tickets'] = Ticket.objects.filter(status=status)
    elif request.user.role == "Viewer":
        context['tickets'] = Ticket.objects.filter(created_by = request.user , status=status)
    else :
        request.user.role == "Manager"
        context['tickets'] = Ticket.objects.filter(assigned_to=request.user,status=status)

    return render(request, 'vats/ticket_list.html', context)

@login_required
def ticket_detail(request, id):
    ticket = Ticket.objects.get(id=id)
    user = User.objects.get(email=ticket.created_by)
    if ticket.created_by == request.user or request.user.role == "Admin" or ticket.assigned_to == request.user  :

        my_string = "https://wa.me/91" + str(ticket.created_by.phone_number)
        context = {'ticket' : ticket , 'user' : user, "my_string" : my_string}
        return render(request, 'vats/ticket_detail.html', context)
    
    else:
        messages.warning(request, 'You are not allowed to access this page.')
        return redirect('home')

@login_required
@admin_required
def ticket_approve(request, id):
    ticket = Ticket.objects.get(id=id)
    form = TicketApproveForm(instance=ticket)
    form.fields["assigned_to"].queryset = User.objects.filter(role='Manager')
    
    if request.method == 'POST':
        form = TicketApproveForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.status = "Assigned"
            ticket.save()
            return redirect('ticket_list')
    
    context = {}
    context['form'] = form
    context['update_type'] = "Assign"
    return render(request, "vats/ticket_update.html", context)

@login_required
@admin_required
def ticket_reject(request, id):
    ticket = Ticket.objects.get(id=id)
    form = TicketRejectForm(instance=ticket)
    
    context = {}
    context['form'] = form
    context['update_type'] = "Reject"
    return render(request, "vats/ticket_update.html", context)

@login_required
@viewernotallowed
def ticket_update(request, id):

    ticket = Ticket.objects.get(id=id)

    form = TicketUpdateForm(instance=ticket)
    form.fields["assigned_to"].queryset = User.objects.filter(role='Manager')
    
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            # if ticket.assigned_to != None:
            #     ticket.status = 'Assigned'
            # else:
            #     ticket.status = 'Approval'
            if request.user.role == "Admin":
                 if ticket.assigned_to != None:
                    ticket.status = 'Assigned'
            
            if ticket.status == "Completed":
                html_message = render_to_string('vats/email_template.html', {'context': ticket})
                message = EmailMessage('Your ticket has been completed successfully', html_message, settings.EMAIL_HOST_USER, [ticket.created_by])
                message.content_subtype = 'html'
            try:
                message.send()
            except Exception as e:
                print("Error",e)

            ticket.save()
            
            return redirect('ticket_list')
    
    context = {}
    context['form'] = form
    return render(request, "vats/ticket_update.html", context)

@login_required
@admin_required
def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.delete()
    return redirect('ticket_list')


@login_required
@admin_required
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

@login_required
@admin_required
def category_create(request):
    return custom_category_create(
        request = request, 
        custom_form = CategoryForm, 
        render_page = 'vats/category_create.html', 
        redirect_url = 'category_list'
    )
    
    
@login_required
@admin_required
def category_list(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request, 'vats/category_list.html', context)

@login_required
@admin_required
def category_delete(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('category_list')


@login_required
@manager_required
def ticket_completed(request,id):
    ticket = Ticket.objects.get(id=id)
    ticket.status = "Completed"
    ticket.save()
    return redirect('ticket_detail',id)


@login_required
@manager_required
def ticket_cancelled(request,id):
    
    ticket = Ticket.objects.get(id=id)
    ticket.status = "Cancelled"
    ticket.save()
    return redirect('ticket_detail',id)


@login_required
@admin_required
def subcategory_create(request, id):
    context = {}
    form = SubcategoryForm()

    if request.method == "POST":
        print(request.POST)
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.fields['category'].initial = id
            form.save()                     
            messages.success(request, 'Your Subcategory has been created successfully.')
            return redirect('subcategory_list', id)

    form.fields['category'].initial = id
    context['form'] = form
    
    return render(request, 'vats/subcategory_create.html', context)
    

@login_required
@admin_required
def subcategory_list(request, id):
    context = {}
    category = Category.objects.get(id=id)
    context['category'] = category
    context['subcategories'] = Subcategory.objects.filter(category=category)
    return render(request, 'vats/subcategory_list.html', context)

@login_required
@admin_required
def subcategory_delete(request,id):
    subcategory = Subcategory.objects.get(id=id)
    subcategory.delete()
    return redirect('subcategory_list')



@login_required
@manager_required

# def custom_worknotes_create(request, custom_form, render_page, redirect_url):
#     context = {}
#     form = custom_form()

#     if request.method == "POST":
#         form = custom_form(request.POST)
#         if form.is_valid():
#             worknotes = form.save(commit=False)
#             worknotes.commented_by = request.user
            
#             worknotes.save()                     
#             messages.success(request, 'Your comment for cancellation of ticket has been created successfully.')
#             return redirect(redirect_url)

#     context['form'] = form
#     return render(request, render_page, context)

# @login_required
# @manager_required
# def worknotes_create(request,id):
#     return custom_worknotes_create(
#         request = request, 
#         custom_form = WorkNoteForm, 
#         render_page = 'vats/worknotes_create.html', 
#         redirect_url = 'ticket_list'
#     )

def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'vats/subcategory_dropdown_list_options.html', {'subcategories': subcategories})