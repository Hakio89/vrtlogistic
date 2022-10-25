from django import forms
from .models import *

class XiaomiNewForm(forms.ModelForm):    
    class Meta:
        model = Xiaomi
        fields = ['delivery', 'reckoning', 'status', 'file']
        
    def __init__(self, *args, **kwargs):
        super(XiaomiNewForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})

class XiaomiDeliveryForm(forms.ModelForm):    
    class Meta:
        model = Xiaomi
        fields = ['delivery', 'reckoning', 'status']
        
    def __init__(self, *args, **kwargs):
        super(XiaomiDeliveryForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            
class XiaomiDeliveryFileForm(forms.ModelForm):    
    class Meta:
        model = Xiaomi
        fields = ['file']
        
    def __init__(self, *args, **kwargs):
        super(XiaomiDeliveryFileForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            
class XiaomiPartsForm(forms.ModelForm):    
    class Meta:
        model = XiaomiPartsCatalog
        fields = ['file']
        
    def __init__(self, *args, **kwargs):
        super(XiaomiPartsForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})

class XiaomiWaitingForm(forms.ModelForm):    
    class Meta:
        model = XiaomiWaitingParts
        fields = ['file']
        
    def __init__(self, *args, **kwargs):
        super(XiaomiWaitingForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            
class PmgpDeliveryForm(forms.ModelForm):
    class Meta:
        model = Xiaomi
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
        model = Xiaomi
        fields = ['zz_pmgh', 'lpr_pmgh', 'status_pmgh']
        labels = {'zz_pmgh':'Give the PMGH order:',
                  'lpr_pmgh':'Give the LPR for PMGH order:',
                  'status_pmgh':'Choose current Status:'}
        
    def __init__(self, *args, **kwargs):
        super(PmghDeliveryForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            
class XiaomiClaimForm(forms.ModelForm):
    class Meta:
        model = XiaomiClaimParts
        fields = ['claim_part', 'qty', 'status']
        labels = {'claim_part':'Give the PN of claim part:',
                  'qty':'Qy of claim part:',
                  'status':'Choose current status:'}
        
    def __init__(self, *args, **kwargs):
        super(XiaomiClaimForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})