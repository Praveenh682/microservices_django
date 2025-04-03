from django.urls import path
from user_app import views

app_name = 'user_app'

urlpatterns = [
    path('create_user/',views.UserCreateAPI.as_view(),name='usercreate'),
    path('create_role/',views.RoleMasterAPI.as_view(),name='rolemaster')
]