from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..logreg.models import User, Pokemon
from .models import Match
from django.contrib import messages
# Create your views here.
def index(request):
    if 'user_id' not in request.session or request.session['user_id'] == -1:
        print "Nuh-uh. You can't see this page yet."
        request.session['user_id'] = -1
        messages.warning(request, 'Please sign-in or register.')
        return redirect('/prof')
    else:
        user = User.objects.get(id=request.session["user_id"])
        return render(request, 'teambuilder/index.html', {"user":user})

def stat_ajax(request):
    if request.method != 'POST':
        return JsonResponse({"success": False, "errors":["Please use the form to calculate Pokemon data."]})
    else:
        if Pokemon.objects.validation(request.POST, request.session["user_id"])[0]:
            new_stat = Pokemon.objects.stat_calc(request.POST)
            if "save" in request.POST:
                print "Attempting to save"
                try:
                    user = User.objects.get(id=request.session["user_id"])
                except User.DoesNotExist:
                    errors.append("An error has occurred. Please log out and log in again.")
                    return JsonResponse({"success":False, "errors":errors})
                if Pokemon.objects.validation(request.POST, request.session["user_id"]):
                    pokemon = Pokemon.objects.create(pokeid=request.POST['id'], hp=new_stat[0], atk=new_stat[1], defense=new_stat[2], spatk=new_stat[3], spdef=new_stat[4], speed=new_stat[5], nature=request.POST['nature'], trainer=user)
            return JsonResponse({"success":True, "pokemon":new_stat})
        else:
            return JsonResponse({"success":False, "errors":Pokemon.objects.validation(request.POST, request.session["user_id"])[1]})

def battle(request):
    try:
        user = User.objects.get(id=request.session['user_id'])
    except:
        return redirect('/')
    context = {
        'user': user,
        'allmatches': Match.objects.order_by("-created_at")[0:5],
        'yourmatches': (Match.objects.filter(winner_id=user)|Match.objects.filter(loser_id=user)).order_by("-created_at")[0:5],
        'allusers': User.objects.all(),
        'opponent': User.objects.get(username="jqchang")
    }
    return render(request, 'teambuilder/battle.html', context)

def battle_ajax(request):
    if "user_id" in request.session:
        user_id = request.session["user_id"]
    else:
        return JsonResponse({"success":False})
    results = Match.objects.battle(request.session["user_id"], 1)
    return JsonResponse(results)

'''
route planning:
calculate(postData, create=False): sends POST async request to /calc/, route runs validate
    returns JSONResponse: valid = true w/ object, invalid = false w/ errors
    JQuery success - adds pokemon to belt

delete(roster_id): sends GET request to delete the pokemon

battle(player_id): Roster model objects compare each other, then returns winner, switching their leaderboard positions
    generates new leaderboard position for unranked players

'''
