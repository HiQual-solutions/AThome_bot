from dotenv import load_dotenv
from flask import Flask, url_for, request
from flask_cors import CORS

from src.db.mongo import db_collection

cleaning = db_collection("cleaning")
cargo = db_collection("cargo")
ren_apartment = db_collection("ren_apartment")
electricity = db_collection("electricity")
painter = db_collection("painter")
security = db_collection("security")
water = db_collection("water")
plumbing = db_collection("plumbing")

app = Flask(__name__)
CORS(app, resources={
    r"/get_list": {"origins": "*"},
    r"/assets/*": {"origins": "*"}
    }) # настройка CORS POLICY
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

#фотка имя телефон ставка 


@app.route("/get_list", methods=['POST'])
def get_list():
    master_type = request.json["type"]
    data = None
    match master_type:
        case "cleaning":
            data = cleaning.get_all_rows({"status" : "active"})
        case "cargo":
            data = cargo.get_all_rows({"status" : "active"})
        case "ren_apartment":
            data = ren_apartment.get_all_rows({"status" : "active"})
        case "electricity":
            data = electricity.get_all_rows({"status" : "active"})
        case "painter":
            data = painter.get_all_rows({"status" : "active"})
        case "security":
            data = security.get_all_rows({"status" : "active"})
        case "water":
            data = water.get_all_rows({"status" : "active"})
        case "plumbing":
            data = plumbing.get_all_rows({"status" : "active"})
    
    if data == []:
        return {}
    
    print(data)

    for i in range(len(data)):
        data[i]["photo"] = "https://engathome.tungulov.space/static/" + data[i]["photo"]
        data[i].pop('_id', None)

    return {
        "data" : data,
    }

@app.route("/img/<img>", methods=['POST'])
def img(img):
    return {
        "photo" : url_for('static', filename=img)
    }

def add_test_data():
    cleaning.add_row({
        "status" : "active",
        "title" : "test",
        "subtitle" : "100",
        "photo" : "test.jpg",
        "tel" : "+79999999999"
    })

def run():
    app.run(host="0.0.0.0", port="5600") # запуск сервераp
