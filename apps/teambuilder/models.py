from __future__ import unicode_literals

from django.db import models
from ..logreg.models import User

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

            # TEMPORARY:
            return {"winner":user1, "loser":user2}
            # /TEMPORARY
        else:
            return {"errors":errors}


class Match(models.Model):
    winner_id = models.ForeignKey(User, related_name='wins')
    loser_id = models.ForeignKey(User, related_name='losses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MatchManager()
