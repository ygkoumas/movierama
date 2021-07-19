import re
from flask import Flask, render_template, make_response, request, redirect, escape
from util.login import validate_user, create_token, validate_token, register_user
from data.movies import Movies
from data.movie_votes import MovieVotes
import util.movies as um
from datetime import date


app = Flask(__name__, template_folder="templates")


def get_username(cookies):
    return validate_token(cookies.get('token') or '')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if get_username(request.cookies):
        return make_response(redirect('/', '303'))

    if request.method == 'GET':
        return render_template('login.html', error='')

    username = escape(request.form['username'])
    if validate_user(username,
                     request.form['password']):
        token = create_token(username)
        resp = make_response(redirect('/', '303'))
        resp.set_cookie('token', token, samesite="None", secure=True)

        return resp

    return render_template('login.html', error='Invalid username or password')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if get_username(request.cookies):
        return make_response(redirect('/', '303'))

    if request.method == 'GET':
        return render_template('signup.html', error='')

    username = escape(request.form['username'])
    if register_user(username,
                     request.form['password']):
        token = create_token(username)
        resp = make_response(redirect('/', '303'))
        resp.set_cookie('token', token, samesite="None", secure=True)

        return resp

    return render_template('signup.html', error='Username already in use')


@app.route('/', methods=['GET', 'POST'])
def show_movies():
    username = get_username(request.cookies)
    rf = request.form
    if 'like' in rf:
        MovieVotes.vote_like(rf['like'], username)
    elif 'hate' in rf:
        MovieVotes.vote_hate(rf['hate'], username)
    elif 'unvote' in rf:
        MovieVotes.remove_vote(rf['unvote'], username)

    sort_by = request.args.get('sortby')
    filter_by = request.args.get('filterby')

    likes = MovieVotes.get_likes()
    hates = MovieVotes.get_hates()

    if filter_by is not None:
        movies = Movies.get_movies_filtered_by_user(filter_by)
    elif sort_by == 'hates':
        movies = um.get_movies_sorted_by_hates()
    elif sort_by == 'likes':
        movies = um.get_movies_sorted_by_likes()
    else:
        movies = Movies.get_movies_sorted_by_date()

    return render_template('movies.html', movies=movies,
                           username=username or '', likes=likes, hates=hates)


@app.route('/add-movie', methods=['GET', 'POST'])
def add_movie():
    username = get_username(request.cookies)
    if not username:
        return make_response(redirect('/', '303'))

    if request.method == 'GET':
        return render_template('add_movie.html')

    rf = request.form
    Movies.add_movie(
        title=escape(rf['title']),
        description=escape(rf['description']),
        date=date.today().strftime("%d/%m/%Y"),
        username=username
    )

    return make_response(redirect('/', '303'))
