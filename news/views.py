from django.views.generic import ListView, CreateView
from news.models import * 
from news.forms import * 
from django.shortcuts import render
from django.http import HttpResponseRedirect

class NewsListView(ListView):
    model = News
    queryset = News.get_news.all()
    paginate_by = 15 

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted = Vote.objects.filter(voter=self.request.user)
            news_in_page = [news.id for news in context['object_list']]
            voted = voted.filter(news_id__in=news_in_page)
            voted = voted.values_list('news_id', flat=True)
            context['voted'] = voted
        context['request'] = self.request
        return context


class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.point = 0.0 
        f.submitter = self.request.user
        f.save()
        f.set_point()
        return super(NewsCreateView, self).form_valid(form)


def vote(request):
    if request.method == 'POST':
        redirect = request.POST['next']
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/?next=' + redirect)

        form = VoteForm(request.POST)
        if form.is_valid():
            news = News.objects.get(id=form.data['news'])
            user = request.user 
            prev_vote = Vote.objects.filter(voter=user, news=news)

            if not (prev_vote.count() > 0):
                Vote.objects.create(voter=user, news=news)
            else:
                prev_vote[0].delete()

            news.set_point()
            return HttpResponseRedirect(redirect) 
    
    return HttpResponseRedirect('/news/') 


def comment(request, id):
    try:
        news = News.objects.get(id=int(id))
        return render(request, 'news/comment.html', locals()) 
    except:
       return render(request, '404.html')

