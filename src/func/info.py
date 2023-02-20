import requests, os, logging

from pygismeteo import Gismeteo


gismeteo = Gismeteo()

def get_weather_and_currency():
    search_results = gismeteo.search.by_query("Алматы")
    if len(search_results) <= 0:
        logging.error("[TOO MANY QUERY ON GISMETEO]")
        return None
    
    city_id = search_results[0].id
    current = gismeteo.current.by_id(city_id)

    date = current.date.local[0:10].split("-")
    del date[0]

    currency = []
    
    headers = {"apikey": os.getenv("CURRENCY_TOKEN")}
    
    
    data = requests.get("https://api.apilayer.com/fixer/convert?to=KZT&from=USD&amount=1", headers=headers).json()    
    
    if 'result' not in data:
        logging.error("[TOO MANY QUERY ON API OF MONEY]")
        return None

    currency.append(str(data['result'])[0:6])

    data = requests.get("https://api.apilayer.com/fixer/convert?to=KZT&from=EUR&amount=1", headers=headers).json()
    currency.append(str(data['result'])[0:6])

    return {
        "date": date,
        "temp": current.temperature.comfort.c,
        "humidity": current.humidity.percent,
        "pressure": current.pressure.mm_hg_atm,
        "currency": currency
    }


# def get_weather_and_currency():
#     return None