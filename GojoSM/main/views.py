from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from main.serializers import UserSerializer, UserProfileSerializer, FollowingSerializer
from django.contrib.auth.models import User
from .models import UserProfile
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
    serializer = FollowingSerializer(data=data)

    if serializer.is_valid(raise_exception=True):
        fol_obj = serializer.save()
        rspdata = serializer.data
        rspdata['Status'] = "OK"
        return Response(rspdata)
    else:
        return Response({"Status" : "Failed"})

@api_view(['POST'])
def delete_account(request):
    data = request.data

    username = data['username']
    try:
        user = User.objects.get(username=username)
        user.delete()
        Response({"Status": "User has been deleted!"})
    except User.DoesNotExist:
        Response({"Status":"The Specified User doesn't exist!"})
    except Exception as c:
        print(c)

@api_view(['GET','POST'])
def edit_profile(request):
    if request.method == "GET":
        Response({"Status": "Not there Yet!"})

    elif request.method == "POST":
        data = request.data
        username = data['user']
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


