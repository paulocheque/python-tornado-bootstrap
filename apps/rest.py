# coding: utf-8
from apps.api import ApiHandler
from apps.accounts.models import User # FIXME need refactoring


class MongoEngineDataManager(object):
    def __init__(self, model):
        self.model = model

    def read_list(self, initial=0, amount=50):
        return self.model.objects.all()[initial:initial+amount]

    def count(self):
        return self.read_list().count()

    def read(self, identifier):
        try:
            return self.read_list().get(pk=identifier)
        except self.model.DoesNotExist:
            return None

    def create(self, data, persist=True):
        obj = self.model(**data)
        if persist:
            obj.save()
        return obj

    def update(self, identifier, data):
        obj = self.read(identifier)
        if obj:
            update_query = {}
            for key, value in data.items():
                update_query['set__%s' % key] = value
            obj.update(**update_query)
        return obj

    def delete(self, identifier):
        obj = self.read(identifier)
        if obj:
            obj.delete()
        return obj


class MongoEngineDataManagerPerUser(MongoEngineDataManager):
    def __init__(self, model, user):
        super(MongoEngineDataManagerPerUser, self).__init__(model)
        self.user = user

    def read_list(self, initial=0, amount=50):
        objs = super(MongoEngineDataManagerPerUser, self).read_list(initial=initial, amount=amount)
        return objs(user=self.user)

    def create(self, data, persist=True):
        obj = super(MongoEngineDataManagerPerUser, self).create(data, persist=False)
        obj.user = self.user
        if persist:
            obj.save()
        return obj


class RestHandler(ApiHandler):
    # CREATE /objs
    def post(self):
        data = self.get_request_data()
        obj = self.data_manager.create(data)
        if obj:
            self.answer(obj)
        else:
            self.raise404()

    # LIST /objs/
    # READ /objs/:id
    def get(self, identifier=None):
        if identifier:
            if identifier == 'count':
                self.answer(self.data_manager.count())
            else:
                obj = self.data_manager.read(identifier)
                if obj:
                    self.answer(obj)
                else:
                    self.raise404()
        else:
            # FIXME pagination
            initial = int(self.get_argument('initial', default=0))
            amount = int(self.get_argument('amount', default=50))
            amount = max(amount, initial) # amount < initial validation
            amount = min(amount, initial+50) # more than 50 records protection
            objs = self.data_manager.read_list(initial=initial, amount=amount)
            self.answer(objs)

    # UPDATE /objs/:id
    def put(self, identifier):
        data = self.get_request_data()
        obj = self.data_manager.update(identifier, data)
        if obj:
            self.answer(obj)
        else:
            self.raise404()

    # DELETE /objs/:id
    def delete(self, identifier):
        obj = self.data_manager.delete(identifier)
        if obj:
            self.answer(obj)
        else:
            self.raise404()

