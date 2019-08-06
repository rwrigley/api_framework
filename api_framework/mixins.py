import falcon_marshmallow
import marshmallow_peewee
import peewee
import marshmallow
import falcon


class ListModelMixin:
    def list(self, req, resp, *args, **kwargs):
        ms = self.filter_modelselect(req, self.get_model_select())
        ms = self.prefetch_modelselect(ms)
        page = self.paginate_modelselect(req, ms)
        schema = self.get_schema(many=True)
        
        if page is not None:
            data, errors = schema.dump(page)
            resp.body = self.get_paginated_response(data)

        else:
            data, _ = self.get_schema(strict=True).dumps(ms, many=True)
            resp.body = data


class CreateModelMixin:
    def create(self, req, resp, *args, **kwargs):
        try:
            instance, _ = self.get_schema(strict=True).load(req.media)
        except marshmallow.exceptions.ValidationError as errors:
            raise falcon.HTTPBadRequest('Invalid payload', errors.messages)
        except TypeError: 
            raise falcon.HTTPBadRequest('Payload cannot be parsed as JSON')
        self.perform_create(instance, req)
        result, _ = self.get_schema(strict=True).dumps(instance)
        resp.body = result
        resp.status = falcon.HTTP_201
    
    def perform_create(self, instance, *args):
        instance.save()


class RetrieveModelMixin:
    def retrieve(self, req, resp, *args, **kwargs):
        instance = self.get_object(req, *args, **kwargs)
        schema = self.get_schema(strict=True)
        results, _ = schema.dumps(instance)
        resp.body = results


class UpdateModelMixin:
    def update(self, req, resp, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(req, *args, **kwargs)
        schema = self.get_schema(instance, partial=partial, strict=True)

        try: 
            loaded, _ = schema.load(req.media)
        except marshmallow.exceptions.ValidationError as errors:
            raise falcon.HTTPBadRequest('Invalid payload', errors.messages)
        except TypeError: 
            raise falcon.HTTPBadRequest('Payload cannot be parsed as JSON')

        self.perform_update(instance, req)
        result, _ = schema.dumps(instance)
        resp.body = result

    def perform_update(self, instance, *args):
        instance.save()

class DestroyModelMixin:
    def destroy(self, req, resp, *args, **kwargs):
        instance = self.get_object(req, *args, **kwargs)
        instance.delete().execute()
        resp.status = falcon.HTTP_204
