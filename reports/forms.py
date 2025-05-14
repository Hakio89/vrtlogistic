from django import forms

class CCSReportsForm(forms.Form):
    SELECT_BUSINESS = [
    ('ALCATEL', 'ALCATEL'),
    ('CAT', 'CAT'),
    ('HUAWEI', 'HUAWEI'),
    ('NEOLINE', 'NEOLINE'),
    ('NOTHING', 'NOTHING'),
    ('SAMSUNG', 'SAMSUNG'),
    ('SETTI', 'SETTI'),
    ('TCL', 'TCL'),
    ('QLIVE', 'QLIVE'),
    ('VIVO', 'VIVO'),
    ('XIAOMI', 'XIAOMI'),
    ('MOTOROLA', 'MOTOROLA'),
    ('SEGWAY', 'SEGWAY'),
    ('BOTTARI', 'BOTTARI'),
    ]
    

    select_business = forms.MultipleChoiceField(
        choices=SELECT_BUSINESS, 
        widget=forms.CheckboxSelectMultiple(), 
        label='Wybierz biznes:',
    )


