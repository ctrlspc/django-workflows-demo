# Create your views here.
from django.http import  HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from tokens.forms import TokenForm
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

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
    
    
    
    return HttpResponse('HOME')

@login_required
def create(request):
    '''
        Create a new token, for which the logged in user will be the owner
    '''
    
    if request.method == "POST":
        form = TokenForm(request.POST)
        
        if form.is_valid():
            form.save()
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