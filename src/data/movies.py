import pandas as pd
MOVIES_FILE = 'data/app_data/movies.csv'


class MoviesClass:
    def __init__(self, movies_file):
        self.movies_file = movies_file
        self.__fetch_movies()

    def __fetch_movies(self):
        self.parsed_movies = pd.read_csv(MOVIES_FILE, dtype='string')
        self.parsed_movies.reset_index(level=0, inplace=True)
        self.parsed_movies.rename({'index': 'id'}, axis=1, inplace=True)
        self.movies = self.parsed_movies.applymap(str)

    def add_movie(self, title, description, date, username):
        with open(MOVIES_FILE, "a+") as mf:
            mf.write("\n")
            mf.write(f"{title},{description},{date},{username}")
        self.__fetch_movies()

    def get_movies(self):
        movies = self.movies.sort_values('id', ascending=True)
        return [movie for _, movie in movies.iterrows()]

    def get_movies_sorted_by_date(self):
        movies = self.movies.sort_values('id', ascending=False)
        return [movie for _, movie in movies.iterrows()]

    def get_movies_filtered_by_user(self, username):
        movies = self.movies.query(f'username == "{username}"')
        return [movie for _, movie in movies.iterrows()]


Movies = MoviesClass(MOVIES_FILE)
