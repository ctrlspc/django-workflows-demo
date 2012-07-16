from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Token(models.Model):
    
    name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s, approved?:%s" % (self.name,self.approved )
    
    
class SupervisorRelationship(models.Model):
    
    supervisor = models.ForeignKey(User, related_name='supervisor')
    supervisee = models.ForeignKey(User, related_name='supervisee')
    
    def __unicode__(self):
        
        return "%s is the supervisor of %s" % (self.supervisor.username, self.supervisee.username)