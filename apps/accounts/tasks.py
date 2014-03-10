# coding: utf-8
from apps.utils.tasks import get_country_from_ip

from .models import *


def update_country(user_id, ip):
    country = get_country_from_ip(ip)
    if country:
        country = country.lower()
        u = User.objects.get(id=user_id)
        u.country = country
        u.save()
