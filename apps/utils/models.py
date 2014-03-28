# coding: utf-8
from mongoengine import *

from apps.utils.serializer import *


# address = EmbeddedDocumentField(Address)
# phone = EmbeddedDocumentField(Phone)
# credit_card = EmbeddedDocumentField(CreditCard)
# addresses = ListField(EmbeddedDocumentField(Address), required=False)
# phones = ListField(EmbeddedDocumentField(Phone), required=False)
# credit_cards = ListField(EmbeddedDocumentField(CreditCard), required=False)


class Address(EmbeddedDocument):
    zip_code = StringField(max_length=20)
    street = StringField(max_length=50)
    number = StringField(max_length=10)
    city = StringField(max_length=30)
    state = StringField(max_length=30)
    country = StringField(max_length=20)

    def to_dict(self):
        return ObjectDict(zip_code=self.zip_code, street=self.street, number=self.number,
            city=self.city, state=self.state, country=self.country)


class Phone(EmbeddedDocument):
    number = StringField(max_length=20)
    reference = StringField(max_length=20)

    def to_dict(self):
        return ObjectDict(number=self.number, reference=self.reference)


class CreditCard(EmbeddedDocument):
    card_type = StringField(required=True, max_length=10)
    number = StringField(required=True, max_length=20)
    exp_month = StringField(required=True, max_length=2)
    exp_year = StringField(required=True, max_length=4)
    holders_name = StringField(required=True, max_length=50)

    def to_dict(self):
        return ObjectDict(card_type=self.card_type, number=self.number, exp_month=self.exp_month,
                exp_year=self.exp_year, holders_name=self.holders_name)
