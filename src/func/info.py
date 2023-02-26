import requests, os, logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def get_weather() -> Optional[list]:
    req = "http://api.weatherapi.com/v1/current.json"
    key = os.getenv("WEATHER_API")
    out = requests.get(req, params={
        "key" : key,
        "q": "43.2,76.8"
    })
    try:
        weather_temp_c = out.json()["current"]["temp_c"]
        weather_data = out.json()["current"]["last_updated"].split(" ")
        weather_data = weather_data[0].split("-")[2] + "." + weather_data[0].split("-")[1] + " " + weather_data[1]
        humidity =  out.json()["current"]["humidity"]
        pressure = float(out.json()['current']["pressure_mb"]) * 0.750063755419211
        return [weather_data, weather_temp_c, humidity, int(pressure)] 
    except:
        return None


def get_weather_and_currency() -> Optional[dict]:
    weather_data = get_weather()
    if weather_data is None:
        logging.error("[TOO MANY QUERY TO WEATHER API]")
        return None
    
    currency = []
    headers = {"apikey": os.getenv("CURRENCY_TOKEN")}
    data = requests.get("https://api.apilayer.com/fixer/convert?to=KZT&from=USD&amount=1", headers=headers).json()    
    
    if 'result' not in data:
        logging.error("[TOO MANY QUERY ON API OF MONEY]")
        return None

    currency.append(str(data['result'])[0:6])

    data = requests.get("https://api.apilayer.com/fixer/convert?to=KZT&from=EUR&amount=1", headers=headers).json()
    currency.append(str(data['result'])[0:6])

    # currency = ["412", "123"]

    # return {
    #     "date": date,
    #     "temp": current.temperature.comfort.c,
    #     "humidity": current.humidity.percent,
    #     "pressure": current.pressure.mm_hg_atm,
    #     "currency": currency
    # }

    return {

        "date": weather_data[0],
        "temp": weather_data[1],
        "humidity": weather_data[2],
        "pressure": weather_data[3],
        "currency": currency
    }


# def get_weather_and_currency():
#     return None