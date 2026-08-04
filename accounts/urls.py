from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('forgot-password/', views.forgot_password),
    path('reset-password/', views.reset_password),
    path('profile/', views.get_profile),
    path('contribute-tender/', views.add_tender_public),
    path('tenders/', views.list_tenders),
]