from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import RentCar


class RentCarForm(forms.ModelForm):
    class Meta:
        model = RentCar
        fields = ['full_name', 'phone', 'email', 'start_date', 'end_date', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'To\'liq ismingizni kiriting'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Qo\'shimcha xabar (ixtiyoriy)'
            }),
        }
        labels = {
            'full_name': 'To\'liq ism',
            'phone': 'Telefon raqami',
            'email': 'Email',
            'start_date': 'Boshlanish sanasi',
            'end_date': 'Tugash sanasi',
            'message': 'Qo\'shimcha xabar',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date < date.today():
                raise ValidationError('Boshlanish sanasi bugungi kundan oldin bo\'lishi mumkin emas!')
            if end_date < start_date:
                raise ValidationError('Tugash sanasi boshlanish sanasidan oldin bo\'lishi mumkin emas!')
        
        return cleaned_data
