from django.conf import settings
from reputation.handlers import BaseReputationHandler
from reputation import reputation_registery


class VotingVoteReputationHandler(BaseReputationHandler):
    """
    Handler for teknolab-django-voting Vote
    """
    UP_VALUE = 15
    DOWN_VALUE = -5
    
    def check_conditions(self, instance):
        return True
    
    def get_target_object(self, instance):
        return instance.content_object
    
    def get_target_user(self, instance):
        return getattr(instance.object, 'user', None)
    
    def get_originating_user(self, instance):
        return getattr(instance, 'user', None)
    
    def get_reputation_action(self, instance):
        if instance.mode == 'up':
            action_object = ReputationAction.objects.get(name = 'voted_up')
        elif instance.mode == 'down':
            action_object = ReputationAction.objects.get(name = 'voted_down')
        return action_object
    
    def get_value(self, instance):
        value = 0
        if instance.vote == 1:
            value = self.UP_VALUE
        elif instance.vote == -1:
            value = self.DOWN_VALUE
        return value

reputation_registry.register(VotingVoteReputationHandler)
