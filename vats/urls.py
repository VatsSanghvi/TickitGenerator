from . import views
from django.urls import path




urlpatterns = [
    path('ticket_create/', views.ticket_create, name='ticket_create'),
    path('ticket_list/', views.ticket_list, name='ticket_list'),
    path('ticket_list/<str:status>', views.ticket_list_status, name='ticket_list_status'),
    path('ticket_update/<int:id>', views.ticket_update, name='ticket_update'),
    path('ticket_delete/<int:id>', views.ticket_delete, name='ticket_delete'),
    path('ticket_detail/<int:id>', views.ticket_detail, name='ticket_detail'),
    path('category_create/', views.category_create, name='category_create'),
    path('category_list/', views.category_list, name='category_list'),
    path('subcategory_create/', views.subcategory_create, name='subcategory_create'),
    path('subcategory_list/', views.subcategory_list, name='subcategory_list'),
    path('ticket_completed/<int:id>', views.ticket_completed, name='ticket_completed'),
    path('ticket_cancelled/<int:id>', views.ticket_cancelled, name='ticket_cancelled'),
    path('email_template/',views.ticket_create, name='email_template'),


]