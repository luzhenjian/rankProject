from django.db import models
import datetime
from django.db.models import Q, F


class Team(models.Model):
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    conference = models.CharField(max_length=2)
    website = models.URLField()

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return self.name

    def win_lost(self):
        total = Game.objects.filter(Q(home=self) | Q(guest=self))
        home_win = total.filter(Q(home=self), Q(home_score__gt=F('guest_score')))
        guest_win = total.filter(Q(guest=self), Q(home_score__lt=F('guest_score')))
        total_count = len(total)
        win_count = len(home_win) + len(guest_win)
        lost_count = total_count - win_count

        return (win_count, lost_count) 
        


class Game(models.Model):
    guest = models.ForeignKey(Team, related_name='game_guest')
    home = models.ForeignKey(Team, related_name='game_home')
    guest_score = models.IntegerField()
    home_score = models.IntegerField()
    date = models.DateField()
    ot = models.IntegerField()

    class Meta:
        unique_together = (('home', 'date'), ('guest', 'date'),)

    def __str__(self):
        return self.guest.name + ' - ' + self.home.name + ' ' + self.date.strftime('%m/%d/%y')

    class Meta:
        ordering = ['-date']
