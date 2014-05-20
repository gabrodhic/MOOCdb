from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from foundary.models import IdeaForm,Idea,Code,CodeForm,Comment
from secretballot.views import vote
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
import json
from django.views.generic import View
from django.template import Template,Context
from tasks import run_script

#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
def home(request):
    frm_error=False
    if request.method=='POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            formVal=form.save()
            return HttpResponseRedirect(reverse('home'))
        else:            
            frm_error=True
    else:
        form = IdeaForm()   
    ideas=Idea.objects.order_by('-total_upvotes')
    return render(request,'home.html',{'form':form,'ideas':ideas,'form_error':frm_error})

def likeit(request):
    pk=request.GET['pk']
    content_type=ContentType.objects.get(app_label='foundary', model__iexact='Idea')
    return vote(request,content_type=content_type,object_id=pk,vote='+1',)

class CodeView(View):
    form_class = CodeForm
    #initial = {'code': 'simple test'}
    def create_template(self,pk):
        form = self.form_class()
        codes=Code.objects.filter(idea__id=pk, user_final=True, is_correct=True)
        str_codes="""    
        {% if codes %}    
        <div class="panel-body" style="background-color:#FAEBD7;">            
            {% for cd in codes %}
                <div class="items-body clearfix">
                    <strong>Author:</strong> {{cd.name}}
                    <small class="pull-right text-muted">
                        <span class="glyphicon glyphicon-time"></span> {{cd.sub_time}}
                    </small>  
                    <pre>{{cd.code}}{% if cd.explanation %}<br style="margin:0;padding:0" /> <small class="text-muted">{{ cd.explanation }}</small>{% endif %}</pre>
                </div>
            {% endfor %}
        </div>
        {% endif %}
        <div class="panel-footer">
            <form role="form">
            <h4> Submit a new code to extract this feature. </h4>

            <div class="row">
                <div class="col-md-6">{{form.name}}</div>
                <div class="col-md-6">{{form.email}}</div>
            </div>            
            </br>
            {{ form.code }} 
            </br>
            <input type="hidden" class="ideapk-hidden" name="idea" value="{{ideapk}}" />
            {% if codes %}{{ form.explanation }}{% endif %}
            {# form.user_final #}
            </br>
            <input type="radio" name="user_final" checked="checked" value="False"/> <label> (Deubg) Check for errors but don't publish online yet. </label>
            </br>
            <input type="radio" name="user_final" value="True"/> <label> Publish online if there are no errors.</label>             
            <button class="btn btn-success btn-xs pull-right btn-savecode" type="button">Save Code</button>
            </form>                                   
        </div>
        """
        c = {'form': form,'codes':codes,'ideapk':pk}
        return Template(str_codes).render(Context(c))
    def get(self, request, *args, **kwargs):        
        return HttpResponse(self.create_template(request.GET['ipk']))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            lastcode=form.save()            
            run_script.delay(lastcode.pk)
            return HttpResponse(self.create_template(lastcode.idea.pk))
        return HttpResponse('1')

class CommentView(View):
    def create_template(self,pk):
        comments=Comment.objects.filter(idea__id=pk)
        str_comments="""    
        {% if comments %}    
        <div class="panel-body">    
   
            {% for cd in comments %}
                <div class="items-body clearfix">     
                    <small class="pull-right text-muted">
                            <span class="glyphicon glyphicon-time"></span> {{cd.sub_time}}
                    </small>                   
                    <div class="bs-callout bs-callout-warning">{{cd.text}}</div>                    
                </div>
                <br>
            {% endfor %}
        </div>
        {% endif %}
        <div class="panel-footer">Add New Comment:  
        <form role="form">
            <input type="hidden" class="ideapk-hidden" name="idea" value="{{ideapk}}" />          
            <textarea class="form-control input-sm" name="text" rows="3"></textarea>
            <br>
            <button class="btn btn-success btn-xs pull-right btn-addcomment" type="button">add comment</button>
        </form>
        </div>
        """
        c = {'comments':comments,'ideapk':pk}
        return Template(str_comments).render(Context(c))

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.create_template(request.GET['ipk']))

    def post(self, request, *args, **kwargs):        
        if len(request.POST['text']) < 15:return HttpResponse('1')
        comt=Comment(text=request.POST['text'],ip=request.META['REMOTE_ADDR'])
        comt.idea=Idea.objects.get(pk=request.POST['idea'])
        comt.save()        
        return HttpResponse(self.create_template(comt.idea.pk))

        