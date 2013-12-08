from django.db import models

# Create your models here.


class Topic(models.Model):
    title = models.CharField(max_length=50)

    def num_threads(self):
        return Thread.objects.filter(topic=self).count()

    def last_thread(self):
        threads = Thread.objects.filter(topic=self)

        if threads:
            return threads[0].title 
        else:
            return 'no threas'

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic)
    author = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True) 
    
    def num_posts(self): 
        return Post.objects.filter(thread=self).count()

    def last_post(self):
        posts = Post.objects.filter(thread=self)
        return posts[len(posts) - 1].title 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time']

class Post(models.Model):
    title = models.CharField(max_length=100)
    thread = models.ForeignKey(Thread)
    author = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True) 
    message = models.TextField(max_length=5000)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['time']



