import dramatiq, os, logging
from src.db.mongo import db_collection
from src.func.info import get_weather_and_currency
from datetime import datetime

Data_menu = db_collection("Data_menu")


@dramatiq.actor
def get_all_dramatiq():

    data = get_weather_and_currency()
    if data is not None: # if data is empty 
        logging.error("[TOO MANY QUERY]")
        data["period"] = int(datetime.now().timestamp())
        Data_menu.add_row(data)

        get_all_dramatiq.send_with_options(delay = 360000)
        return
    
    get_all_dramatiq.send_with_options(delay = int(os.getenv("TIME_IF_NO_DATA")))
        