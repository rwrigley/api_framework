from .generics import GenericAPIController
from .mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetreiveModelMixin, UpdateModelMixin


class CreateAPIController(GenericAPIController, CreateModelMixin):
    def on_post(self, req, resp, *args, **kwargs):
        self.create(req, resp, *args, **kwargs)

class RetreiveAPIController(GenericAPIController, RetreiveModelMixin):
    def on_get(self, req, resp, *args, **kwargs):
        self.retreive(req, resp, *args, **kwargs)


class ListAPIController(GenericAPIController, ListModelMixin):
    def on_get(self, req, resp, *args, **kwargs):
        self.list(req, resp, *args, **kwargs)


class DestroyAPIController(GenericAPIController, DestroyModelMixin):
    def on_delete(self, req, resp, *args, **kwargs):
        self.destroy(req, resp, *args, **kwargs)


class UpateAPIController(GenericAPIController, UpdateModelMixin):
    def on_patch(self, req, resp, *args, **kwargs):
        self.update(req, resp, partial=True, *args, **kwargs)

    def on_put(self, req, resp, *args, **kwargs):
        self.update(req, resp, partial=False, *args, **kwargs)


class ListCreateAPIController(GenericAPIController, ListModelMixin,
                              CreateModelMixin):
    def on_get(self, req, resp, *args, **kwargs):
        self.list(req, resp, *args, **kwargs)

    def on_post(self, req, resp, *args, **kwargs):
        self.create(req, resp, *args, **kwargs)


class RetreiveUpdateAPIController(GenericAPIController, RetreiveModelMixin,
                                  UpdateModelMixin):
    def on_get(self, req, resp, *args, **kwargs):
        self.retreive(req, resp, *args, **kwargs)

    def on_put(self, req, resp, *args, **kwargs):
        self.update(req, resp, partial=False, *args, **kwargs)

    def on_patch(self, req, resp, *args, **kwargs):
        self.update(req, resp, partial=True, *args, **kwargs)


class RetreiveDestroyAPIController(GenericAPIController, RetreiveModelMixin,
                                   DestroyModelMixin):
    def on_delete(self, req, resp, *args, **kwargs):
        self.destroy(req, resp, *args, **kwargs)

    def on_get(self, req, resp, *args, **kwargs):
        self.retreive(req, resp, *args, **kwargs)


class RetreiveUpdateDestoryAPIController(GenericAPIController,
                                         RetreiveModelMixin, UpdateModelMixin,
                                         DestroyModelMixin):
    def on_delete(self, req, resp, *args, **kwargs):
        self.destroy(req, resp, *args, **kwargs)

    def on_get(self, req, resp, *args, **kwargs):
        self.retreive(req, resp, *args, **kwargs)

    def on_put(self, req, resp, *args, **kwargs):
        self.update(req, resp, partial=False, *args, **kwargs)

    def on_patch(self, req, resp, *args, **kwargs):
        self.update(req, resp, partial=True, *args, **kwargs)