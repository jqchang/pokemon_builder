from __future__ import unicode_literals
from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    # Login checks and functions
    def login(self, **kwargs):
        print "** User manager activated **"
        print "** Checking login info **"
        status = {}
        messages = []
        username = kwargs['username'][0]
        password = kwargs['password'][0]
        if len(username) < 1 or len(password) < 1:
            messages.append("Login fields cannot be blank.")
        else:
            userinfo = User.objects.filter(username=username)
            if not userinfo:
                messages.append("Unable to find user. Please register.")
            elif not bcrypt.checkpw(password.encode(), userinfo[0].password.encode()):
                messages.append("Incorrect password.")
        if not messages:
            valid = True
            status.update({'user_id': userinfo[0].id})
        else:
            valid = False
            status.update({'messages': messages})
        status.update({'valid': valid})
        return status
    # Register checks and functions
    def register(self, **kwargs):
        print "** User manager activated **"
        print "** Checking registration form **"
        status = {}
        messages = []
        username = kwargs['username'][0]
        pword = kwargs['pword'][0]
        cpword = kwargs['c-pword'][0]
        if len(username) < 1:
            messages.append('Username is required.')
        elif len(username) < 2:
            messages.append('Username has to be at least 2 characters.')
        elif len(username) > 16:
            messages.append('Username cannot be more than 16 characters.')
        elif len(User.objects.filter(username__iexact=username)) > 0:
            messages.append('Username already taken.')
        if len(pword) < 1:
            messages.append('Password is required.')
        elif len(pword) < 8:
            messages.append('Password should be at least 8 characters.')
        elif pword != cpword:
            messages.append('Password fields do not match.')
        if not messages:
            valid = True
            messages.append('Thank you for registering! Please sign in.')
            pw_hash = bcrypt.hashpw(pword.encode(), bcrypt.gensalt())
            User.objects.create(username=username, password = pw_hash)
        else:
            valid = False
        status.update({'valid': valid, 'messages': messages})
        return status

