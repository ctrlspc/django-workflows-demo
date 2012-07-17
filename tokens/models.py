from django.db import models
from django.contrib.auth.models import User

from workflows.utils import get_state
from permissions.models import  Role, PrincipalRoleRelation
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class Token(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return "%s, current state:%s" % (self.name, self.get_current_state())
    
    def get_current_state(self):
        return get_state(self)
    
    def get_token_generators(self):
        token_generator_role = Role.objects.get(name='Token_Generator')
        return [roleRelation.user for roleRelation in self._get_role_relations_for_me().filter(role=token_generator_role) ]
    
    def get_token_supervisor(self):
        
        supervisor_role = Role.objects.get(name='Supervisor')
        return [roleRelation.user for roleRelation in self._get_role_relations_for_me().filter(role=supervisor_role) ]
    
    def _get_role_relations_for_me(self):
        ctype = ContentType.objects.get_for_model(self)
        return PrincipalRoleRelation.objects.filter(content_type=ctype).filter(content_id=self.id)
    
    
class SupervisorRelationship(models.Model):
    
    supervisor = models.ForeignKey(User, related_name='supervisor')
    supervisee = models.ForeignKey(User, related_name='supervisee')
    
    def __unicode__(self):
        
        return "%s is the supervisor of %s" % (self.supervisor.username, self.supervisee.username)