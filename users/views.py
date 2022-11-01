from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def user_login(request):
    
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = User.objects.get(username=username)
            except:
                messages.warning(request, 'Login is incorrect')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'successfully logged in')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Password is incorrect')
            
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
        
        
    return render(request, "users/login.html")

def user_logout(request):
    try:
        logout(request)
        messages.success(request, 'successfully logged out')
        
    except:
            messages.warning(request, 'Something went wrong. Please contact admin')
            
    return redirect('user_login')

def user_registration(request):
    registered = False
    
    if request.method=="POST":
        try:
            user_form = UserForm(data=request.POST)
            profile_form = UserProfileForm(data=request.POST)
            
            if user_form.is_valid() and profile_form.is_valid():
                
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                messages.success(request, 'successfully registered')
                
                profile = profile_form.save(commit=False)
                profile.owner = user
                
                if 'profile_image' in request.FILES:
                    
                    profile.profile_image = request.FILES['profile_image']
                
                profile.save()
                registered = True    
                
            else:
                print(user_form.errors, profile_form.errors)
                
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm
    
    ctx = {"user_form" : user_form,
           "profile_form" : profile_form,
           "registered" : registered,
           }
    return render(request, "users/registration.html", ctx)

@login_required
def user_profile(request, pk):
    user = User.objects.get(username=pk)
    user_profile = Profile.objects.get(owner=user)
    profile_update_form = UserProfileUpdateForm(instance=user_profile)
    profile_image_form = UserProfileImageUpdateForm(instance=user_profile)
    
    if request.method == "POST":
        try:
            profile_image_form = UserProfileImageUpdateForm(request.POST, request.FILES, instance=user_profile)
            profile_update_form = UserProfileUpdateForm(request.POST, instance=user_profile)
            
            if "image_update" in request.POST:
                user_profile.profile_image.delete()
                if profile_image_form.is_valid():
                    profile_image_form.save()
                    messages.success(request, 'image successfully updated')
                    return redirect('user_profile', pk )
                
            if "data_update" in request.POST:
                if profile_update_form.is_valid():
                    profile_update_form.save()     
                    messages.success(request, 'successfully updated')       
                    return redirect('user_profile', pk )
                
        except:
            messages.warning(request, 'Something went wrong. Please contact admin')
        
    ctx = {
        "user" : user,
        "profile_update_form" : profile_update_form,
        "profile_image_form" : profile_image_form,
    }
    return render(request, "users/profile.html", ctx)