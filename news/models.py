from django.db import models
from django.db.models import Count
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta 
from math import log
from django.contrib.auth.models import User
from tldextract import extract

class NewsVoteCountManager(models.Manager):
    def get_query_set(self):
        return super(NewsVoteCountManager, self).get_query_set().order_by('-point','-time')

class News(models.Model):
    title = models.CharField(max_length=100)
    submitter = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    point = models.FloatField(default=0.0)
    url = models.URLField(max_length=100, blank=True)
    
    get_news = NewsVoteCountManager() 
    objects = models.Manager()

    def get_absolute_url(slef):
        return reverse('news')

    def __str__(self):
        return self.title

    def vote_count(self):
        votes = Vote.objects.filter(news=self)
        return votes.count()

    def comhead(self):
        url_str = str(self.url)
        result = extract(url_str)
        return (result[1]+'.'+result[2]).lower()

    def set_point(self):
        epoch = datetime.strptime('1/15/2013 0:00:00 AM', '%m/%d/%Y %H:%M:%S %p')
        delta = self.time.replace(tzinfo=None) - epoch
        seconds = delta.total_seconds()

        score = self.vote_count() 
        #print(score)
        order = log(max(abs(score), 1), 10)
        
        self.point = round(order + seconds / 45000, 7)
        #print (self.point)
        self.save()

        

class Vote(models.Model):
    voter = models.ForeignKey(User)
    news = models.ForeignKey(News)
    
    def __str__(self):
        return '%s voted %s' % (self.voter, self.news)
