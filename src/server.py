from dotenv import load_dotenv
import logging
from flask import Flask, url_for, request
from flask_cors import CORS
from src.db.mongo import db_collection
from admin_panel import admins

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
logging.basicConfig(level=logging.INFO)
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
        return []
    
    for i in range(len(data)):
        # data[i]["photo"] = "https://engathome.tungulov.space/static/" + data[i]["photo"]
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
    # cleaning.add_row({
    #     "status" : "active",
    #     "title" : "test",
    #     "subtitle" : "100",
    #     "photo" : "test.jpg",
    #     "tel" : "+79999999999"
    # })

    # cleaning.drop_collection()
    # cargo.drop_collection()
    # ren_apartment.drop_collection()
    # electricity.drop_collection()
    # painter.drop_collection()
    # security.drop_collection()
    # water.drop_collection()
    # plumbing.drop_collection()

    admins.add_row({
        "adminID": 170798045,
        "status": "active",
    })

    # plumbing.create_link([ # clening data
    #     ["Юрий Ступченко", "https://naimi.kz/specialist/425361?work_id=120#/", "https://upload.naimi.kz/picture/thumbnail/qSJ78AsEQNHZCdQ3Rn6G66rEZPqHR7TUuWh"],
    #     ["Иван Нестеренко", "https://naimi.kz/specialist/464880?work_id=120#/", "https://upload.naimi.kz/picture/thumbnail/qRJ23mLnF6UiJTBuRMx9iqj8eqvVLESCfZBpuNYTWViTcGJPkBB6kHIlQhOYi6qb31xRJn7jLID9aIAwGX4sbpUNfE2onacAalFLf1s1w"],
    #     ["Дилмурат Амирдинов", "https://naimi.kz/specialist/127241?work_id=120#/", "https://upload.naimi.kz/picture/thumbnail/gR3ndxFT1Eyndf2cAM7ixLO1oj1og3ynUxGfbNEj70mjdHzxziXk4v1P64QTCN80MapPh2Crd5ngw2Nhz8vh35uCdHAVLlHqPer4M72dH73VrGBjBaMh4UihfOi5tLP6z1tE9ib92CAvk63c4jxP11yIfYo"],
    #     ["Бахтияр Валиев", "https://naimi.kz/specialist/159839?work_id=812#/", "https://upload.naimi.kz/picture/thumbnail/1YDZptOJ15iZgT0"],
    #     ["Роман Жук", "https://naimi.kz/specialist/13483?work_id=812#/", "https://upload.naimi.kz/picture/thumbnail/1YDZpO4Z0kTybDS"],
    #     ["CАНТЕХНИК АЛМАТЫ", "https://eco-service.kz/santehnik/", "https://eco-service.kz/wp-content/uploads/%D0%A1%D0%90%D0%9D%D0%A2%D0%95%D0%A5%D0%9D%D0%98%D0%9A2.jpg"],
    #     ["Алматехник", "https://almatehnic.kz/vizov-santehnika-almaty ", "https://i0.wp.com/almatehnic.kz/wp-content/uploads/2023/02/final_logo_2018.png?w=500&ssl=1"],
    #     ["Сантех Эксперт", "https://santeh-expert.kz/kontakty/", "https://santeh-expert.kz/wp-content/themes/custom/images/header-logo.png"],
    # ])


    # electricity.create_link([ # electricity
    #     ["Нурсултан Чалгынбаев", "https://naimi.kz/specialist/16299?work_id=187#/", "https://upload.naimi.kz/picture/thumbnail/1YDZpurMHrnlHY9"],
    #     ["Дмитрий Баркалов", "https://naimi.kz/specialist/47953?work_id=187#/", "https://upload.naimi.kz/picture/thumbnail/1YDZpfl3aU7ShvK"],
    #     ["Бауыржан Турсынов", "https://naimi.kz/specialist/43932?work_id=187#/", "https://upload.naimi.kz/picture/thumbnail/qSJ7860co2b4lZYuvzAlNoNcWY5QXNHp2oI"],
    #     ["Самат Оралханов", "https://naimi.kz/specialist/531179?work_id=187#/", "https://upload.naimi.kz/picture/thumbnail/qRJ23iooSX5bSQVXTUUOOUx8zCMctQS8X7krsBIttg1HoaQD8S9WJqa9JTaMeAaZHmK9pTt3YC6xNx4HlcpsRDGNQ5s4guM8wgKZ9n39o"],
    #     ["Бекзат Бателханов", "https://naimi.kz/specialist/158456?work_id=187#/", "https://upload.naimi.kz/picture/thumbnail/qSJ78nrKkAptzNqhO9n18E0gdBakTas8NgT"],
    #     ["ЭЛЕКТРИК АЛМАТЫ", "https://eco-service.kz/elektrik/", "https://eco-service.kz/wp-content/uploads/electric-2-3-569x600.jpg"],
    #     ["Electro Uslugi", "https://electrouslugi.kz/index.php?view=contacts", "https://electrouslugi.kz/images/logo.png"],
    #     ["ЭЛЕКТРИК В АЛМАТЕ", "http://1electrik.kz/", "http://1electrik.kz/logo2.png"],
    # ])

    # cleaning.create_link([
    #     ["Еркежан Амиржан", "https://naimi.kz/specialist/374094?work_id=134#/", "https://upload.naimi.kz/picture/thumbnail/qRJ23PSVzklmrF8Q9XjtjTq5of1Rky9LQmZdgGoZyTgWBFnxiUt6Lx2GRj2h5E4bhn5DlxUnRWGl6iob2qyEN7lljnYKMR3U8PxsFZn9H"],
    #     ["Акмарал Изембаева", "https://naimi.kz/specialist/259558?work_id=134#/", "https://upload.naimi.kz/picture/thumbnail/gR3nd7M2LO8NIVpwOYTUB3RdmXpWf6qTvI1ScIspyxEPasNDPbjZzAHLQjOLbwEH47Vr4POuqEeLLF6sERiK5auAjbOo8uW3jelQSlp2xv51aUH10q9iZKqNLztVUW8slanmyP9EyQpa6jDj1w2h70ieol1"],
    #     ["Снежанна Линькова", "https://naimi.kz/specialist/254912?work_id=134#/", "https://upload.naimi.kz/picture/thumbnail/qRJ23gPYiMUg3aNmG27kB0W8jGqbtrohQm8OLquZrQdemROvq6q4ZT0SS1CiumwjQexVr6ZR7aev8sheFNFtF6mSoRc8ByJAWxHCqiSJ3"],
    #     ["Арай Абдолда", "https://naimi.kz/specialist/550308?work_id=134#/", "https://upload.naimi.kz/picture/thumbnail/qRJ23uL12G93yaulnQsV7LtFBVPxVcjwMAGlLiuZIxtkdXlN6KOUqA70MMbBDVhFRwgYetX0UTILebpbj90SOhjdfgeXtbzMPjFS8ypAn"],
    #     ["Аида Наурызбаева", "https://naimi.kz/specialist/435820?work_id=134#/", "https://upload.naimi.kz/picture/thumbnail/qSJ78gj8W3z5vXTJjWJetFgNXIEa81MzO8C"],
    #     ["Alma Clean", "https://almaclean.kz/", "https://almaclean.kz/images/logo.svg"],
    #     ["Cleaning Home", "https://cleaninghome.kz/", "https://cleaninghome.kz/wp-content/uploads/2021/02/%D0%9B%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF-%D0%BA%D0%BE%D1%80%D0%BE%D0%BD%D0%B0-%D1%81-%D0%BD%D0%B0%D0%B4%D0%BF%D0%B8%D1%81%D1%8C%D1%8E.jpg"],
    #     ["Top", "https://top.kz/", "https://top.kz/images/logo.svg"],
    #     ["AST-DEZ", "https://dezsluzhba.kz/?utm_source=google_search_almaty&utm_medium=cpc&utm_campaign=dz_desktop&utm_term=%D0%B4%D0%B5%D0%B7%D0%B8%D0%BD%D1%84%D0%B5%D0%BA%D1%86%D0%B8%D1%8F%20%D0%B0%D0%BB%D0%BC%D0%B0%D1%82%D1%8B&gclid=Cj0KCQiAk4aOBhCTARIsAFWFP9HVjK9XywGGx5Ox1jLNmpHvGJU5FIGMwbwDa252SRCAhX18ZGeJ2X0aAqM6EALw_wcB#2", ""],
    #     ["ДезГарант", "https://dezgarant.kz/", ""],
    #     ["DST", "https://ds.dstrade.kz/?utm_source=google-ads&utm_medium=cpc&utm_campaign=%D0%94%D0%B5%D0%B7%D0%B8%D0%BD%D1%84%D0%B5%D0%BA%D1%86%D0%B8%D1%8F_New&utm_content=120851665376-512442646978-&utm_term=%D0%B4%D0%B5%D0%B7%D0%B8%D0%BD%D1%84%D0%B5%D0%BA%D1%86%D0%B8%D1%8F%20%D0%B0%D0%BB%D0%BC%D0%B0%D1%82%D1%8B-p", ""],
    #     ["Aatomy", "https://www.aatomy.kz/?gclid=Cj0KCQiAk4aOBhCTARIsAFWFP9GriZNo-YvNyoXe5QGgFCKoDACnuj-KBYKtje4467uyBNYewUkxu1UaArgJEALw_wcB", ""],
    #     ["Белоснежнка", "https://himchistka-almaty.kz/", ""],
    #     ["Grand Clean", "https://grandclean.kz/", ""],
    #     ["Eco Dry", "http://www.ecodry.kz/", ""],
    #     ["Панда", "http://himpanda.kz/adresa-i-kontakty/", ""]
    # ])

    # painter.create_link([
    #     ["Умит Мустафаева", "https://naimi.kz/specialist/260602?work_id=178#/", "Умит Мустафаева"],
    #     ["Жибек Бажан", "https://naimi.kz/specialist/69360?work_id=178#/", "https://upload.naimi.kz/picture/thumbnail/1YDZpRFwzBr9TJL"],
    #     ["Мухтар Сулейменов", "https://naimi.kz/specialist/28131?work_id=178#/", "https://upload.naimi.kz/picture/thumbnail/qRJ23czaKIp9NHI0VAGfXSYA5oqE2sN0oThr81ehPh7XcTmVGmrpeXAF6jNtEthMINvTzNAKZFtWeAV11UtX51cM1xGztadx1Q4jNwNmv"],
    #     ["Диас Бахтиаров", "https://naimi.kz/specialist/118575?work_id=178#/", "https://upload.naimi.kz/picture/thumbnail/qRJ23gIfMiXwo5y3ArW1poUqwKG1zUc7lPA6Nh0mMFTqNLk47edhEozzl3MNvp98CwYCIDWsSJKGam5qJmqCnCezwT6ig4CEyFR9nbLc4"],
    #     ["Бауыржан Дощанов", "https://naimi.kz/specialist/163729?work_id=178#/", "https://upload.naimi.kz/picture/thumbnail/gR3ndYYwdvjCTHerJ7u0w8ZyRsMP583Ezbino7VYxZB2vffIMTUtXmj2THcPXKZYVfcsZJWslPmnfkQVRIJXDp3fQYlkdcXlt2gaypLBKzGmK4k0HKY0xwq9dhVTWmUsuzp1OW7rMq3pVctW6p5F3z9keh9"],
    #     ["Серик Джумашпаев", "https://naimi.kz/specialist/48327?work_id=185#/", "https://upload.naimi.kz/picture/thumbnail/gR3nd1t9v782exD79vBnJqjk5BcTHLAfzXjmXiKiqWGkkcGnXvI8pghaxoxU1juLHWR7H4F5A8kBhRnIdzhHWUWyShDWGtuhpgiR6jNg0UhITSnT1kSVc94QrwY2iDtmT6SNglD1uW9ujpvRpnTx498JbFi"],
    #     ["Mega Master", "https://almaty.megamaster.kz/tag/uslugi-shtukatura", "https://images.megamaster.kz/4d4b1d4c-4785-4569-8549-e862b93427fe.png"],
    #     ["ПРОФИ", "https://alm.profi.kz/remont/malyarnye-shtukaturnye-raboty/", "https://alm.profi.kz/_next/static/media/logo_red.9501ac31.svg"],
    # ])

    # security.create_link([
    #     ["СОП «Күзет»", "https://aokuzet.kz/service/homesecurity/?utm_source=adwords_poisk_almaty&utm_campaign=ohrana_kvartiry_2&utm_term=%2B%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%B0%20%2B%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%8B%20%2B%D0%B0%D0%BB%D0%BC%D0%B0%D1%82%D1%8B&gclid=Cj0KCQiAk4aOBhCTARIsAFWFP9FzQ-ZMLqzk6mqmJv441NJ8txNn8AGYiPZNtJzSCrgAQRJzXVTtecAaAgJJEALw_wcB", ""],
    #     ["Пультовая охрана", "https://quzet.kz/?gclid=Cj0KCQiAk4aOBhCTARIsAFWFP9HkFkwIV6XEj1YNjrHZiQB--hfIk_3cRwSbbjwJ6EXWYOjvvfS4NnYaArCwEALw_wcB", ""],
    #     ["Kaz-Kuzet", "https://kaz-kuzet.kz/?utm_source=google&utm_medium=cpc&utm_term=%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%20%D0%B0%D0%BB%D0%BC%D0%B0%D1%82%D1%8B&utm_content=502262418185&utm_campaign=gl-search&gclid=Cj0KCQiAk4aOBhCTARIsAFWFP9GbmgJeVRnKSw_rv19HJvWJgPOltMBrzeYONMJrPiN4KwhFj4xStIEaAkXVEALw_wcB", ""],
    #     ["security.kz", "https://mtz.security.kz/ru/domofon/?gclid=Cj0KCQiAk4aOBhCTARIsAFWFP9H6mthEuBonlSpDaz226WPC8UEoIHzsGBtDNjqa9AQPvJQZ_5uEHj8aAmYKEALw_wcB", ""],
    #     ["FASL", "https://fasl.satu.kz/contacts", ""],
    #     ["AtlantSecurity.kz", "https://atlantsecurity.kz/", ""],
    #     ["Eco Service", "https://eco-service.kz/domofon/", ""]
    # ])

    # ren_apartment.create_link([
    #     ["ACG", "https://adiletgroup.kz/", ""],
    #     ["AINN", "https://www.ainn.kz/", ""],
    #     ["Aztec", "https://otdelka-almaty.kz/remont-kvartir-v-almaty.html", ""],
    #     ["Идеал ремонт", "https://ideal-remont.kz/", ""],
    #     ["Barsha.kz", "https://barsha.kz/remont-kvartir-almaty", ""]
    # ])

    # water.create_link([
    #     ["Комета", "https://calipso-water.kz/kontakty/", ""],
    #     ["Samal Water", "https://samal.kz/product-category/voda/", ""],
    #     ["Oasis water", "https://oasiswater.kz/index.php", ""],
    # ])

    # cargo.create_link([
    #     ["KL Logistic", "https://kl-logistic.kz/?utm_source=google-ads&utm_medium=cpc&utm_campaign=10833704063&utm_content=112267036448-456560684579-&utm_term=%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B7%D0%BA%D0%B0%20%D0%B3%D1%80%D1%83%D0%B7%D0%BE%D0%B2-e", ""],
    #     ["FARTLOGISTIC", "https://fartlogistic.kz/?gclid=Cj0KCQiAk4aOBhCTARIsAFWFP9Hojj1ASSGoVrzxSLDrVGJDlFEAKKqtbfQMQ4bwAwxJgL9DChupP4EaAkpeEALw_wcB", ""]
    # ])


def run():
    app.run(host="0.0.0.0", port="5600") # запуск сервераp
