from django.shortcuts import redirect
from django.contrib import messages

def logout_required(my_function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return my_function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper

def admin_required(my_function):
    def wrapper(request, *args, **kwargs):
        if request.user.role == "Admin":
            return my_function(request, *args, **kwargs)
        else:
            messages.warning(request, 'You are not allowed to access this page.')
            return redirect('home')
    return wrapper

def manager_required(my_function):
    def wrapper(request, *args, **kwargs):
        if request.user.role == "Manager":
            return my_function(request, *args, **kwargs)
        else:
            messages.warning(request, 'You are not allowed to access this page.')
            return redirect('home')
    return wrapper

def viewer_required(my_function):
    def wrapper(request, *args, **kwargs):
        if request.user.role == "Viewer":
            return my_function(request, *args, **kwargs)
        else:
            messages.warning(request, 'You are not allowed to access this page.')
            return redirect('home')
    return wrapper

def viewernotallowed(my_function):
    def wrapper(request, *args, **kwargs):
        if request.user.role != "Viewer":
            return my_function(request, *args, **kwargs)
        else:
            messages.warning(request, 'You are not allowed to access this page.')
            return redirect('home')
    return wrapper