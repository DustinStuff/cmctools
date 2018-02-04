import requests


TICKER_URL = "https://api.coinmarketcap.com/v1/ticker/"
GLOBAL_URL = "https://api.coinmarketcap.com/v1/global/"
coin_name_info_list = []


def ticker(coin_id="", limit="", start="", convert=""):
    url = "{}{}/".format(TICKER_URL, coin_id) if coin_id else TICKER_URL
    params = {"limit": limit, "start": start, "convert": convert}
    return requests.get(TICKER_URL, params).json()


def global_data(convert=""):
    params = {}
    if convert:
        params["convert"] = name_info(convert)["symbol"]
    url = GLOBAL_URL
    r = requests.get(url, params)
    return r.json()


def name_info(coin_input):
    """Takes a coinmarketcap ID, name, or symbol, and returns a dict containing all of that information"""
    if not coin_name_info_list:
        _create_name_info_cache()
    coin_input = str(coin_input).lower()
    for coin in coin_name_info_list:
        if coin['id'].lower() == coin_input or coin['name'].lower() == coin_input or coin['symbol'].lower() == coin_input:
            return coin
    return {"error": "id not found for input \"{}\"".format(coin_input)}


def _create_name_info_cache():
    params = {"limit": 0}
    coin_list = requests.get(TICKER_URL, params).json()
    for coin in coin_list:
        coin_name_info_list.append({
            "id": coin["id"],
            "name": coin["name"],
            "symbol": coin["symbol"]
        })