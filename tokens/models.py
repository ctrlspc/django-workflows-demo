from django.db import models

# Create your models here.


class Token(models.Model):
    
    name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s, approved?:%s" % (self.name,self.approved )