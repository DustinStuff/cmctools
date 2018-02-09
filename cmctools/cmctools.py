import requests


class CMCTools:

    def __init__(self):
        self.TICKER_URL = "https://api.coinmarketcap.com/v1/ticker/"
        self.GLOBAL_URL = "https://api.coinmarketcap.com/v1/global/"
        self.coin_name_info_list = []

        self.headers = { "User-agent": "cmcools - A lightweight coinmarketcap wrapper. https://github.com/DustinStuff/cmctools" }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def ticker(self, coin_id="", limit="", start="", convert=""):
        """
        Gets information from the coinmarketcap API's ticker endpoint. Only valid coinmarketcap coin IDs can
        be used, however you can use a symbol or name if you pass it through name_info([symbol or name])['id'].

        Example return JSON:
        [
            {
                "id": "bitcoin",
                "name": "Bitcoin",
                "symbol": "BTC",
                "rank": "1",
                "price_usd": "8026.4",
                "price_btc": "1.0",
                "24h_volume_usd": "8925990000.0",
                "market_cap_usd": "135277547580",
                "available_supply": "16854075.0",
                "total_supply": "16854075.0",
                "max_supply": "21000000.0",
                "percent_change_1h": "-0.53",
                "percent_change_24h": "-0.73",
                "percent_change_7d": "-7.88",
                "last_updated": "1518151167"
        If convert is used, it also has these entries (using ETH as an example):
                "price_eth": "10.0965816895",
                "24h_volume_eth": "11228195.3546",
                "market_cap_eth": "170168545.0"
            },
            { ... }
        ]
        :param coin_id: A valid coinmarketcap coin id.
        :param limit: Returns a maximum of [limit] results. Defaults to 100, use 0 to return all results.
        :param start: Returns results from rank [start].
        :param convert: Returns price, 24h volume, and market cap in another specified currency.
        :return: /ticker/endpoint JSON data.
        """
        url = "{}{}/".format(self.TICKER_URL, coin_id) if coin_id else self.TICKER_URL
        params = {"limit": limit, "start": start, "convert": convert}
        return self.session.get(url, params=params).json()

    def global_data(self, convert=""):
        """
        Gets information from the coinmarketcap API's global endpoint.

        Example JSON output:
        {
            "total_market_cap_usd": 383330297293.0,
            "total_24h_volume_usd": 24300271821.0,
            "bitcoin_percentage_of_market_cap": 35.07,
            "active_currencies": 888,
            "active_assets": 593,
            "active_markets": 8641,
            "last_updated": 1518152066
        }
        :param convert: Returns price, 24h volume, and market cap in another specified currency
        :return: /global/ endpoint JSON data
        """
        params = {}
        if convert:
            params["convert"] = self.name_info(convert)["symbol"]
        url = self.GLOBAL_URL
        r = self.session.get(url, params=params)
        return r.json()

    def name_info(self, coin_input):
        """
        Takes a coinmarketcap ID, name, or symbol, and returns a dict containing all of that information.

        Example output:
        {
            "id": "bitcoin-cash",
            "name": "Bitcoin Cash",
            "symbol": "BCH"
        }
        :param coin_input: A valid ID, name, or symbol
        :return: Dict
        """
        if not self.coin_name_info_list:
            self._create_name_info_cache()
        coin_input = str(coin_input).lower()
        for coin in self.coin_name_info_list:
            if coin['id'].lower() == coin_input \
                    or coin['name'].lower() == coin_input \
                    or coin['symbol'].lower() == coin_input:
                return coin
        return {"error": "id not found for input \"{}\"".format(coin_input)}

    def _create_name_info_cache(self):
        """
        Creates a cache of all coinmarketcap IDs, names, and symbols so we don't have to keep hitting the API.
        :return: N/A
        """
        params = {"limit": 0} # Get all listings
        coin_list = self.session.get(self.TICKER_URL, params=params).json()
        for coin in coin_list:
            self.coin_name_info_list.append({
               "id": coin["id"],
               "name": coin["name"],
               "symbol": coin["symbol"]
            })