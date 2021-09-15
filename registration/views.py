from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, 
    CreateView, UpdateView, DeleteView,
)
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# FORM
from .forms import CustomUserCreationForm

# DECORATORS
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import admin_required

@login_required
def home(request):
    context = {}
    return render(request, 'registration/home.html', context)

# USER CBV

@method_decorator(admin_required, name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
    model = User

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user_details'

@method_decorator(admin_required, name='dispatch')
class UserCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/user_form.html'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name')