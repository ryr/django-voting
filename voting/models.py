from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models

from voting.managers import VoteManager

SCORES = (
    (u'+1', +1),
    (u'-1', -1),
)

class Vote(models.Model):
    """
    A vote on an object by a User.
    """
    user         = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id    = models.PositiveIntegerField()
    object       = generic.GenericForeignKey('content_type', 'object_id')
    vote         = models.SmallIntegerField(choices=SCORES)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        unique_together = (('user', 'content_type', 'object_id'),)
        permissions = (('can_vote_up', 'Can vote up'),
                       ('can_vote_down', 'Can vote down'))

    def __unicode__(self):
        return u'%s: %s on %s' % (self.user, self.vote, self.object)

    def is_upvote(self):
        return self.vote == 1

    def is_downvote(self):
        return self.vote == -1


class VotingReputationHandler(BaseReputationHandler):
    model = Vote
    UP_VALUE = 15
    DOWN_VALUE = -5

    def check_conditions(self, instance):
        return True
    
    def get_target_object(self, instance):
        return instance.object
    
    def get_target_user(self, instance):
        return getattr(instance.object, 'user', None)
    
    def get_originating_user(self, instance):
        return getattr(instance, 'user', None)
            
    def get_value(self, instance):
        value = 0
        if instance.vote == 1:
            value = self.UP_VALUE
        elif instance.vote == -1:
            value = self.DOWN_VALUE
        return value
