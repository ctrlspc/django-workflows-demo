# Create your views here.
from django.http import  HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from tokens.forms import TokenForm
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from permissions.models import Role
from permissions.utils import add_local_role, has_permission

from workflows.models import Workflow, State
from workflows.utils import set_workflow, set_state, do_transition
from tokens.models import Token
from django.core.exceptions import PermissionDenied

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
    
    token_generator_role = Role.objects.get(name='Token_Generator')
    supervisor_role = Role.objects.get(name='Supervisor')
    
    #get the tokens that I am the researcher for
    my_tokens = [roleRelation.content for roleRelation in user.principalrolerelation_set.filter(role=token_generator_role) ]
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
            token_generator_role = Role.objects.get(name='Token_Generator')
            supervisor_role = Role.objects.get(name='Supervisor')
            
            #get the approval workflow
            approval_workflow = Workflow.objects.get(name='Token_Approval')
            
            #add the user and their supervisor as local roles for this token
            add_local_role(token, user, token_generator_role)
            add_local_role(token, supervisor, supervisor_role)
            
            
            set_workflow(token, approval_workflow)
            
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
def evaluate(request, token, approved):
    '''
        This will allow you to decide if a token is approved or diapproved.
        You must have evaluate permission for this token otherwise you will get a nasty 403 Fobidden error.
        
        
    '''
    
    #get or 404 the token
    token_object = get_object_or_404(Token,pk=token)
    
    #check that the user has got the submit permission for the token
    

        
    if approved:
        transition_allowed = do_transition(token_object, 'approved', request.user)
    else:
        transition_allowed = do_transition(token_object, 'rejected', request.user)
    
    
    if not transition_allowed:
        raise PermissionDenied()
        
        
   
    return HttpResponseRedirect(reverse('home_view'))

@login_required
def submit(request, token):
    '''
        This will submit a given token for approval
        In order to do this, you must have the submit permission for the token otherwise you will get a nasty 403 Fobidden error.
    
    '''
    #get or 404 the token
    token_object = get_object_or_404(Token,pk=token)
    
    
    #attempt the token_submission transition, if not allowed raise permissiondenied!
    if not do_transition(token_object, 'token_submission', request.user):
        raise PermissionDenied()
    
    #set the object state to awaiting_approval
    
    return HttpResponseRedirect(reverse('home_view'))