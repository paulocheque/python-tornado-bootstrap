# coding: utf-8
from .api import ApiHandler
from apps.accounts.models import User # FIXME need refactoring


class MongoEngineComplexDataManager(object):
    def __init__(self, model, filters):
        self.model = model
        self.filters = filters

    def expected_keys(self):
        return len(self.filters) + 1

    def read_list(self, identifiers, initial=0, amount=50):
        filters = {}
        for f, value in zip(self.filters, identifiers):
            # filters[f.__name__.lower()] = value
            filters[f.__name__.lower()] = f.objects(pk=value).get()
        return self.model.objects(**filters).all()[initial:initial+amount]

    def count(self):
        return self.read_list().count()

    def read(self, identifiers):
        identifier = identifiers[-1]
        try:
            return self.read_list(identifiers[:-1]).get(pk=identifier)
        except self.model.DoesNotExist:
            return None

    def create(self, identifiers, data, persist=True):
        obj = self.model(**data)
        for f, value in zip(self.filters, identifiers):
            setattr(obj, f.__name__.lower(), f.objects(pk=value).get())
        if persist:
            obj.save()
        return obj

    def update(self, identifiers, data):
        obj = self.read(identifiers)
        if obj:
            update_query = {}
            for key, value in data.items():
                if hasattr(obj, key):
                    update_query['set__%s' % key] = value
            obj.update(**update_query)
            obj.reload()
        return obj

    def delete(self, identifiers):
        obj = self.read(identifiers)
        if obj:
            obj.delete()
        return obj


class MongoEngineComplexDataManagerPerUser(MongoEngineComplexDataManager):
    def __init__(self, model, filters, user, user_filter_path='user'):
        super(MongoEngineComplexDataManagerPerUser, self).__init__(model, filters)
        self.user = user
        self.user_filter_path = user_filter_path

    def read_list(self, identifiers, initial=0, amount=50):
        objs = super(MongoEngineComplexDataManagerPerUser, self).read_list(identifiers, initial=initial, amount=amount)
        user_filter = {}
        user_filter[self.user_filter_path] = self.user
        # return objs(**user_filter)
        return objs

    def create(self, identifiers, data, persist=True):
        obj = super(MongoEngineComplexDataManagerPerUser, self).create(identifiers, data, persist=False)
        obj.user = self.user
        if persist:
            obj.save()
        return obj


class ComplexRestHandler(ApiHandler):
    perm_public = 'CRLUD'
    perm_user = 'CRLUD'
    perm_admin = 'CRLUD'

    def check_permission(self, action):
        user = self.get_current_user()
        admin = self.is_admin_user()
        if action in self.perm_public or (user and action in self.perm_user) or (admin and action in self.perm_admin):
            pass # ok
        else:
            self.raise403()

    # CREATE /objs
    def post(self, *identifiers, **kwargs):
        self.check_permission('C')
        data = self.get_request_data()
        obj = self.data_manager.create(identifiers, data)
        if obj:
            self.answer(obj)
        else:
            self.raise404()

    # LIST /objs/
    # READ /objs/:id
    def get(self, *identifiers, **kwargs):
        if len(identifiers) == 1 and identifiers[0] == 'count':
            self.answer(self.data_manager.count())
        elif len(identifiers) == self.data_manager.expected_keys():
            self.check_permission('R')
            obj = self.data_manager.read(identifiers)
            if obj:
                self.answer(obj)
            else:
                self.raise404()
        else:
            self.check_permission('L')
            # FIXME pagination
            initial = int(self.get_argument('initial', default=0))
            amount = int(self.get_argument('amount', default=50))
            amount = max(amount, initial) # amount < initial validation
            amount = min(amount, initial+50) # more than 50 records protection
            objs = self.data_manager.read_list(identifiers, initial=initial, amount=amount)
            self.answer(objs)

    # UPDATE /objs/:id
    def put(self, *identifiers, **kwargs):
        self.check_permission('U')
        data = self.get_request_data()
        obj = self.data_manager.update(identifiers, data)
        if obj:
            self.answer(obj)
        else:
            self.raise404()

    # DELETE /objs/:id
    def delete(self, *identifiers, **kwargs):
        self.check_permission('D')
        obj = self.data_manager.delete(identifiers)
        if obj:
            self.answer(obj)
        else:
            self.raise404()
