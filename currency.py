import requests
from config import API

def fetch_rates(currencies: list[str]) -> dict:
    api_key = API['key']
    url = API['url']
    headers = {"accept": "application/json"}

    response = requests.get(
        f"{url}?app_id={api_key}&symbols={','.join(currencies)}&prettyprint=false&show_alternative=false",
        headers=headers
    )
    response.raise_for_status()

    return response.json()

def by_currency(symbol: str) -> dict:
    symbol = symbol.upper()
    currencies = API['currencies']
    if symbol not in currencies:
        raise ValueError(f"Currency {symbol} not supported.")

    data = fetch_rates(currencies)
    rates = {}

    if symbol not in data["rates"]:
        raise ValueError(f"Base currency {symbol} not found in exchange rates data.")

    base_rate = data["rates"][symbol]

    for currency, value in data["rates"].items():
        if currency != symbol:
            rates[currency] = {
                f"{currency}_{symbol}": base_rate / value,
                f"{symbol}_{currency}": value / base_rate,
            }
    return rates
