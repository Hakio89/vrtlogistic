from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("username", "email", "password")
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
        
class UserProfileForm(forms.ModelForm):   
     
    class Meta:
        model = Profile
        fields = ["workplace", "occupation", "supervisor", "profile_image"]
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            
class UserProfileUpdateForm(forms.ModelForm):   
     
    class Meta:
        model = Profile
        fields = ["workplace", "occupation", "supervisor"]
        
    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            
class UserProfileImageUpdateForm(forms.ModelForm):
     
    class Meta:
        model = Profile
        fields = ["profile_image"]
        
    def __init__(self, *args, **kwargs):
        super(UserProfileImageUpdateForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})