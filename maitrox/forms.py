from django import forms
from .models import *

class NewDeliveryForm(forms.ModelForm):    
    class Meta:
        model = Maitrox
        fields = ['delivery', 'reckoning', 'business', 'status', 'file']
        
    def __init__(self, *args, **kwargs):
        super(NewDeliveryForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})

class DeliveryForm(forms.ModelForm):    
    class Meta:
        model = Maitrox
        fields = ['delivery', 'reckoning', 'business', 'status']
        
    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            
class DeliveryFileForm(forms.ModelForm):    
    class Meta:
        model = Maitrox
        fields = ['file']
        
    def __init__(self, *args, **kwargs):
        super(DeliveryFileForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            
class PartsForm(forms.ModelForm):    
    class Meta:
        model = PartsCatalog
        fields = ['file']
        
    def __init__(self, *args, **kwargs):
        super(PartsForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})

class WaitingForm(forms.ModelForm):    
    class Meta:
        model = WaitingParts
        fields = ['file']
        
    def __init__(self, *args, **kwargs):
        super(WaitingForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
              
class ClaimForm(forms.ModelForm):
    class Meta:
        model = ClaimParts
        fields = ['claim_part', 'qty', 'status']
        labels = {'claim_part':'Give the PN of claim part:',
                  'qty':'Qy of claim part:',
                  'status':'Choose current status:'}
        
    def __init__(self, *args, **kwargs):
        super(ClaimForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})