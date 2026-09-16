from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('departments/', views.departments, name='departments'),
    path('reports/', views.reports, name='reports'),
    path('directory/', views.employee_list, name='employee_list'),
    path('export/', views.export_employees, name='export_employees'),
    path('bulk-delete/', views.bulk_delete_employees, name='bulk_delete_employees'),
    path('add/', views.add_employee, name='add_employee'),
    path('<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
]