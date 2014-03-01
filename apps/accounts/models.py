# coding: utf-8
from datetime import datetime
import os
import re
import sha

from mongoengine import *


SOCIAL_CHOICES = (('GH', 'GitHub'), ('F', 'Facebook'), ('G', 'Google'), ('T', 'Twitter'), ('FF', 'FriendFinder'), )

class User(Document):
    email = EmailField(required=True, max_length=1024)
    password = StringField(max_length=1024) # social login
    secret_key = StringField(required=True, max_length=1024)
    admin = BooleanField()

    social = StringField(required=False, choices=SOCIAL_CHOICES, max_length=2)
    registered_on = DateTimeField(required=True, default=datetime.utcnow)

    @classmethod
    def authenticate(cls, email, password):
        if password:
            pw = User.encrypt_password(password)
            return User.objects(email=email, password=pw)
        return []

    @classmethod
    def encrypt_password(cls, password):
        return sha.sha(password).hexdigest()

    @classmethod
    def generate_secret_key(cls):
        return os.urandom(24).encode('base64').strip()

    @classmethod
    def is_valid_password(cls, password):
        if not password: return False
        if len(password) < 10 or len(password) > 1024: return False
        if re.match('.*\s+', password): return False
        if not re.match('.*[a-z]+', password): return False
        if not re.match('.*[A-Z]+', password): return False
        if not re.match('.*[0-9]+', password): return False
        if not re.match('.*[!@#$%&*()_+-={}|/?;:,.<>\\\[\]]+', password): return False
        return True

    def pre_save(self, encrypt_pass=False):
        created = self.id is None
        if encrypt_pass:
            self.validate_password() # validate only for non-social logins
            self.password = User.encrypt_password(self.password)
        if not self.secret_key:
            self.secret_key = User.generate_secret_key()

    def save(self, encrypt_pass=False, **kwargs):
        self.pre_save(encrypt_pass=encrypt_pass)
        super(User, self).save(**kwargs)

    def get_or_create(encrypt_pass=False, write_concern=None, auto_save=True, *q_objs, **query):
        self.pre_save(encrypt_pass=encrypt_pass)
        return super(User, self).get_or_create(write_concern=write_concern, auto_save=auto_save, *q_objs, **query)

    def validate_password(self): # it must be called before encrypting the password
        if not User.is_valid_password(self.password):
            errors = {}
            print(self.password)
            msg = "Invalid password. It must have at least 10 chars, 1 lower case, 1 upper case, 1 number, 1 symbol."
            errors['password'] = ValidationError(msg, field_name='password')
            raise ValidationError('ValidationError', errors=errors)

    def change_password(self, current_password, new_password):
        errors = {}
        if User.encrypt_password(current_password) != self.password:
            errors['password'] = ValidationError('The current password is wrong', field_name='password')
        if current_password == new_password:
            errors['password'] = ValidationError('New password must not be the same as the old one', field_name='password')
        if errors:
            raise ValidationError('ValidationError', errors=errors)
        self.password = new_password
        self.save(encrypt_pass=True)


# Migration
# users = User.objects.filter(secret_key=None)
# for u in users:
#     u.save()
