# Extra utils for string, time
import random

from django.utils import timezone


class ExtraUtils(object):

    @staticmethod
    def today():
        localtime = timezone.localtime(timezone.now())
        return localtime.strftime('%Y-%m-%d')

    @staticmethod
    def now():
        localtime = timezone.localtime(timezone.now())
        return localtime.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def random_20():
        rand = 1 if random.random() < 0.1 else 0
        return rand

    @staticmethod
    def captcha_number():
        return random.randint(1111, 9999)


