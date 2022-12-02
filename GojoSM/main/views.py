from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.serializers import json
from django.shortcuts import redirect

from datetime import datetime
import random

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from main.serializers import UserSerializer, UserProfileSerializer, FollowingSerializer, PostSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, Following, Post
# Create your views here.
def index(request):

    return HttpResponse("This is working")

@api_view(['GET','POST'])
def sign_up(request):
    if request.method == "GET":
        data = {"Response":"Not there yet"}
        return Response(data)

    elif request.method == "POST":
        print(request.data)
        # user_data = JSONParser().parse(request)
        user_data = request.data
        user_data_main = user_data['main']
        user_data_profile = user_data['profile']

        # Reformat the string date to a python datetime object
        # Or you can just insert it in the form of YYYY-MM-DD ----------- This is UNTESTED(May cause error)
        # user_data_profile['birth_date'] = datetime.strptime(user_data_profile['birth_date'], "%d-%m-%Y").date()

        user_serializer = UserSerializer(data=user_data_main)

        rsp_data = {}

        if user_serializer.is_valid(raise_exception=True):
            
            us = user_serializer.save()

            #Add the current User as the one to which the Profile is going to be added
            user_data_profile['user'] = us.pk
            print(user_data_profile)
            rsp_data['user-data-passed'] = user_serializer.data
            user_profile_serializer = UserProfileSerializer(data=user_data_profile)
            user_profile_serializer.is_valid()
            print("This is validated profile data: ", user_profile_serializer.validated_data)
            if user_profile_serializer.is_valid(raise_exception=True):
                
                usp = user_profile_serializer.save()
                rsp_data['user-profile-data-passed'] = user_profile_serializer.data
                print("Profile Created Succussfully!")
            else:
                print("User Profile is not valid")
                print(user_data_profile)
        else:
            print("User is not valid!")
                
        
        
        rsp_data['status'] = "OK"
        
        
        return Response(rsp_data)

@api_view(['POST'])
def follow(request):
    
    data = request.data
    if request.user.is_authenticated:
        try:
            follower = User.objects.get(username=request.user.username)
            followed = User.objects.get(username=data['followed'])
        except User.DoesNotExist:
            return Response({"Status":"User doesn't exist!"})
        
        data['follower'] = follower.pk
        data['followed'] = followed.pk
        serializer = FollowingSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            fol_obj = serializer.save()
            rspdata = serializer.data
            rspdata['Status'] = "OK"
            return Response(rspdata)
        else:
            return Response({"Status" : "Failed"})
    else:
        return Response({"Status":"Please login!"})

@api_view(['POST'])
def delete_account(request):
    data = request.data
    
    if request.user.is_authenticated:
        username = request.user.username
        try:
            user = User.objects.get(username=username)
            user.delete()
            return Response({"Status": "User has been deleted!"})
        except User.DoesNotExist:
            return Response({"Status":"The Specified User doesn't exist!"})
        except Exception as c:
            print(c)
            return Response({"Status":"Request failed"})
    else:
        return Response({"Status":"You are not logged in!"})

@api_view(['GET','POST'])
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return Response({"Status": "Not there Yet!"})

        elif request.method == "POST":
            data = request.data
            username = request.user.username
            try:
                data['user'] = User.objects.get(username=username).pk
            except User.DoesNotExist:
                return Response({"Error":"The User Doesn't exist"})
            validated_data = data
            profile = UserProfile.objects.get(pk=validated_data['user'])
            profile.first_name = validated_data['first_name']
            profile.last_name = validated_data['last_name']
            profile.country = validated_data['country']
            profile.birth_date = validated_data['birth_date']
            profile.save()

        return Response(data)
    else:
        return Response({"Status":"You are not logged in!"})


@api_view(['GET','POST'])
def followers(request, user_name):


    if request.method == "POST":
        data = {}
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({"Status":"User doesn't exist"})

        query = Following.objects.filter(followed=user)
        data['follower_number'] = len(query)
        f_list = []
        for q in query:
            u_prof = UserProfile.objects.get(user=q.follower)
            f_list.append(f"{u_prof.first_name} {u_prof.last_name}")
        data['follower_list'] = f_list

        return Response(data)
    
    elif request.method == "GET":

        return HttpResponse("Not there YET!")
            
