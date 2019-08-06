from .models import Book
from .schemas import BookSchema
from api_framework.controllers import CreateAPIController, RetrieveAPIController

def test_not_found(build_test_client, bind_models):
    bind_models(Book)

    class BookController(RetrieveAPIController):
        modelselect = Book
        schema_class = BookSchema

    client = build_test_client({'/books/{id}': BookController()})
    result = client.simulate_get('/books/1')
    assert result.status_code == 404

def test_schema_validation(build_test_client, bind_models):
    bind_models(Book)

    class BookController(CreateAPIController):
       modelselect = Book
       schema_class = BookSchema

    client = build_test_client({'/books': BookController()}) 
    
    result = client.simulate_post('/books')
    assert result.status_code == 400 
    data = result.json
    assert 'title' in data
    assert data['title'] == "Payload cannot be parsed as JSON"

    result = client.simulate_post('/books', json={'author': True, 'title': 1})
    data = result.json
    author_msgs = data['description']['author']
    assert author_msgs == ['Not a valid string.']
    title_msgs = data['description']['title']
    assert title_msgs == ['Not a valid string.']
    