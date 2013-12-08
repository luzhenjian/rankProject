from django.http import HttpResponse, Http404
from django.template.loader import get_template, Context
from django.template import RequestContext
from forum.models import *
from django.shortcuts import render, render_to_response
from django.db.models import Q


def forum(request):
    '''
    print('this is forum')
    topics = Topic.objects.all()
    return render(request, 'forum.html', {'topics': topics})
    '''
    return render(request, 'building_msg.html', {'request':request})

def topic(request, id):
    print('this is topic')
    print(id)
    topic = Topic.objects.get(id=int(id))
    threads= Thread.objects.filter(topic=topic)
    return render(request, 'topic.html', {'threads': threads}, {'request':request})

def thread(request, id):
    print('this is thread')
    print(id)
    thread = Thread.objects.get(id=int(id))
    posts= Post.objects.filter(thread=thread)
    print(posts)
    return render(request, 'thread.html', {'posts': posts}, {'request':request})

def new_thread(request, topic_id):
    pass

def new_post(request, thread_id):
    pass
    
def twitter(request):
    return render(request, 'building_msg.html', {'request':request})

 
def about(request):
    return render(request, 'about.html', {'request':request})


