from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('sign-up/', views.sign_up, name='sign_up_url'),
path("follow/", views.follow, name="follow_url"),
path("edit-profile/", views.edit_profile, name="edit_profile_url"),
path('delete-account/', views.delete_account, name="delete_account_url"),
path('<str:user_name>/followers/', views.followers, name="followers_url"),
path('<str:user_name>/following/', views.following, name="following_url"),
path('<str:user_name>/', views.profile, name="profile_url")
]