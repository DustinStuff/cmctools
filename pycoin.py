import requests
from pprint import pprint


class CMCTools:

    def __init__(self):
        self.URL = "https://api.coinmarketcap.com/v1/ticker/"
        self.coin_name_info_list = []
        self.coin_id = ""

    def ticker(self, coin_id="", limit="", convert=""):

        params = {"limit": limit, "convert": convert}

        return requests.get(self.URL, params).json()

    def get_name_info(self, coin_input):
        """ Takes a coinmarketcap ID, name, or symbol, and returns a dict containing all of that information"""

        if not self.coin_name_info_list:
            self._create_name_info_cache()

        coin_input = str(coin_input).lower()

        for coin in self.coin_name_info_list:
            if coin['id'].lower() == coin_input or coin['name'].lower() == coin_input or coin['symbol'].lower() == coin_input:
                return coin

        raise ValueError("Could not find a valid id, name, or symbol associated with \"{}\"".format(coin_input))

    def _create_name_info_cache(self):

        params = {"limit": 0}
        coin_list = requests.get(self.URL, params).json()

        # Make cache
        for coin in coin_list:
            self.coin_name_info_list.append({
                "id": coin["id"],
                 "name": coin["name"],
                "symbol": coin["symbol"]
             })


c = CMCTools()
coin = c.get_name_info("btc")["id"]
alt = c.get_name_info("eth")["id"]

print(c.ticker(coin, convert=alt))