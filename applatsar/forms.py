from django.forms import ModelForm
from .models import DatabaseTamu
from django import forms

class FormTamu(ModelForm):
    class Meta:
        model = DatabaseTamu
        exclude = ['tanggal']
        
        widgets = {
            'nama' : forms.TextInput(attrs={'class': 'form-control', 'color':'white'}),
            'instansi' : forms.TextInput(attrs={'class': 'form-control'}),
            'agenda' : forms.TextInput(attrs={'class': 'form-control'}),
        }