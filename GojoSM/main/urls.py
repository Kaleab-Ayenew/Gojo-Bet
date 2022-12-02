from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index_url'),
path('sign-up/', views.sign_up, name='sign_up_url'),
path("follow/", views.follow, name="follow_url"),
path("unfollow/", views.unfollow, name="unfollow_url"),
path("edit-profile/", views.edit_profile, name="edit_profile_url"),
path('delete-account/', views.delete_account, name="delete_account_url"),
path('@<str:user_name>/followers/', views.followers, name="followers_url"),
path('@<str:user_name>/following/', views.following, name="following_url"),
path('@<str:user_name>/', views.profile, name="profile_url"),
#THE POSTING FUNCTION URLS
path('post/', views.create_post, name = "create_post_url"),
path('@<str:user_name>/posts/', views.get_posts, name="get_post_url"),
path('delete-post/', views.delete_post, name="delete_post_url"),
#Session management functions
path('login/', views.login_view, name="login_view_url"),
path('logout/', views.logout_view, name="logout_view_url"),
#The home feed
path('home/', views.home_feed, name="home_feed_url")
]