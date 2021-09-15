from . import views
from django.urls import path




urlpatterns = [
    path('ticket_create/', views.ticket_create, name='ticket_create'),
    path('ticket_list/', views.ticket_list, name='ticket_list'),
    path('ticket_update/<int:id>', views.ticket_update, name='ticket_update'),
    path('ticket_delete/<int:id>', views.ticket_delete, name='ticket_delete'),
    path('ticket_detail/<int:id>', views.ticket_detail, name='ticket_detail'),
    path('category_create/', views.category_create, name='category_create'),
    path('category_list/', views.category_list, name='category_list'),
]