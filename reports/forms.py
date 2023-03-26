from django import forms

class CCSReportsForm(forms.Form):
    REPORT_CHOICE = [
    ('NC', 'Naprawy Czekające'),
    ('DCC', 'Dostępne części pod czeka'),
    ('PNDZ', 'Potencjalne naprawy do zwolnienia'),
    ('DX', 'Dostawy Xiaomi'),
]
    report = forms.ChoiceField(choices=REPORT_CHOICE, label='Wybierz raport:')

