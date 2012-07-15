'''
Created on Jul 15, 2012

@author: jasonmarshall
'''
from django import forms
from models import Token

class TokenForm(forms.ModelForm):
    
    class Meta:
        model = Token
        exclude = ('approved')  