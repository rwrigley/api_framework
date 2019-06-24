from .models import Job, proxy
from api_framework.controllers import ListAPIController
from .schemas import JobSchema
import json
from unittest import mock
from api_framework.filters import BaseFilterBackend


def test_simple_filter(db):
    proxy.initialize(db)
    db.create_tables([Job])

    Job.create(number='1A')
    Job.create(number='2BC')

    class JobNumberAFilter(BaseFilterBackend):
        def filter_modelselect(self, req, modelselect, controller):
            return modelselect.where(Job.number.contains('B'))

    class JobFilterAPIController(ListAPIController):
        modelselect = Job
        schema_class = JobSchema
        filter_backends = (JobNumberAFilter,)

    ctlr = JobFilterAPIController()

    req = mock.Mock()
    resp = mock.Mock()

    ctlr.on_get(req, resp)

    result = json.loads(resp.body)
    assert len(result) == 1
    assert result[0]['number'] == '2BC'