@api_view(['GET','POST'])
def following(request, user_name):


    if request.method == "POST":
        data = {}
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({"Status":"User doesn't exist"})

        query = Following.objects.filter(follower=user)
        data['following_number'] = len(query)
        f_list = []
        for q in query:
            u_prof = UserProfile.objects.get(user=q.followed)
            f_list.append(f"{u_prof.first_name} {u_prof.last_name}")
        data['following_list'] = f_list

        return Response(data)

    elif request.method == "GET":

        return HttpResponse("Not there YET!")

@api_view(["GET","POST"])
def profile(request, user_name):

    if request.method == "GET":
        try: 
            user = User.objects.get(username = user_name)
        except User.DoesNotExist:
            return HttpResponse("User doesn't exist!")

        user_profile= UserProfile.objects.get(user= user)
        return HttpResponse(f"This is the profile of {user_profile.first_name} {user_profile.last_name}")

    elif request.method == "POST":
        try:
            user = User.objects.get(username = user_name)
        except User.DoesNotExist:
            return Response({"Status":"User doesn't exist"})
        user_profile = UserProfile.objects.get(user=user)
        data = UserProfileSerializer(user_profile).data

        return Response(data)
        

@api_view(["GET","POST"])
def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            data = request.data
            """ 
            Expected data = {"author":"username", 
            "post-date-time":"YYYY-MM-DD HH:MM:SS", 
            "content":"Every thing you can imagine"}
            """
            data['author'] = User.objects.get(username=data['author']).pk
            data['post_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            serializer = PostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                post_obj = serializer.save()
                val_data = serializer.data
                val_data['status'] = "Sucess"
                return Response(val_data)
    else:
        return Response({"Status":"You are not logged in!"})



@api_view(["POST"])
def get_posts(request, user_name):
    serializer = json.Serializer()
    if request.method == "POST":
        try:
            author = User.objects.get(username=user_name)
            posts = Post.objects.filter(author=author)
        except User.DoesNotExist:
            return Response({"status":"This user doesn't exist!"})
        post_list = []
        for p in posts:
            data = PostSerializer(p).data
            author_user = User.objects.get(pk=data['author'])
            author_profile = UserProfile.objects.get(user=author_user)
            data['author'] = f"{author_profile.first_name}  {author_profile.last_name}"

            post_list.append(data)
        
        return Response(post_list)
   
        

@api_view(["POST"])
def delete_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post_id = request.data['post_id']

            try:
                post = Post.objects.get(pk=post_id)
                post.delete()
                return Response({"Status":"Post Deleted!"})
            except Post.DoesNotExist:
                return Response({"Status":"Post doesn't exist!"})
    else:
        return Response({"Status":"You are not logged in!"})

@api_view(['POST'])
def login_view(request):
    
    data = request.data
    username = data['username']
    password = data['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"Status":f"User {username} Succesfully logged In!"})
        
    else:
        return Response({"Status":"Login failed, wrong credentials."})

@api_view(["POST"])
def logout_view(request):
    logout(request)
    return redirect("index_url")


@api_view(['POST'])
def unfollow(request):
    
    if request.user.is_authenticated:
        data = request.data
        try:
            user = User.objects.get(username=request.user.username)
            followed_user = User.objects.get(username=data['followed'])
        except User.DoesNotExist:
            return Response({"Status":"User doesn't exist"})

        query = Following.objects.get(follower=user, followed=followed_user)
        query.delete()
        
        return Response({"Status": "Succesfully Unfollowed!"})
    else:
        return Response({"Status":"You are not logged in!"})

@api_view(['GET','POST'])
def home_feed(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = User.objects.get(username=request.user.username)
            following = [followed.followed for followed in Following.objects.filter(follower=user)]
            post_list = []
            for f in following:
                posts = Post.objects.filter(author=f)
                if posts:
                    for p in posts:
                        post = PostSerializer(p).data
                        author_user = User.objects.get(pk=post['author'])
                        post['author'] = author_user.username
                        post_list.append(post)
                else:
                    continue

            random.shuffle(post_list)
            return Response(post_list)
        elif request.method == "GET":
            return HttpResponse("comming soon")
