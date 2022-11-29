from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('sign-up/', views.sign_up, name='sign_up_url'),
path("follow/", views.follow, name="follow_url"),
path("edit-profile/", views.edit_profile, name="delete_account_url")
]