from api_service.views import CustomUserList,CustomUserDetails
from django.urls import path

urlpatterns = [
    path('user',CustomUserList.as_view(),name='customuser_list'),
    path('user/<int:pk>',CustomUserDetails.as_view(),name='customuser_details')
]