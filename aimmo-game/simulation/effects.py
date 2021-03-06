from abc import ABCMeta, abstractmethod

import math

import sys


class _Effect(object):
    __metaclass__ = ABCMeta

    def __init__(self, avatar):
        self._avatar = avatar
        self.is_expired = False

    @abstractmethod
    def on_turn(self):
        raise NotImplementedError()


class _TimedEffect(_Effect):
    __metaclass__ = ABCMeta
    EFFECT_TIME = 10

    def __init__(self, *args):
        super(_TimedEffect, self).__init__(*args)
        self._time_remaining = self.EFFECT_TIME

    def remove(self):
        try:
            self._avatar.effects.remove(self)
        except KeyError as e:
            raise KeyError("The avatar object does not exist! Cannot remove the effect.")

    def on_turn(self):
        self._time_remaining -= 1
        if self._time_remaining <= 0:
            self.is_expired = True


class InvulnerabilityPickupEffect(_TimedEffect):
    def __init__(self, *args):
        super(InvulnerabilityPickupEffect, self).__init__(*args)
        self._avatar.resistance += 1000

    def remove(self):
        super(InvulnerabilityPickupEffect, self).remove()
        self._avatar.resistance -= 1000


class DamageBoostPickupEffect(_TimedEffect):
    def __init__(self, damage_boost, *args):
        # For now we have no maximum damage boost constraints, so infinity needs to be casted into a max int.
        if math.isinf(damage_boost):
            damage_boost = sys.maxsize

        self._damage_boost = int(round(damage_boost))
        super(DamageBoostPickupEffect, self).__init__(*args)
        self._avatar.attack_strength += self._damage_boost

    def remove(self):
        super(DamageBoostPickupEffect, self).remove()
        self._avatar.attack_strength -= self._damage_boost
