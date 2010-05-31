from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from voting.managers import VoteManager


class Vote(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices=((1, 1), (-1, -1)))

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

