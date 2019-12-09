import string
import random

from django.test import TestCase
from core.models.globals import User, Cards

def create_test_obj(card=1, user=1):
    for i in range(card):
        Cards.objects.create(
            name=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)),
            offer_profit=int(''.join(random.choice(string.digits) for _ in range(2))),
            binnary_profit=int(''.join(random.choice(string.digits) for _ in range(2))),
        )
    for i in range(user):
        User.objects.create_user(
            password=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20)),
            cart_number=int(''.join(random.choice(string.digits) for _ in range(12))),
            cart_type_id=random.choice([i[0] for i in Cards.objects.all().values_list('id')]),
            first_name=''.join(random.choice(string.ascii_lowercase + ' ') for _ in range(10)),
            last_name=''.join(random.choice(string.ascii_lowercase + ' ') for _ in range(10)),
            refer_id=random.choice([i[0] for i in User.objects.all().values_list('id')]) if User.objects.all().count() else None,
        )
