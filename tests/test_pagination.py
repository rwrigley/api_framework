import json
from unittest import mock

from api_framework.controllers import ListAPIController
from api_framework.pagination import PageNumberPagination
from .models import Job, proxy
from .schemas import JobSchema


def test_pagination(db):
    proxy.initialize(db)
    db.create_tables([Job])
    for i in range(15):
        Job.create(number=str(i))

    class TestPaginator(PageNumberPagination):
        page_size = 10

    class JobListAPIController(ListAPIController):
        modelselect = Job   
        schema_class = JobSchema
        pagination_class = TestPaginator


    controller = JobListAPIController()

    req = mock.Mock()
    req.params = {'page': 1}
    resp = mock.Mock()

    controller.on_get(req, resp)
    data = json.loads(resp.body)
    assert data['count'] == 15
    a = data['results'][0]
    assert a['number'] == '0'

    
    req = mock.Mock()
    req.params = {'page': 2}
    resp = mock.Mock()

    controller.on_get(req, resp)
    data = json.loads(resp.body)
    assert data['count'] == 15
    a = data['results'][0]
    assert a['number'] == '10'