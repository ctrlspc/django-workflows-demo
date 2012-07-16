# Create your views here.
from django.http import  HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from tokens.forms import TokenForm
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from permissions.models import Role
from permissions.utils import grant_permission, add_local_role

@login_required
def home(request):
    '''
        Shows all the tokens that this person has view access too, and gives them other
        options depending upon the permissions they have for the object.
        
        These are:
        
        edit 
        delete
        evaluate (approve/disapprove)
    '''
    
    user = request.user
    
    researcher_role = Role.objects.get(name='Researcher')
    supervisor_role = Role.objects.get(name='Supervisor')
    
    #get the tokens that I am the researcher for
    my_tokens = [roleRelation.content for roleRelation in user.principalrolerelation_set.filter(role=researcher_role) ]
    supervisee_tokens = [roleRelation.content for roleRelation in user.principalrolerelation_set.filter(role=supervisor_role) ]
    
    
    return render_to_response("token_home.html", {'my_tokens':my_tokens, 'supervisee_tokens':supervisee_tokens}, context_instance=RequestContext(request) )

@login_required
def create(request):
    '''
        Create a new token, for which the logged in user will be the owner
    '''
    
    if request.method == "POST":
        form = TokenForm(request.POST)
        
        if form.is_valid():
            
            token = form.save()
            

            #get the user and supervisor
            user = request.user
            supervisor = user.supervisee.all()[0].supervisor
            #get the researcher and supervisor  roles
            researcher_role = Role.objects.get(name='Researcher')
            supervisor_role = Role.objects.get(name='Supervisor')
            
            #researcher permissions
            grant_permission(token, researcher_role, 'owner')
            grant_permission(token, researcher_role, 'edit')
            grant_permission(token, researcher_role, 'view')
            grant_permission(token, researcher_role, 'submit')
            
            #supervisor permissions
            grant_permission(token, supervisor_role, 'view')
            
            #add the user and their supervisor as local roles for this token
            add_local_role(token, user, researcher_role)
            add_local_role(token, supervisor, supervisor_role)
            
            
            # redirect to home
            return HttpResponseRedirect(reverse('home_view'))
            
    else:
        form = TokenForm()
        
    return render_to_response("create_token.html", {
                                                        "form": form,
                                                    }, context_instance=RequestContext(request) )

@login_required
def edit(request, token):
    
    '''
        Edit the details of a token.
        You must have edit permission for this object to be able to do this
        otherwise you will get a nasty 403 Fobidden error!
    '''
    return HttpResponse('edit')


@login_required
def delete(request, token):
    
    '''
        Delete a token.
        You must have delete permission for this object to be able to do this
        otherwise you will get a nasty 403 Fobidden error!
    '''
    return HttpResponse('delete')

@login_required
def evaluate(request, token):
    '''
        This will allow you to decide if a token is approved or diapproved.
        You must have evaluate permission for this token otherwise you will get a nasty 403 Fobidden error.
    '''
    return HttpResponse('evaluate')