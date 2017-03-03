from __future__ import unicode_literals

from django.db import models
from ..logreg.models import User, Pokemon


# Create your models here.
class MatchManager(models.Manager):
    def battle(self, user1_id, user2_id):
        # Returns match winner
        errors = []
        try:
            user1 = User.objects.get(id=user1_id)
            user2 = User.objects.get(id=user2_id)
        except User.DoesNotExist:
            errors.append("Match not found!")
        if len(errors) == 0:
            # Calculate match results
            roster1 = Pokemon.objects.filter(trainer=user1)
            stat1 = 0;
            for pk in roster1:
                stat1 += (pk.hp+pk.atk+pk.defense+pk.spatk+pk.spdef+pk.speed)
            roster2 = Pokemon.objects.filter(trainer=user2)
            stat2 = 0;
            for pk in roster2:
                stat2 += (pk.hp+pk.atk+pk.defense+pk.spatk+pk.spdef+pk.speed)
            # TEMPORARY:
            if stat2 > stat1:
                Match.objects.create(winner_id=user2, loser_id=user1)
                return {"winner":user2.username, "loser":user1.username}
            else:
                Match.objects.create(winner_id=user1, loser_id=user2)
                return {"winner":user1.username, "loser":user2.username}
            # /TEMPORARY
        else:
            return {"errors":errors}


class Match(models.Model):
    winner_id = models.ForeignKey(User, related_name='wins')
    loser_id = models.ForeignKey(User, related_name='losses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MatchManager()
