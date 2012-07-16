'''
Created on Jul 15, 2012

@author: jasonmarshall
'''
from django.contrib import admin
 
from models import Token, SupervisorRelationship

    
    

admin.site.register(Token)
admin.site.register(SupervisorRelationship)