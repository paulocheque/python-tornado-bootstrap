# coding: utf-8
from datetime import datetime
import os
import re
import sha

from mongoengine import *


class User(Document):
    email = EmailField(required=True)
    password = StringField() # social login
    secret_key = StringField(required=True)
    admin = BooleanField()

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
        if len(password) < 10 or len(password) > 512: return False
        if re.match('.*\s+', password): return False
        if not re.match('.*[a-z]+', password): return False
        if not re.match('.*[A-Z]+', password): return False
        if not re.match('.*[0-9]+', password): return False
        if not re.match('.*[!@#$%&*()_+-={}|/?;:,.<>\\\[\]]+', password): return False
        return True

    def save(self, encrypt_pass=False, **kwargs):
        if encrypt_pass:
            self.validate_password()
            self.password = User.encrypt_password(self.password)
        created = self.id is None
        if not self.secret_key:
            self.secret_key = User.generate_secret_key()
        super(User, self).save(**kwargs)

    def validate_password(self):
        errors = {}
        try:
            super(User, self).validate()
        except ValidationError as e:
            errors = e.errors

        if not User.is_valid_password(self.password):
            msg = "Invalid password. It must have at least 10 chars, 1 lower case, 1 upper case, 1 number, 1 symbol."
            errors['password'] = ValidationError(msg, field_name='password')
        if errors:
            raise ValidationError('ValidationError', errors=errors)

    def change_password(self, current_password, new_password):
        errors = {}
        if User.encrypt_password(current_password) != self.password:
            errors['password'] = ValidationError('The current password is wrong', field_name='password')
        if current_password != self.password:
            errors['password'] = ValidationError('New password must not be the same as the old one', field_name='password')
        if errors:
            raise ValidationError('ValidationError', errors=errors)
        self.password = new_password
        self.save(encrypt_pass=True)


# Migration
# users = User.objects.filter(secret_key=None)
# for u in users:
#     u.save()
