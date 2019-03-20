from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Setup import Base, MovieGenre, MovieName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///movies.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Movies"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
mbs_ssm = session.query(MovieGenre).all()

# login


@app.route('/login')
def showLogin():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    mbs_ssm = session.query(MovieGenre).all()
    ssmb = session.query(MovieName).all()
    return render_template('login.html',
                           STATE=state, mbs_ssm=mbs_ssm, ssmb=ssmb)
    # return render_template('myhome.html', STATE=state
    # mbs_ssm=mbs_ssm,ssmb=ssmb)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(User1)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

# Home


@app.route('/')
@app.route('/home')
def home():
    mbs_ssm = session.query(MovieGenre).all()
    return render_template('myhome.html', mbs_ssm=mbs_ssm)

# Movie Genres for admins


@app.route('/MovieZone')
def MovieZone():
    try:
        if login_session['username']:
            name = login_session['username']
            mbs_ssm = session.query(MovieGenre).all()
            mbs = session.query(MovieGenre).all()
            ssmb = session.query(MovieName).all()
            return render_template('myhome.html', mbs_ssm=mbs_ssm,
                                   mbs=mbs, ssmb=ssmb, uname=name)
    except:
        return redirect(url_for('showLogin'))

# Showing Movies based on Movie Genres


@app.route('/MovieZone/<int:mbid>/AllMovies')
def showMovies(mbid):
    mbs_ssm = session.query(MovieGenre).all()
    mbs = session.query(MovieGenre).filter_by(id=mbid).one()
    ssmb = session.query(MovieName).filter_by(moviegenreid=mbid).all()
    try:
        if login_session['username']:
            return render_template('showMovies.html', mbs_ssm=mbs_ssm,
                                   mbs=mbs, ssmb=ssmb,
                                   uname=login_session['username'])
    except:
        return render_template('showMovies.html',
                               mbs_ssm=mbs_ssm, mbs=mbs, ssmb=ssmb)

# Add New Movie Genre


@app.route('/MovieZone/addMovieGenre', methods=['POST', 'GET'])
def addMovieGenre():
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        moviegenre = MovieGenre(name=request.form['name'],
                                user_id=login_session['user_id'])
        session.add(moviegenre)
        session.commit()
        return redirect(url_for('MovieZone'))
    else:
        return render_template('addMovieGenre.html', mbs_ssm=mbs_ssm)

# Edit Movie Genre


