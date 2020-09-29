import requests
import json


class GameExtractor:
    base_url = 'http://www.magetic.com/c/test'
    tries = 20
    no_new_threshold = 20

    def __init__(self, name):
        '''
        :param name: use your name to reach the API or you will have a
        problem like (API error - use ypur name is url &name=[Fname_Lname])
        '''
        self.name = name
        self.no_new_count = 0

    def build_url(self):
        '''
        Build url with your name
        '''
        url = "{}?api=1&name={}".format(self.base_url, self.name)
        return url

    def get_base_games_list(self):
        '''
        Build base array with games
        tries are needed if there is an error in the list instead of games
        :return: list with games
        '''
        url = self.build_url()
        for t in range(self.tries):
            s = requests.get(url)
            if not s.text.startswith('Error 501'):
                games = s.text.split(';')
                return games

    def get_all_games(self):
        '''
        Get all games from API without duplicates
        iterate over the base list, creating a new request with each iteration, and if the new request contains data
        that is not in the base list, we add it
        If the data is in the base list, add +1 to the no_new_count, if a new game is added to the base list,
        then this no_new_count == 0, as soon as the no_new_count == no_new_threshold then iteration ends
        '''

        base_list = self.get_base_games_list()

        url = self.build_url()

        for game in base_list:
            request = requests.get(url)
            data = request.text

            if data.startswith('Error 501'):
                continue

            start_len = len(base_list)
            new_games = set(data.strip().split(';'))

            for new_game in new_games:
                if new_game not in base_list:
                    base_list.append(new_game)
                    self.no_new_count = 0

            updated_len = len(base_list)
            if start_len == updated_len:

                print('No new')
                self.no_new_count += 1
                if self.no_new_count == self.no_new_threshold:
                    break
                continue
        if base_list:
            return self.build_output_json(base_list)
        else:
            return None

    def build_output_json(self, games_list):
        '''
        Output our game_list to json format
        '''
        result = [{"gamename": x, "number": games_list.index(x)} for x in games_list]
        return json.dumps(result)