class PokeManager(models.Manager):
    def stat_calc(self, postData):
        hp = int(postData['hp_base'])
        attack = int(postData['atk_base'])
        defense = int(postData['def_base'])
        sp_atk = int(postData['spa_base'])
        sp_def = int(postData['spd_base'])
        speed = int(postData['spe_base'])
        pkid = int(postData['id'])
        hp = (2 * int(hp)) + int(postData['hp_iv']) + (int(postData['hp_ev']) / 4) + 110
        attack = (2 * int(attack)) + int(postData['atk_iv']) + (int(postData['atk_ev']) / 4) + 5
        defense = (2 * int(defense)) + int(postData['def_iv']) + (int(postData['def_ev']) / 4) + 5
        sp_atk = (2 * int(sp_atk)) + int(postData['spa_iv']) + (int(postData['spa_ev']) / 4) + 5
        sp_def = (2 * int(sp_def)) + int(postData['spd_iv']) + (int(postData['spd_ev']) / 4) + 5
        speed = (2 * int(speed)) + int(postData['spe_iv']) + (int(postData['spe_ev']) / 4) + 5
        if postData['nature'] == 'adamant':
          attack *= 1.1
          sp_atk *= 0.9
        if postData['nature'] == 'lonely':
          attack *= 1.1
          defense *= 0.9
        if postData['nature'] == 'brave':
          attack *= 1.1
          speed *= 0.9
        if postData['nature'] == 'naughty':
          attack *= 1.1
          sp_def *= 0.9
        if postData['nature'] == 'bold':
          defense *= 1.1
          attack *= 0.9
        if postData['nature'] == 'relaxed':
          defense *= 1.1
          speed *= 0.9
        if postData['nature'] == 'impish':
          defense *= 1.1
          sp_atk *= 0.9
        if postData['nature'] == 'lax':
          defense *= 1.1
          sp_def *= 0.9
        if postData['nature'] == 'timid':
          speed *= 1.1
          attack *= 0.9
        if postData['nature'] == 'hasty':
          speed *= 1.1
          defense *= 0.9
        if postData['nature'] == 'jolly':
          speed *= 1.1
          sp_atk *= 0.9
        if postData['nature'] == 'naive':
          speed *= 1.1
          sp_def *= 0.9
        if postData['nature'] == 'modest':
          sp_atk *= 1.1
          attack *= 0.9
        if postData['nature'] == 'mild':
          sp_atk *= 1.1
          defense *= 0.9
        if postData['nature'] == 'quiet':
          sp_atk *= 1.1
          speed *= 0.9
        if postData['nature'] == 'rash':
          sp_atk *= 1.1
          sp_def *= 0.9
        if postData['nature'] == 'calm':
          sp_def *= 1.1
          attack *= 0.9
        if postData['nature'] == 'gentle':
          sp_def *= 1.1
          defense *= 0.9
        if postData['nature'] == 'sassy':
          sp_def *= 1.1
          speed *= 0.9
        if postData['nature'] == 'careful':
          sp_def *= 1.1
          sp_atk *= 0.9
        array = [int(hp), int(attack), int(defense), int(sp_atk), int(sp_def), int(speed), int(pkid)]
    # obj = {"hp": int(hp), "attack": int(attack), "defense": int(defense), "sp_atk": int(sp_atk), "sp_def": int(sp_def), "speed": int(speed)}
        return array

    def validation(self, postData):
        errors = []
        pokemon = {
            "id":int(postData["id"]),
            "nature":postData["nature"],
            "hp_iv":int(postData["hp_iv"]),
            "hp_ev":int(postData["hp_ev"]),
            "atk_iv":int(postData["atk_iv"]),
            "atk_ev":int(postData["atk_ev"]),
            "def_iv":int(postData["def_iv"]),
            "def_ev":int(postData["def_ev"]),
            "spa_iv":int(postData["spa_iv"]),
            "spa_ev":int(postData["spa_ev"]),
            "spd_iv":int(postData["spd_iv"]),
            "spd_ev":int(postData["spd_ev"]),
            "spe_iv":int(postData["spe_iv"]),
            "spe_ev":int(postData["spe_ev"]),
            "base": {
                "hp":int(postData["hp_base"]),
                "atk":int(postData["atk_base"]),
                "def":int(postData["def_base"]),
                "spa":int(postData["spa_base"]),
                "spd":int(postData["spd_base"]),
                "spe":int(postData["spe_base"])
            }
        }
        if postData["id"] == "":
            errors.append("Please select a Pokemon!")
        if postData["nature"] == "":
            errors.append("Please select a nature.")
        if pokemon['hp_ev'] + pokemon['atk_ev'] + pokemon['def_ev'] + pokemon['spa_ev'] + pokemon['spd_ev'] + pokemon['spe_ev'] > 510:
            errors.append("EVs cannot add up to greater than 510.")
        if pokemon['hp_ev'] > 255 or pokemon['atk_ev'] > 255 or pokemon['def_ev'] > 255 or pokemon['spa_ev'] > 255 or pokemon['spd_ev'] > 255 or pokemon['spe_ev'] > 255:
            errors.append("Each EV cannot be greater than 255.")
        if pokemon['hp_iv'] > 31 or pokemon['atk_iv'] > 31 or pokemon['def_iv'] > 31 or pokemon['spa_iv'] > 31 or pokemon['spd_iv'] > 31 or pokemon['spe_iv'] > 31:
            errors.append("Each IV cannot be greater than 31.")
        if len(errors):
            return (False, errors)
        return (True, errors)

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    rank = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Pokemon(models.Model):
    pokeid = models.IntegerField()
    hp = models.IntegerField()
    atk = models.IntegerField()
    defense = models.IntegerField()
    spatk = models.IntegerField()
    spdef = models.IntegerField()
    speed = models.IntegerField()
    nature = models.CharField(max_length=255)
    trainer = models.ForeignKey(User, related_name="pkmn")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PokeManager()
