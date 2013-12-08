from django import forms
from news.models import *


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ('submitter', 'point') 
        
class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
