from django.urls import path
from . import views


urlpatterns = [
    path('create_employee/', views.create_employee, name="create_employee"),
    path('list_employee/', views.view_all_employees, name="list_employee"),
    path('delete_employee/', views.delete_employee, name="delete_employee")
]