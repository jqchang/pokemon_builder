from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..logreg.models import User, Pokemon
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
    errors = []
    if request.method != 'POST':
        errors.append("Please use the form to calculate Pokemon data.")
    else:
        pokemon = {
            "id":request.POST["id"],
            "nature":request.POST["nature"],
            "hp_iv":request.POST["hp_iv"],
            "hp_ev":request.POST["hp_ev"],
            "atk_iv":request.POST["atk_iv"],
            "atk_ev":request.POST["atk_ev"],
            "def_iv":request.POST["def_iv"],
            "def_ev":request.POST["def_ev"],
            "spa_iv":request.POST["spa_iv"],
            "spa_ev":request.POST["spa_ev"],
            "spd_iv":request.POST["spd_iv"],
            "spd_ev":request.POST["spd_ev"],
            "spe_iv":request.POST["spe_iv"],
            "spe_ev":request.POST["spe_ev"],
            "base": {
                "hp":request.POST["hp_base"],
                "atk":request.POST["atk_base"],
                "def":request.POST["def_base"],
                "spa":request.POST["spa_base"],
                "spd":request.POST["spd_base"],
                "spe":request.POST["spe_base"]
            }
        }

        if request.POST["id"] == "":
            errors.append("Please select a Pokemon!")
        if request.POST["nature"] == "":
            errors.append("Please select a nature!")
        if len(errors) == 0:
            new_stat = Pokemon.objects.stat_calc(request.POST)
            if "save" in request.POST:
                print "Attempting to save"
                try:
                    user = User.objects.get(id=request.session["user_id"])
                except User.DoesNotExist:
                    errors.append("An error has occurred. Please log out and log in again.")
                    return JsonResponse({"success":False, "errors":errors})
                pokemon = Pokemon.objects.create(pokeid=request.POST['id'], hp=new_stat[0], atk=new_stat[1], defense=new_stat[2], spatk=new_stat[3], spdef=new_stat[4], speed=new_stat[5], nature=request.POST['nature'], trainer=user)
            # display on roster
            # # return createchart()
            return JsonResponse({"success":True, "pokemon":new_stat})
            # else:
            #     return JsonResponse({"success":True, "pokemon":pokemon})

        else:
            return JsonResponse({"success":False, "errors":errors})

def battle(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'allusers': User.objects.all(),
        'opponent': User.objects.get(username="jqchang")
    }
    return render(request, 'teambuilder/battle.html', context)


'''
route planning:
calculate(postData, create=False): sends POST async request to /calc/, route runs validate
    returns JSONResponse: valid = true w/ object, invalid = false w/ errors
    JQuery success - adds pokemon to belt

delete(roster_id): sends GET request to delete the pokemon

battle(player_id): Roster model objects compare each other, then returns winner, switching their leaderboard positions
    generates new leaderboard position for unranked players

'''
