from django.urls import path

import accounts.views as views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('create/', views.AccountCreateView.as_view(), name='employee-retrieve'),
]