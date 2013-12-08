from django.http import HttpResponse, Http404
from django.template.loader import get_template, Context
from django.template import RequestContext
from rank.models import *
from django.shortcuts import render, render_to_response
import numpy as np
from django.db.models import Q


delta = 0.0001
beta = 0.60
default_game = '3'

def rank(request):
    if 'q' in request.GET:
        q = request.GET['q']
    else:
        q = default_game

    errors = check(q)
    if not errors:
        # render result page
        game_num = int(q)
        items = get_items(game_num)
        games = get_games(items[0][1], game_num)
        team = items[0][1] 
        return render(request, 'rank/rank.html', locals())

    # render error page
    items = []
    game_num = 0
    return render(request, 'rank/rank.html', locals())


def games(request):
    q = request.GET['q']
    t = request.GET['t']

    game_num = int(q)
    team_id = int(t)
    team = Team.objects.get(id=team_id)
    games = get_games(team, game_num)
    
    tmpl = get_template('rank/games.html') 
    ctx = Context({'games': games, 'team': team})

    return HttpResponse(tmpl.render(ctx))


def check(q):
    errors = []
    if not q:
            errors.append('Please enter a number.')
    elif not q.isdigit():
            errors.append('Please enter a valid number.')
    elif int(q) < 1:
            errors.append('Please enter a positive number.')
    else: 
        teams = get_teams()
        for t in teams:
            games = list(Game.objects.filter(Q(home=t) | Q(guest=t)))
            if len(games) < int(q):
                errors.append('No enough games, Please enter a smaller number.')
                break
            
    return errors

 
def get_items(game_num):
    teams = get_teams()
    (teamRank, teamWin, teamHome) = get_rank(game_num)
    
    # sort items according to teamRank 
    items = list(zip(teamRank, teamWin, teamHome, range(len(teams)), teams))
    items.sort()
    items.reverse()

    # create the tuple as (rank, team, win, lost, home, guest, teamRank)
    rank = 1
    prev_rank = items[0][0]
    items[0] = (rank, items[0][4], items[0][1], game_num - items[0][1], items[0][2], game_num - items[0][2], '%.3f'%items[0][0])
    for i in range(1, len(items)):
        if items[i][0] != prev_rank:
            rank += 1     
        prev_rank = items[i][0]
        items[i] = (rank, items[i][4], items[i][1], game_num - items[i][1], items[i][2], game_num - items[i][2], '%.3f'%items[i][0])
    
    return items        


def get_games(team, num):
    games = list(Game.objects.filter(Q(home=team) | Q(guest=team)))[:num]
    return games


def get_teams():
    team_list = Team.objects.all()
    return team_list


def get_rank(game_num):
    teams = get_teams()
    team_num = len(teams)
    teamRank = []
    teamWin = []
    teamHome = []

    # create transition matrix
    M1 = np.zeros((team_num, team_num))
    V1 = np.zeros((team_num, 1))
    M2 = np.zeros((team_num, team_num))
    V2 = np.zeros((team_num, 1))
    
    for i in range(team_num):
        games = list(Game.objects.filter(Q(home=teams[i]) | Q(guest=teams[i])))[:game_num]

        for j in range(game_num):
            # create a arc from the loser to the winner 
            if find_winner(games[j]) == teams[i]:
                loser_index = find_index(teams, find_loser(games[j]))
                M1[i][loser_index] += 1
            # create a arc from the winner to the loser
            else:
                winner_index = find_index(teams, find_winner(games[j]))
                M2[i][winner_index] += 1

        # keep track of the number of wins and home
        teamWin.append(int(sum(M1[i, :])))
        home = [g for g in games if g.home == teams[i]]
        teamHome.append(len(home))

    # normalize
    V1[:, 0] = 1/team_num
    V2[:, 0] = 1/team_num

    for k in range(team_num):
        normalize1 = sum(M1[:, k])
        normalize2 = sum(M2[:, k])
        if normalize1 != 0:
            M1[:, k] /= normalize1
        if normalize2 !=0:
            M2[:, k] /= normalize2

    M1 = np.matrix(M1)
    V1 = np.matrix(V1)
    M2 = np.matrix(M2)
    V2 = np.matrix(V2)

    e = np.copy(V1) * beta 

    # mutiply until converge
    W1 = ((1-beta) * M1) * V1 + e
    W2 = ((1-beta) * M2) * V2 + e

    while not equal(V1, W1):
        V1 = W1
        W1 = ((1-beta) * M1) * V1 + e

    while not equal(V2, W2):
        V2 = W2
        W2 = ((1-beta) * M2) * V2 + e

    # return rank score 
    for i in range(team_num):
        teamRank.append(W1[i, 0] - W2[i, 0])

    return (teamRank, teamWin, teamHome)


def find_winner(game):
    if game.home_score > game.guest_score:
        return game.home
    return game.guest


def find_loser(game):
    if game.home_score < game.guest_score:
        return game.home
    return game.guest

    
def equal(X, Y):
    for i in range(len(X)):
        if abs(X[i] - Y[i]) > delta:
            return False
    return True


def find_index(teams, team):    
    for i, t in enumerate(teams):
        if t == team:
            return i
    return -1

