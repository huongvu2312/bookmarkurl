from django.urls import path

from user import views

urlpatterns = [
    path('user/', views.MyAccount.as_view()),
]
