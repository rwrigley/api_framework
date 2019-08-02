import falcon_marshmallow
import marshmallow_peewee
import peewee
import marshmallow
import falcon


class ListModelMixin:
    def list(self, req, resp, *args, **kwargs):
        ms = self.filter_modelselect(req, self.get_model_select())
        ms = self.prefetch_modelselect(ms)
        # TODO Add pagination
        # page = self.paginate_modelselect(modelselect)
        # if page is not None:
        #     result,  = self.get_schema(page, many=True)
        #     return self.get_paginated_response(marshal)

        # marshal, errors = self.schema().dumps(ms, many=True)
        result, errors = self.get_schema().dumps(ms, many=True)
        if errors:
            raise NotImplementedError('Error handling not implemented')
        resp.body = result


class CreateModelMixin:
    def create(self, req, resp, *args, **kwargs):
        instance, errors = self.get_schema().loads(req.stream)
        if errors:
            raise NotImplementedError('Error handling not implemented')
        instance.save()
        result, errors = self.get_schema().dumps(instance)
        if errors:
            raise NotImplementedError('Error handling not implemented')
        resp.body = result


class RetrieveModelMixin:
    def retrieve(self, req, resp, *args, **kwargs):
        instance = self.get_object(req, *args, **kwargs)
        schema = self.get_schema()
        results, errors = schema.dumps(instance)
        if errors:
            raise NotImplementedError
        resp.body = results


class UpdateModelMixin:
    def update(self, req, resp, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(req, *args, **kwargs)
        schema = self.get_schema(instance, partial=partial)
        loaded, errors = schema.loads(req.stream)
        if errors:
            raise NotImplementedError
        loaded.save()
        result, errors = schema.dumps(instance)
        if errors:
            raise NotImplementedError
        resp.body = result


class DestroyModelMixin:
    def destroy(self, req, resp, *args, **kwargs):
        instance = self.get_object(req, *args, **kwargs)
        instance.delete().execute()
        resp.status = falcon.HTTP_204
