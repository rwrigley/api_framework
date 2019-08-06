import peewee
import falcon
import marshmallow
from .pagination import PageNumberPagination


class GenericAPIController:
    modelselect = None
    schema_class = None
    lookup_field = 'id'
    lookup_url_kwarg = None
    filter_backends = []
    prefetch = None
    pagination_class = PageNumberPagination

    def get_model_select(self):
        assert self.modelselect is not None, (
            "'%s' should either include a `model` attribute, "
            "or override the `get_model()` method." % self.__class__.__name__)

        modelselect = self.modelselect
        if issubclass(modelselect, peewee.Model):
            # Ensure modelselect is re-evaluated on each request.
            modelselect = modelselect.select()
        return modelselect

    def get_schema_class(self):
        assert self.schema_class is not None, (
            "'%s' should either include a `schema_class` attribute, "
            "or override the `get_schema_class()` method." %
            self.__class__.__name__)
        return self.schema_class

    def get_prefetch(self):
        return self.prefetch

    def get_schema(self, *args, **kwargs):
        schema_class = self.get_schema_class()
        kwargs['context'] = self.get_schema_context()
        return schema_class(*args, **kwargs)

    def get_schema_context(self):
        return {'controller': self}

    def filter_modelselect(self, req, modelselect):
        for backend in list(self.filter_backends):
            modelselect = backend().filter_modelselect(req, modelselect, self)
        return modelselect

    def prefetch_modelselect(self, modelselect):
        prefetch = self.get_prefetch()
        if prefetch:
            return modelselect.prefetch(*prefetch)
        return modelselect

    def get_object(self, req, *args, **kwargs):
        modelselect = self.filter_modelselect(req, self.get_model_select())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg))

        filter_kwargs = {self.lookup_field: kwargs[lookup_url_kwarg]}
        modelselect = modelselect.filter(**filter_kwargs)

        try:
            obj = self.prefetch_modelselect(modelselect)[0]
        except(peewee.DoesNotExist, IndexError):
            raise falcon.HTTPNotFound()

        # May raise a permission denied
        self.check_object_permissions(req, obj)

        return obj

    def check_object_permissions(self, req, obj):
        import warnings
        warnings.warn('Obj permission not implemented yet')

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_modelselect(self, request, modelselect):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_modelselect(modelselect,
                                                request,
                                                view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)