from django import forms
from .models import *

class NewForm(forms.ModelForm):    
    class Meta:
        model = Maitrox
        fields = ['delivery', 'reckoning', 'status', 'file']
        
    def __init__(self, *args, **kwargs):
        super(NewForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})

class DeliveryForm(forms.ModelForm):    
    class Meta:
        model = Maitrox
        fields = ['delivery', 'reckoning', 'status', 'status_pmgp', 'status_pmgh']
        
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
            
class PmgpDeliveryForm(forms.ModelForm):
    class Meta:
        model = Maitrox
        fields = ['zz_pmgp', 'lpr_pmgp', 'status_pmgp']
        labels = {'zz_pmgp':'Give the PMGP order:',
                  'lpr_pmgp':'Give the LPR for PMGP order:',
                  'status_pmgp':'Choose current Status:'}
        
    def __init__(self, *args, **kwargs):
        super(PmgpDeliveryForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            
class PmghDeliveryForm(forms.ModelForm):
    class Meta:
        model = Maitrox
        fields = ['zz_pmgh', 'lpr_pmgh', 'status_pmgh']
        labels = {'zz_pmgh':'Give the PMGH order:',
                  'lpr_pmgh':'Give the LPR for PMGH order:',
                  'status_pmgh':'Choose current Status:'}
        
    def __init__(self, *args, **kwargs):
        super(PmghDeliveryForm, self).__init__(*args, **kwargs)
        
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