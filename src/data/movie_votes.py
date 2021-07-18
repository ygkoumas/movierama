import pandas as pd
MOVIE_VOTES_FILE = 'data/app_data/movie_votes.csv'


class MovieVotesClass:
    def __init__(self, votes_file):
        self.votes_file = votes_file
        self.__fetch_votes()


    def __fetch_votes(self):
        self.likes = dict()
        self.hates = dict()
        self.parsed_votes = pd.read_csv(self.votes_file, dtype = 'string')
        for _, ml in self.parsed_votes.iterrows():
            movie_id = ml['movie_id']
            username = ml['username']
            like = ml['like']
            hate = ml['hate']
            if like == 'true':
                if movie_id not in self.likes:
                    self.likes[movie_id] = set()
                self.likes[movie_id].add(username)
            elif hate == 'true':
                if movie_id not in self.hates:
                    self.hates[movie_id] = set()
                self.hates[movie_id].add(username)


    def __save_votes(self):
        self.parsed_votes.to_csv(self.votes_file, index=False)


    def __remove_vote(self, movie_id, username):
        print(self.parsed_votes)
        res1 = self.parsed_votes.query(f'movie_id == "{movie_id}"')
        print(res1)
        res2 = res1.query(f' username == "{username}"')
        print(res2)
        index=res2.index
        print(index)
        self.parsed_votes.drop(index, inplace=True)      


    def vote_like(self, movie_id, username):
        self.__remove_vote(movie_id, username)
        self.parsed_votes.loc[len(self.parsed_votes.index)] = [movie_id, username, 'true', 'false'] 
        self.__save_votes()
        self.__fetch_votes()


    def vote_hate(self, movie_id, username):
        self.__remove_vote(movie_id, username)
        self.parsed_votes.loc[len(self.parsed_votes.index)] = [movie_id, username, 'false', 'true'] 
        self.__save_votes()
        self.__fetch_votes()


    def remove_vote(self, movie_id, username):
        self.__remove_vote(movie_id, username)
        self.__save_votes()
        self.__fetch_votes()


    def get_likes(self):
        return self.likes


    def get_hates(self):
        return self.hates


MovieVotes = MovieVotesClass(MOVIE_VOTES_FILE)