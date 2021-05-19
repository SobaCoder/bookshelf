import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
import random

from dbsetupmodels import setup_db, Book

BOOKS_PER_SHELF = 8
app = Flask(__name__)
# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there. 
#     If you do not update the endpoints, the lab will not work - of no fault of your API code! 
#   - Make sure for each route that you're thinking through when to abort and with which kind of error 
#   - If you change any of the response body keys, make sure you update the frontend to correspond. 

#def create_app(test_config=None):
  # create and configure the app

setup_db(app)
CORS(app)
  
   
  # CORS Headers 
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

  # @TODO: Write a route that retrivies all books, paginated. 
  #         You can use the constant above to paginate by eight books.
  #         If you decide to change the number of books per page,
  #         update the frontend to handle additional books in the styling and pagination
  #         Response body keys: 'success', 'books' and 'total_books'
  # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
def paginate_books(page, selection):
  start = (page-1) * BOOKS_PER_SHELF
  end = start + BOOKS_PER_SHELF
  
  books = [book.format() for book in selection]
  current_books = books[start:end]
  return current_books

@app.route('/books/<page_id>')
def show_books(page_id):
    selection = Book.query.order_by('id').all()
    page = request.args.get('page_id', 1, type=int)
    current_books = paginate_books(page, selection)
    if len(current_books) == 0:
      abort(404)
      
    return render_template('index.html', books=current_books)

@app.route('/')
def all_books():
  return redirect(url_for('show_books', page_id=1))


# @TODO: Write a route that will update a single book's rating. 
#         It should only be able to update the rating, not the entire representation
#         and should follow API design principles regarding method and route.  
#         Response body keys: 'success'
# TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
#@app.route('/books/<int:book_id>')
#def get_specific_book(book_id): 
  
    

  # @TODO: Write a route that will delete a single book. 
  #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
  #        Response body keys: 'success', 'books' and 'total_books'

  # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.
@app.route('/<book_id>/delete', methods=['DELETE'])
def delete_book(book_id):
  error = False
  try:
    book = Book.query.get(book_id)
    book.delete()
  except:
    error = True
  if error:
    abort(500)
  return jsonify({ 'success': True })

  # @TODO: Write a route that create a new book. 
  #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
  # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books. 
  #       Your new book should show up immediately after you submit it at the end of the page.
@app.route('/createbook', methods=['POST'])
def add_book():
  error = False
  body = request.get_json()
  try:
    booktitle = body.get('booktitle', None)
    bookauthor = body.get('bookauthor', None)
    bookrating = body.get('bookrating', None)
    book = Book(title=booktitle, author=bookauthor, rating=bookrating)
    book.insert()
    body['success'] = True
    body['bookid'] = book.id
    body['booktitle'] = book.title
    body['bookauthor'] = book.author
    body['bookrating'] = book.rating
  except:
    error = True
  if error:
    abort (422)
  else:
    return jsonify(body)
       
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

    