@app.route('/MovieZone/<int:mbid>/edit', methods=['POST', 'GET'])
def editMovieGenre(mbid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    editMovieGenre = session.query(MovieGenre).filter_by(id=mbid).one()
    creator = getUserInfo(editMovieGenre.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Movie Genre."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('MovieZone'))
    if request.method == "POST":
        if request.form['name']:
            editMovieGenre.name = request.form['name']
        session.add(editMovieGenre)
        session.commit()
        flash("Movie Genre Edited Successfully")
        return redirect(url_for('MovieZone'))
    else:
        # mbs_ssm is global variable we can them in entire application
        return render_template('editMovieGenre.html',
                               mb=editMovieGenre, mbs_ssm=mbs_ssm)

# Delete Movie Genre


@app.route('/MovieZone/<int:mbid>/delete', methods=['POST', 'GET'])
def deleteMovieGenre(mbid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    mb = session.query(MovieGenre).filter_by(id=mbid).one()
    creator = getUserInfo(mb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot  delete this Movie Genre."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('MovieZone'))
    if request.method == "POST":
        session.delete(mb)
        session.commit()
        flash("Movie Genre Deleted Successfully")
        return redirect(url_for('MovieZone'))
    else:
        return render_template('deleteMovieGenre.html', mb=mb, mbs_ssm=mbs_ssm)

# Add New Movie Details


@app.route('/MovieZone/addMovieGenre/addMovie/<string:mbname>/add',
           methods=['GET', 'POST'])
def addMovie(mbname):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    mbs = session.query(MovieGenre).filter_by(name=mbname).one()
    # See if the logged in user is not the owner of MovieGenre
    creator = getUserInfo(mbs.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new Movie"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showMovies', mbid=mbs.id))
    if request.method == 'POST':
        poster = request.form['poster']
        name = request.form['name']
        year = request.form['year']
        rating = request.form['rating']
        budget = request.form['budget']
        gross = request.form['gross']
        moviedetails = MovieName(poster=poster, name=name,
                                 year=year, rating=rating,
                                 budget=budget,
                                 gross=gross,
                                 date=datetime.datetime.now(),
                                 moviegenreid=mbs.id,
                                 user_id=login_session['user_id'])
        session.add(moviedetails)
        session.commit()
        return redirect(url_for('showMovies', mbid=mbs.id))
    else:
        return render_template('addMovie.html',
                               mbname=mbs.name, mbs_ssm=mbs_ssm)

# Edit Movie Details


@app.route('/MovieZone/<int:mbid>/<string:ssmname>/edit',
           methods=['GET', 'POST'])
def editMovie(mbid, ssmname):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    mb = session.query(MovieGenre).filter_by(id=mbid).one()
    moviedetails = session.query(MovieName).filter_by(name=ssmname).one()
    # See if the logged in user is not the owner of MovieGenre
    creator = getUserInfo(mb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this Movie"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showMovies', mbid=mb.id))
    # POST methods
    if request.method == 'POST':
        moviedetails.poster = request.form['poster']
        moviedetails.name = request.form['name']
        moviedetails.year = request.form['year']
        moviedetails.rating = request.form['rating']
        moviedetails.budget = request.form['budget']
        moviedetails.gross = request.form['gross']
        moviedetails.date = datetime.datetime.now()
        session.add(moviedetails)
        session.commit()
        flash("Movie Edited Successfully")
        return redirect(url_for('showMovies', mbid=mbid))
    else:
        return render_template('editMovie.html',
                               mbid=mbid, moviedetails=moviedetails,
                               mbs_ssm=mbs_ssm)

# Delete Movie Details


@app.route('/MovieZone/<int:mbid>/<string:ssmname>/delete',
           methods=['GET', 'POST'])
def deleteMovie(mbid, ssmname):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    mb = session.query(MovieGenre).filter_by(id=mbid).one()
    moviedetails = session.query(MovieName).filter_by(name=ssmname).one()
    # See if the logged in user is not the owner of MovieGenre
    creator = getUserInfo(mb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this Movie"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showMovies', mbid=mb.id))
    if request.method == "POST":
        session.delete(moviedetails)
        session.commit()
        flash("Deleted Movie Successfully")
        return redirect(url_for('showMovies', mbid=mbid))
    else:
        return render_template('deleteMovie.html',
                               mbid=mbid, moviedetails=moviedetails,
                               mbs_ssm=mbs_ssm)

# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'}
                  )[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully'
                                            'disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Json
# Show all Movies along with Movie Genres


@app.route('/MovieZone/JSON')
def allMoviesJSON():
    moviegenre_names = session.query(MovieGenre).all()
    category_dict = [c.serialize for c in moviegenre_names]
    for c in range(len(category_dict)):
        movies = [i.serialize for i in session.query(
                MovieName).
                filter_by(moviegenreid=category_dict[c]["id"]).all()]
        if movies:
            category_dict[c]["moviesgenres"] = movies
    return jsonify(MovieGenre=category_dict)

# Show all Movie Genres


@app.route('/movieZone/movieGenre/JSON')
def categoriesJSON():
    moviegenres = session.query(MovieGenre).all()
    return jsonify(moviegenre_Name=[c.serialize for c in moviegenres])

# Show all Movies


@app.route('/movieZone/moviegenres/JSON')
def itemsJSON():
    items = session.query(MovieName).all()
    return jsonify(moviegenres=[i.serialize for i in items])

# Show the Movies present in a particular Movie Genre


@app.route('/MovieZone/<path:moviegenre>/moviegenres/JSON')
def categoryItemsJSON(moviegenre):
    movieGenre = session.query(
                           MovieGenre).filter_by(name=moviegenre).one()
    moviegenres = session.query(
                           MovieName).filter_by(moviegenre=movieGenre).all()
    return jsonify(movieGenre=[i.serialize for i in moviegenres])

# Show the details of particular movie in a particular Movie Genre


@app.route('/MovieZone/<path:moviegenre>/<path:movieitem_name>/JSON')
def ItemJSON(moviegenre, movieitem_name):
    movieGenre = session.query(MovieGenre).filter_by(name=moviegenre).one()
    movieItemName = session.query(MovieName).filter_by(
           name=movieitem_name, moviegenre=movieGenre).one()
    return jsonify(movieItemName=[movieItemName.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
