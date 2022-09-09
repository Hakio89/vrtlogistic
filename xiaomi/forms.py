from django import forms
from .models import Xiaomi

class XiaomiAdd(forms.ModelForm):
    
    class Meta:
        model = Xiaomi
        fields = ('delivery', 'status', 'file')
        
    def __init__(self, *args, **kwargs):
        super(XiaomiAdd, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})