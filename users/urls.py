from django.urls import path

from frontend.views import views_users


app_name = 'users'

urlpatterns=[
    path('register/', views_users.register, name='register'),
    path('login/', views_users.login, name='login'),
]
