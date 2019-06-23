import falcon_marshmallow
import marshmallow_peewee
import peewee
import marshmallow
import falcon



class GenericAPIController:
    model = None
    schema = None
    lookup_field = 'id'
    lookup_url_kwarg = None
    filter_backends = []

    def get_model_select(self):
        assert self.model is not None, (
            "'%s' should either include a `model` attribute, "
            "or override the `get_model()` method."
            % self.__class__.__name__
        )

        modelselect = self.model
        if isinstance(modelselect, peewee.Model):
            # Ensure modelselect is re-evaluated on each request.
            modelselect = modelselect.select()
        return modelselect
    
    def get_schema(self):
        assert self.schema is not None, (
            "'%s' should either include a `schema` attribute, "
            "or override the `get_schema()` method."
            % self.__class__.__name__
        )

        schema = self.schema
        if isinstance(schema, marshmallow.Schema):
            schema = schema()
        return schema
    
    def filter_modelselect(self, modelselect):
        for backend in list(self.filter_backends):
            modelselect = backend().filter_modelselect(self.request, modelselect, self)
        return modelselect

    
    def get_object(self, req, *args, **kwargs):
        modelselect = self.filter_modelselect(self.get_model_select())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: kwargs[lookup_url_kwarg]}
        obj = modelselect.get_or_none()
        if not obj:
            raise NotImplementedError('Raise 404 not implemented')

        # May raise a permission denied
        self.check_object_permissions(req, obj)

        return obj
    
    def check_object_permissions(self, req, obj):
        import warnings
        warnings.warn('Obj permission not implemented yet')

    @property
    def model(self):
        return self.get_model()
    
    def get_model(self):
        raise NotImplementedError

    @property
    def schema(self):
        raise NotImplementedError
    

class ListModelMixin:
    def list(self, req, resp, *args, **kwargs):
        ms = self.filter_modelselect(self.get_model_select())
        # TODO Add pagination
        # page = self.paginate_modelselect(modelselect)
        # if page is not None:
        #     result,  = self.get_schema(page, many=True)
        #     return self.get_paginated_response(marshal)
        
        # marshal, errors = self.schema().dumps(ms, many=True)
        result, errors = self.schema().dumps(ms, many=True)
        if errors:
            raise NotImplementedError('Error handling not implemented')
        resp.body = result

class CreateModelMixin:
    def create(self, req, resp, *args, **kwargs):
        instance, errors = self.schema().loads(req.stream)
        if errors:
            raise NotImplementedError('Error handling not implemented')
        instance.save()
        result, errors= self.schema().dumps(instance)
        if errors:
            raise NotImplementedError('Error handling not implemented')
        resp.body = result

class RetreiveModelMixin:
    def retreive(self, req, resp, *args, **kwargs):
        instance = self.get_object(req, *args, **kwargs)
        schema = self.get_schema()
        results, errors = schema().dumps(instance)
        if errors:
            raise NotImplementedError
        resp.body = results

class UpdateModelMixin:
    def update(self, req, resp, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(req, *args, **kwargs)
        schema = self.get_schema()
        loaded, errors = schema(instance, partial=partial).loads(req.stream)
        if errors:
            raise NotImplementedError
        loaded.save()
        result, errors = schema().dumps(instance)
        if errors:
            raise NotImplementedError
        resp.body = result
        
class DestroyModelMixin:
    def destroy(self, req, resp, *args, **kwargs):
        instance = self.get_object(req, *args, **kwargs)
        instance.delete().execute()
        resp.status = falcon.HTTP_204
