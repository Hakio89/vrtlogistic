from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def user_login(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.get(username=username)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        
    return render(request, "users/login.html")

def user_logout(request):
    logout(request)
    return redirect('user_login')

def user_registration(request):
    registered = False
    
    if request.method=="POST":
        
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.owner = user
            
            if 'profile_image' in request.FILES:
                
                profile.profile_image = request.FILES['profile_image']
            
            profile.save()
            
            registered = True
            
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm
    
    
            
        print("Wysłano formularz")
    
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
        profile_image_form = UserProfileImageUpdateForm(request.POST, request.FILES, instance=user_profile)
        profile_update_form = UserProfileUpdateForm(request.POST, instance=user_profile)
        
        if "image_update" in request.POST:
            user_profile.profile_image.delete()
            if profile_image_form.is_valid():
                profile_image_form.save()
                return redirect('user_profile', pk )
            
        if "data_update" in request.POST:
            if profile_update_form.is_valid():
                profile_update_form.save()            
                return redirect('user_profile', pk )
    ctx = {
        "user" : user,
        "profile_update_form" : profile_update_form,
        "profile_image_form" : profile_image_form,
    }
    return render(request, "users/profile.html", ctx)