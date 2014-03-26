# coding: utf-8
from mongoengine import *

from apps.utils.serializer import *


# addresses = ListField(EmbeddedDocumentField(Address), required=False)
# phones = ListField(EmbeddedDocumentField(Phone), required=False)
# credit_cards = ListField(EmbeddedDocumentField(CreditCard), required=False)


class Address(EmbeddedDocument):
    zip_code = StringField(required=True, max_length=20)
    street = StringField(required=True, max_length=50)
    number = StringField(required=True, max_length=10)
    city = StringField(required=True, max_length=30)
    state = StringField(required=False, max_length=30)
    country = StringField(required=False, max_length=20)


class Phone(EmbeddedDocument):
    number = StringField(required=True, max_length=20)
    reference = StringField(required=False, max_length=20)


class CreditCard(EmbeddedDocument):
    card_type = StringField(required=True, max_length=10)
    number = StringField(required=True, max_length=20)
    exp_month = StringField(required=True, max_length=2)
    exp_year = StringField(required=True, max_length=4)
    holders_name = StringField(required=True, max_length=50)
