from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
#import requests

engine = create_engine('sqlite:///catalog.db')
User.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
def ReadItems():
    categories = session.query(Category).all()
    #return categories.name
    return render_template('index.html', categories = categories)

#shows login button/page to allow user to authenticate.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

#add a category
@app.route('/catalog/category/new/', methods=['GET', 'POST'])
def AddCategory():
    if request.method == 'POST':
        NewItem = Category(name = request.form['music-genre'], created_by = 1)
        session.add(NewItem)
        session.commit()
        return redirect(url_for('ReadItems'))
    else:
        return render_template('AddCategory.html')

#edit a category
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def EditCategory(category_id):
    editedItem = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['music-genre']:
            editedItem.name = request.form['music-genre']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('ReadItems'))
    else:
        return render_template('EditCategory.html', category_id = category_id, item = editedItem)

#delete a category
@app.route('/catalog/<int:category_id>/delete/')
def DeleteCategory(category_id):
    deletedItem = session.query(Category).filter_by(id=category_id).one()
    session.delete(deletedItem)
    session.commit()
    return redirect(url_for('ReadItems'))

#displays all items in a category
@app.route('/catalog/<int:category_id>/items/')
def DisplayCategoryItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id)
    return render_template('DisplayItems.html', category = category, items = items, category_id = category_id)

#add an item to a category
@app.route('/catalog/<int:category_id>/new/', methods=['GET', 'POST'])
def NewItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Item(item_name=request.form['music-artist'], description=request.form['music-description'], category_id = category_id )
        session.add(newItem)
        session.commit()
        return redirect(url_for('DisplayCategoryItems',category_id=category_id, category = category ))
    else:
        return render_template('AddItem.html', category_id = category_id, category = category)

#show an item's details
@app.route('/catalog/<int:category_id>/<int:item_id>')
def ShowItem(category_id, item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('ShowItem.html', item = item, category_id = category_id, item_id=item_id)

#edit an item
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/')
def EditItem(category_id, item_id):
    if request.method =="GET":
        item = session.query(Item).filter_by(id = item_id).one()
        return render_template('EditItem.html', category_id = category_id, item_id=item_id, item=item)

#delete an item
@app.route('/catalog/<int:category_name>/delete/')
def DeleteItem(category_name):
    return "page to delete item here"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)