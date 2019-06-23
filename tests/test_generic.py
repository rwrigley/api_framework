import json
from unittest import mock

import falcon
import peewee
import pytest

from api_framework.controller import (CreateModelMixin, DestroyModelMixin,
                                      GenericAPIController, ListModelMixin,
                                      RetreiveModelMixin, UpdateModelMixin)

from .models import Job, proxy
from .schemas import JobSchema


def test_list_model(db):
    proxy.initialize(db)
    db.create_tables([Job])

    class JobListAPIController(GenericAPIController, ListModelMixin):
        model = Job
        schema = JobSchema

    Job.create(number='1')

    ctlr = JobListAPIController()

    req = mock.Mock()
    resp = mock.Mock()

    ctlr.list(req, resp)
    assert not isinstance(resp.body, mock.Mock)
    result = json.loads(resp.body)
    assert len(result) == 1
    assert result[0]['number'] == '1'

def test_create_model(db):
    proxy.initialize(db)
    db.create_tables([Job])

    class JobCreateAPIController(GenericAPIController, CreateModelMixin):
        model = Job
        schema = JobSchema
    
    req = mock.Mock()
    req.stream = '{"number": "1"}'

    resp = mock.Mock()

    ctlr = JobCreateAPIController()
    ctlr.create(req, resp)
    assert not isinstance(resp.body, mock.Mock)
    result = json.loads(resp.body)
    assert result['number'] == '1'
    assert Job.get().number == '1'



def test_retreive_model(db):
    proxy.initialize(db)
    db.create_tables([Job])

    class JobRetreiveAPIController(GenericAPIController, RetreiveModelMixin):
        model = Job
        schema = JobSchema
    
    req = mock.Mock()
    resp = mock.Mock()
    job = Job.create(number='1')

    ctlr = JobRetreiveAPIController()
    ctlr.retreive(req, resp, id=1)
    assert not isinstance(resp.body, mock.Mock)
    result = json.loads(resp.body)
    assert result['number'] == '1'
    assert Job.get().number == '1'

def test_update_model(db):
    proxy.initialize(db)
    db.create_tables([Job])

    class JobUpdateAPIController(GenericAPIController, UpdateModelMixin):
        model = Job
        schema = JobSchema
    
    req = mock.Mock()
    req.stream = '{"number":"3"}'
    resp = mock.Mock()
    job = Job.create(number='2')

    ctlr = JobUpdateAPIController()
    ctlr.update(req, resp, id=1)
    assert not isinstance(resp.body, mock.Mock)
    result = json.loads(resp.body)
    assert result['number'] == '3'
    assert Job.get().number == '3'

def test_delete_model(db):
    proxy.initialize(db)
    db.create_tables([Job])

    class JobDestroyAPIController(GenericAPIController, DestroyModelMixin):
        model = Job
        schema = JobSchema
    
    req = mock.Mock()
    resp = mock.Mock()
    job = Job.create(number='2')

    ctlr = JobDestroyAPIController()
    ctlr.destroy(req, resp, id=1)
    assert len(Job.select()) == 0
    assert resp.status == falcon.HTTP_204
