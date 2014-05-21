from django.db import models
from django.forms import ModelForm,ValidationError
from django.contrib import admin
import secretballot

class Idea(models.Model):
    name = models.CharField(max_length=50)
    email=models.EmailField() 
    idea = models.TextField()
    def total_comments(self):
        return Comment.objects.filter(idea__id=self.pk).count()
    def has_code(self):
        return True if Code.objects.filter(idea__id=self.pk,user_final=True,is_correct=True) else False


class Code(models.Model):
    idea=models.ForeignKey(Idea)
    code = models.TextField()
    name=models.CharField(max_length=50)
    email=models.EmailField() 
    user_final=models.BooleanField(default=False)
    explanation= models.TextField(blank=True)
    sub_time=models.DateTimeField(auto_now_add=True)
    sub_result=models.TextField(blank=True, null=True)
    is_correct=models.IntegerField(blank=True, null=True)
    elapsed=models.IntegerField(blank=True, null=True)

class Comment(models.Model):
    idea=models.ForeignKey(Idea)
    text=models.TextField()
    sub_time=models.DateTimeField(auto_now_add=True)
    ip=models.CharField(max_length=50)

class IdeaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        extra={'name':'Name','email':'E-mail','idea':'Enter New Idea... '}
        for key,value in extra.iteritems():
            self.fields[key].widget.attrs['class'] = 'form-control input-sm'
            self.fields[key].widget.attrs['placeholder'] = value
        self.fields['idea'].widget.attrs['rows'] = "2"

    class Meta:
        model = Idea
    def clean_idea(self):
        data = self.cleaned_data['idea']
        if len(data) < 20:
            raise ValidationError("Description must have atleast 20 characters.")        
        return data

class CodeForm(ModelForm):	
    def __init__(self, *args, **kwargs):
        super(CodeForm, self).__init__(*args, **kwargs)
        extra={'name':'Name','email':'E-mail',
            'code':'Submit a New code... ','explanation':'why are you submitting a new code?'}
        for key,value in extra.iteritems():
            self.fields[key].widget.attrs['class'] = 'form-control input-sm'
            self.fields[key].widget.attrs['placeholder'] = value
        self.fields['code'].widget.attrs['rows'] = "2"
        self.fields['explanation'].widget.attrs['rows'] = "2"     
    class Meta:
        model = Code

secretballot.enable_voting_on(Idea)
admin.site.register(Idea)
admin.site.register(Comment)
admin.site.register(Code)
