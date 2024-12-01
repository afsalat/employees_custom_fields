from django.urls import path
from . import views


urlpatterns = [ 
    path('create-custom-field/', views.create_custom_field, name="CreateCustomField"),
    path('update-custom-field/<int:field_id>/', views.update_custom_field, name="UpdateCustomField"),
    path('delete-custom-field/<int:field_id>/', views.delete_custom_field, name="DeleteCustomField"),
    path('view-all-fields/', views.view_all_custom_fields, name="ViewAllCustomField")
]