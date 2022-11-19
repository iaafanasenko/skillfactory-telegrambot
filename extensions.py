import requests
import json
from config import APIKEY, exchanges


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Невозможно конвертировать одинаковые валюты: {base}.')

        try:
            base_ticker = exchanges[base]
        except KeyError:
            raise APIException(f'Валюта "{base}" не найдена.')

        try:
            quote_ticker = exchanges[quote]
        except KeyError:
            raise APIException(f'Валюта "{quote}" не найдена.')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}.')

        base_ticker, quote_ticker = exchanges[base], exchanges[quote]
        url = f'https://api.apilayer.com/currency_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}'
        response = requests.request('GET', url, headers=APIKEY)
        result = json.loads(response.text)['result']

        return result
