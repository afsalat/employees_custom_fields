from django.urls import path
from . import views


urlpatterns = [ 
    path('create-custom-field/', views.CreateCustomField, name="CreateCustomField"),
    path('update-custom-field/<int:field_id>/', views.UpdateCustomField, name="UpdateCustomField"),
    path('delete-custom-field/<int:field_id>/', views.DeleteCustomField, name="DeleteCustomField"),
    path('view-all-fields/', views.ViewAllCustomField, name="ViewAllCustomField")
]