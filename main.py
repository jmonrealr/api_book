from flask import Flask, jsonify, abort, request
from faker import Faker

app = Flask(__name__)

columns = ['id_book', 'title', 'authors', 'isbn', 'language', 'num_pages']  # Only for reference

fake = Faker()


def make_book(id_book):
    """
    Generates a book with fake data
    using Faker
    :param id_book: id to use
    :return: new book
    """
    book = {
        'id_book': id_book,
        'title': fake.sentence(4),
        'authors': fake.name(),
        'isbn': fake.isbn10(),
        'language': fake.language_code(),
        'num_pages': fake.random_number(3)
    }
    return book


def _next_id():
    """
    Select all the book book ids and then get the largest value.
    It increments the value by one to get the next id
    :return: Return the next int id
    """
    return max(book['id_book'] for book in books) + 1


books = [make_book(i) for i in range(10)]


def find_book(id_book):
    """
    Iterate the books to find book with the id requested and if exist take his index
    If not return -1
    :param id_book: of the book to be found
    :return:
        If exist the book return his index
        If not return -1
    """
    for i in range(len(books)):
        if books[i]['id_book'] == id_book:
            return i
    return -1


@app.get("/books")
def get_books():
    return jsonify(books)


@app.post("/books")
def add_book():
    if request.is_json:
        book = request.get_json()
        book['id_book'] = _next_id()
        books.append(book)
        return {'success': "Record Stored"}, 201
    return {'error': 'Request must be JSON'}, 415  # media type not compatible


@app.get("/books/<id_book>")
def get_book(id_book):
    id_book = int(id_book)
    try:
        return jsonify(books[id_book])
    except KeyError:
        abort(404)


@app.delete("/books/<id_book>")
def remove_book(id_book):
    id_book = int(id_book)
    if len(books) > 0:
        id = find_book(id_book)
        if id != -1:
            del books[id]
            return {'success': "Record deleted"}
    return {'error': 'Not found'}, 404


@app.put("/books/<id_book>")
def update_book(id_book):
    id_book = int(id_book)
    if len(books) > 0:
        if request.is_json:
            id = find_book(id_book)
            book = request.get_json()
            if id != -1:
                books[id].update(book)
                return {'success': "Record updated"}
        else:
            return {'error': 'Request must be JSON'}, 415  # media type not compatible
    return {'error': 'Not found'}, 404


if __name__ == "__main__":
    app.run(debug=True)
    # print(books)
