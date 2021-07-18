from data.movies import Movies
from data.movie_votes import MovieVotes


def get_movies_sorted_by_hates():
    hates = MovieVotes.get_hates()
    movies = Movies.get_movies()
    movies.sort(
        reverse=True,
        key=lambda movie: len(hates[movie['id']]) if movie['id'] in hates else 0
    )
    return movies


def get_movies_sorted_by_likes():
    likes = MovieVotes.get_likes()
    movies = Movies.get_movies()
    movies.sort(
        reverse=True,
        key=lambda movie: len(likes[movie['id']]) if movie['id'] in likes else 0
    )
    return movies
