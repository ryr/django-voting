from reputation.handlers import BaseReputationHandler


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
