from flask import *
from flask import session
from functools import wraps
from databasesetup import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib2
import string
import json
import random

# Setting up and connect to database.

engine = create_engine("sqlite:///itemcatalog.db")
DBSession = sessionmaker(bind=engine)
sess = DBSession()
app = Flask(__name__)


# arr1 = []
# arr2 = []
# arr3 = {}

# This will create an event when user is logged in.

def createEvent():
    statechar = (string.ascii_uppercase + string.digits)
    event = ''.join(random.choice(statechar) for i in range(32))

    return event

# This will retrieve user information from database.


def retrieveUserInfo(email):
    username = sess.query(User).filter(User.email == email).first()
    if username:
        return username.id
    else:
        return ""

# This will return categories as arrays.


def arrayofCategories(category):

    adictionary = dict()
    if category:
        items = sess.query(Item).filter(Item.category_id == category.id).all()
        arr2 = []

        for i in items:
            arr2.append(arrayofItems(i))

        adictionary['id'] = category.id
        adictionary['name'] = category.name
        adictionary['items'] = arr2

    return adictionary


# This will return array of items.

def arrayofItems(x):
    arr3 = {}
    if x:
        return {"category_id": x.category_id,
                "created": str(x.created),
                "item_id": x.id,
                "name": x.name,
                "description": x.description}
    else:
        return arr3


# This will retrieve items from database.

def retrieveItem(category_id, item_id):
    item = sess.query(Item).filter(Item.id == item_id) \
        .filter(Item.category_id == category_id).first()
    return item

# This will retrieve the categories from database.


def retrieveCategory(category_id):
    cat = sess.query(Category).filter(Category.id == category_id).first()
    return cat

# This will allow the user to verify and login.


def loggingIn(route):
    @wraps(route)
    def verifyLogin(*args, **kwargs):
        if 'username' in session:
            return route(*args, **kwargs)
        else:
            flash('Login required')
            return redirect(url_for('catalog'))

    return verifyLogin

# This will show the home page.


@app.route('/')
def catalog():
    username = session.get('username')
    cats = sess.query(Category).all()

    recentItems = sess.query(Item).order_by(Item.created.desc()).limit(5).all()

    return render_template('catalog.html', user=username,
                           categories=cats, recentItems=recentItems)

# This will display the categories in JSON.


@app.route('/category/<int:category_id>/json/')
def displayJsonCategoryInfo(category_id):
    category = retrieveCategory(category_id)
    catDict = arrayofCategories(category)
    getjsoncat = make_response(json.dumps(catDict))
    getjsoncat.headers['Content-Type'] = 'application/json'

    return getjsoncat

# This will display the items.


@app.route('/category/<int:category_id>/<int:item_id>/')
def displayItems(category_id, item_id):
    item = retrieveItem(category_id, item_id)
    user = retrieveUserInfo(session.get('email'))

    return render_template('itemDisplay.html', item=item, user=user)

# This will display both categories and items in JSON.


@app.route('/json/')
def allJson():
    categories = sess.query(Category).all()
    cat = dict()
    categoriesArray = []

    for category in categories:
        categoriesArray.append(arrayofCategories(category))

    cat["categories"] = categoriesArray

    getjson = make_response(json.dumps(cat))
    getjson.headers['Content-Type'] = 'application/json'

    return getjson

# This will display the items in JSON.


@app.route('/category/<int:category_id>/<int:item_id>/json/')
def displayJsonItemInfo(category_id, item_id):
    item = retrieveItem(category_id, item_id)
    getjsoni = make_response(json.dumps(arrayofItems(item)))
    getjsoni.headers['Content-Type'] = 'application/json'
    return getjsoni

# This will show the categories


@app.route('/category/<int:category_id>/')
def displayCategories(category_id):
    category = retrieveCategory(category_id)
    return render_template('categoryItems.html', category=category)

# This will allow you to edit the item.


@app.route('/category/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    theuser = retrieveUserInfo(session.get('email'))
    theitem = retrieveItem(category_id, item_id)

    if request.method == 'GET':
        if theuser == theitem.user_id:
            return render_template('editItem.html', item=theitem)
        else:
            return "Please look for the ones you have created."
    elif request.method == 'POST':
        name = request.values.get('name')
        description = request.values.get('description')

        if theuser == theitem.user_id:
            theitem.name = name
            theitem.description = description
            sess.add(theitem)
            sess.commit()

        return redirect(url_for('catalog'))

# This will delete the item.


@app.route('/category/<int:category_id>/<int:item_id>/delete/',
           methods=['POST'])
def deleteItem(category_id, item_id):
    item = retrieveItem(category_id, item_id)
    user = retrieveUserInfo(session.get('email'))

    if user == item.user_id:
        sess.delete(item)
        sess.commit()

        return redirect(url_for('catalog'))
    else:
        return "This is not your item you created"

# This will take and show the Google login.


@app.route('/login/')
def login():
    state = createEvent()
    session['state'] = state

    return render_template('login.html', STATE=state)

# This will retrieve the google login token.


@app.route('/gconnect/', methods=['POST'])
def gconnect():
    oauthT = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={}'
    client_state = request.args.get('state')
    if client_state != session['state']:
        retrievejson = make_response(json.dumps('Invalid state'), 401)
        retrievejson.headers['Content-Type'] = 'application/json'

        return retrievejson
    else:
        id_token = request.data
        id_claims = urllib2.urlopen(
            oauthT.format(id_token)).read()
        id_claims_json = json.loads(id_claims)

        stored_id = session.get('id_token')
        if stored_id == id_token:
            retrievejson = make_response(
                json.dumps('Current user logged in.'), 200)
            retrievejson.headers['Content-Type'] = 'application/json'

            return retrievejson
        else:
            session['id_token'] = id_token
            session['username'] = id_claims_json['name']
            session['email'] = id_claims_json['email']

            if retrieveUserInfo(session['email']):
                print "Existing user."
            else:
                new_user = User(
                    name=session['username'], email=session['email'])
                sess.add(new_user)
                sess.commit()
            return 'Welcome, {}!'.format(session['username'])

# This will log out the user.


@app.route('/gdisconnect/')
def gdisconnect():

    id_token = session.get('id_token')
    if id_token:
        del session['id_token']
        del session['username']
        del session['email']

        return 'Logged out.'
    else:
        return redirect(url_for('catalog'))

# This will create a new item along with showing
# it when logged in.


@app.route('/addItem/', methods=['GET', 'POST'])
@loggingIn
def addItem():

    if request.method == 'GET':
        username = session.get('username')
        categories = sess.query(Category).all()

        return render_template('addItem.html',
                               categories=categories, user=username)
    else:
        category = int(request.values.get('category'))
        name = request.values.get('name')
        user_id = retrieveUserInfo(session.get('email'))
        description = request.values.get('description')
        item = Item(name=name, description=description,
                    category_id=category, user_id=user_id)
        sess.add(item)
        sess.commit()
        return redirect(url_for('catalog'))

# Main for running project.py

if __name__ == '__main__':
    app.secret_key = "falcon pawnch"
    app.run(host='0.0.0.0', port=8080)
