#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask import request
import requests
from influxdb import InfluxDBClient
import mysql.connector
from flask_cors import CORS
import re

# Коннект к БД
# Датчики кладут данные раз в секунду
clientdb = InfluxDBClient(host='pmelikov.ru', port='46306')

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# Тариф за электроэнергию (задается в приложении)
CONFIG = {
    "tariff": 4.36
}


# Список фич (наброски):

# Предсказательная информация ( ты сейчас тратишь столько то, если будешь тратить столько же то к концу месяца получится вот такой счет)
# Калькулятор ( вот столько плачу за энергию, если я хочу потратить за месяц столько денег, то сколько всего кВт будет и сколько кВт на день)
# Советы по приборам (Прибор подключенный к этой розетке тратит больше всего энергии в сутки,неделю, месяц)
# Графики по розеткам (В мобилке отображать сводный график по всем приборам подключенным)
# Можем собирать с разных розеток
# Возможно добавить любую умную розетку


@app.route('/')
def index():
    return "Тут API лежит"


# Отдает текущее потребление (Кв*ч) по каждому устройству
"""
Пример результата

{
    "Android": 0.5832376890267379,
    "FAN": 0.5832376890267379,
    "Fridge": 1.4455796820473148,
    "Heater": 0.5832376890267379,
    "Light": 0.583262218774227,
    "TV": 1.4455796820473148,
    "TeslaPowerWall": 1.4455796820473148,
    "Xiaomi": 1.4455796820473148
}
"""


@app.route('/get_current_by_devices')
def get_current_by_devices():
    result = clientdb.query(
        "SELECT mean(\"value\") FROM \"kvartira1\" WHERE time > now() - 1h AND (\"mesurement\" = \'kilowatt\' AND \"sensor_id\" <> \'main\')  GROUP BY \"sensor_id\"").raw
    vals = dict()
    for i in result['series']:
        vals[i['tags']['sensor_id']] = i['values'][0][1]
    return vals


"""
Получение общего потребления в час\день\месяц
http://АДРЕС_СЕРВЕРА/get_current_total?type=<type>
Принимает параметр: type
Возможные значения: hour, day, mounth
Результат:
{"total":1.8967232110091705,"total_price":8.269713199999984}
total -- количество потраченных кВт
total_price -- набежавшая сумма за эти кВт
"""


@app.route('/get_current_total')
def get_current_data():
    type = request.args.get("type")
    count_hour = 1
    if type:
        if type == 'day':
            count_hour = 24
        if type == 'mounth':
            count_hour = 24 * 30
    result = clientdb.query('SELECT mean("value") FROM "kvartira1"')
    points = result.get_points()
    total_kwt = 0
    for point in points:
        total_kwt += point["mean"]
    total_price = total_kwt * CONFIG["tariff"]
    return {"total": round(total_kwt, 1), "total_price": round(total_price, 1)}


# Возмращает данные для диаграммы по суммарному потреблению каждого усройства за указанный прошедший месяц
"""
Пример запроса
http://АДРЕС_СЕРВЕРА/get_data_from_pie?month=<month>

Пример результата

{
    "Android": 2.426183281010387,
    "FAN": 2.426183281010387,
    "Fridge": 6.430361134408805,
    "Heater": 2.426183281010387,
    "Light": 2.426183281010387,
    "Not Defined": 8.856544415418504,
    "TV": 6.430361134408805,
    "TeslaPowerWall": 6.430361134408805,
    "Xiaomi": 6.430361134408805,
    "main": 44.28272207709527
}

"Not Defined" - расход который не попадат под мониторинг

"""


@app.route('/get_data_from_pie')
def get_data_from_pie(month_param=-1):
    if month_param == -1:
        month_param = int(request.args.get("month", default=-1))
    if month_param > 12 or month_param < 1:
        return {"error": "invalid month"}
    month = month_param
    next_month = month + 1

    if month < 10:
        month = '0' + str(month)
    if next_month < 10:
        next_month = '0' + str(next_month)

    if month == 12:
        Query = "SELECT mean(\"value\") FROM \"kvartira1\" WHERE time >= \'2020-" + str(
            month) + "-01 00:00:00\' and time < \'2020-" + "01" + "-01 00:00:00\' AND \"mesurement\" = \'kilowatt\' GROUP BY time(1h), \"sensor_id\""
    else:
        Query = "SELECT mean(\"value\") FROM \"kvartira1\" WHERE time >= \'2020-" + str(
            month) + "-01 00:00:00\' and time < \'2020-" + str(
            next_month) + "-01 00:00:00\' AND \"mesurement\" = \'kilowatt\' GROUP BY time(1h), \"sensor_id\""

    result = clientdb.query(Query).raw
    vals = dict()
    global_sum = 0
    main = 0
    for i in result['series']:
        summ_by_dev = 0
        for each in i['values']:
            if each[1] != None:
                summ_by_dev += each[1]
        print(summ_by_dev)
        vals[i['tags']['sensor_id']] = summ_by_dev
        if i['tags']['sensor_id'] != 'main':
            global_sum += summ_by_dev
        elif i['tags']['sensor_id'] == 'main':
            main = summ_by_dev
        vals["Not Defined"] = main - global_sum
    return vals


# Возвращает сравнение затрат с предыдущим методом

"""
Пример запроса
http://АДРЕС_СЕРВЕРА//get_compare_prevmonth?month=<month>

Пример результата
В этом месяце вы потратили на 53.1 кВт больше, это привело к увеличению расходов на 231.52 руб.

Если данных не достаточно (например месяц еще не закончился)



"""


@app.route('/get_compare_prevmonth')
def get_compare_prevmonth():
    month = request.args.get('month')
    if month:
        month = int(month)
    else:
        return {'error': "ERROR set ?month=<value>"}
    month_data = get_data_from_pie(month)
    print(month_data)
    prevmonth_data = get_data_from_pie(month - 1)
    print(prevmonth_data)
    compare = round(float(month_data.get("main", 0)) - float(prevmonth_data.get("main", 0)), 1)
    if compare == 0:
        message = "К сожалению , пока что недостаточно данных."
        return message  # {"message": message}
    elif compare < 0:
        message = f"В этом месяце вы потратили на {-compare} кВт меньше, это помогло вам сохранить {round(-compare * CONFIG['tariff'], 2)} руб."
        return message  # {"message": message}
    else:
        message = f"В этом месяце вы потратили на {compare} кВт больше, это привело к увеличению расходов на {round(compare * CONFIG['tariff'], 2)} руб."
        return message  # {"message": str(message)}


# Возвращает устройство (или устройства если их несколько) имеющие максимальное и минимальное потребление (по пикам и минимумам) за запрашуемый месяц
"""
Пример запроса
http://АДРЕС_СЕРВЕРА/max_min_consum?month=<month>

Пример результата

{
    "max_consum": [
        "Fridge",
        "TV",
        "TeslaPowerWall",
        "Xiaomi"
    ],
    "min_consum": [
        "Android",
        "FAN",
        "Heater",
        "Light"
    ]
}

"""


@app.route('/max_min_consum')
def max_min_consum():
    month_param = int(request.args.get("month", default=-1))
    if month_param > 12 or month_param < 1:
        return {"error": "invalid month"}
    month = month_param
    next_month = month + 1

    if month == 12:
        Query = "SELECT mean(\"value\") FROM \"kvartira1\" WHERE time >= \'2020-" + str(
            month) + "-01 00:00:00\' and time < \'2020-" + "01" + "-01 00:00:00\' AND \"mesurement\" = \'kilowatt\' GROUP BY time(1h), \"sensor_id\""
    else:
        Query = "SELECT mean(\"value\") FROM \"kvartira1\" WHERE time >= \'2020-" + str(
            month) + "-01 00:00:00\' and time < \'2020-" + str(
            next_month) + "-01 00:00:00\' AND \"mesurement\" = \'kilowatt\' GROUP BY time(1h), \"sensor_id\""

    result = clientdb.query(Query).raw
    list_dev_val = list()

    for i in result['series']:
        current_dev_val = list()
        for each in i['values']:
            if each[1] != None:
                current_dev_val.append(each[1])
        tmp_dict = dict()
        tmp_dict['name'] = i['tags']['sensor_id']
        tmp_dict['val'] = current_dev_val
        list_dev_val.append(tmp_dict)
    print(list_dev_val)

    result_max_dict = dict()
    result_min_dict = dict()
    for i in list_dev_val:
        result_max_dict[i['name']] = max(i['val'])
    # print(result_max_dict)

    for i in list_dev_val:
        result_min_dict[i['name']] = min(i['val'])
    # print(result_min_dict)

    max_consum = [key for (key, value) in result_max_dict.items() if value == max(result_max_dict.values())]
    min_consum = [key for (key, value) in result_min_dict.items() if value == min(result_min_dict.values())]

    return {"min_consum": min_consum, "max_consum": max_consum}


@app.route('/get_departments')
def get_departments():
    con = mysql.connector.connect(user='Solidworks', password='Solidworks1212',
                                  host='pmelikov.ru',
                                  port='46306',
                                  database='hackinhome')
    c = con.cursor(dictionary=True)
    c.execute("""SELECT * FROM departaments""")
    response = c.fetchall()
    c.close()
    return jsonify({"departments":response})


@app.route('/get_appeal')
def get_appeal():
    con = mysql.connector.connect(user='Solidworks', password='Solidworks1212',
                                  host='pmelikov.ru',
                                  port='46306',
                                  database='hackinhome')
    dep_id = int(request.args.get("id", default=-1))
    c = con.cursor(dictionary=True)
    if dep_id == -1:
        c.execute(f"""select appeal.id, appeal.chat_id, appeal.message_id, appeal.text, departament_id, appeal.state,departaments.departament_name,users.stud_id, users.full_name  
                    from appeal join departaments on appeal.departament_id = departaments.id join users on appeal.chat_id = users.chat_id where appeal.state = 1""")
    else:
        c.execute(f"""select appeal.id, appeal.chat_id, appeal.message_id, appeal.text, departament_id, appeal.state,departaments.departament_name,users.stud_id, users.full_name  
                    from appeal join departaments on appeal.departament_id = departaments.id join users on appeal.chat_id = users.chat_id where departament_id = {dep_id} and appeal.state = 1""")
    response = c.fetchall()
    c.close()
    return jsonify({"appeals":response})


def send_quiz(url):
    con = mysql.connector.connect(user='Solidworks', password='Solidworks1212',
                                  host='pmelikov.ru',
                                  port='46306',
                                  database='hackinhome')
    c = con.cursor(dictionary=True)
    c.execute("""select * from users""")
    response = c.fetchall()
    c.close()
    for row in response:
        r = requests.post(' https://api.telegram.org/bot1618058420:AAEubhAUSpbOQ7GKPNlQxlpEPrhdC72BF6g/sendMessage',
                      json={'chat_id': int(row.get('chat_id')), 'text': f'Пройдите опрос: {url}'})
        print(r.text)
    return "OK"


@app.route('/quiz', methods=['POST'])
def quiz():
    con = mysql.connector.connect(user='Solidworks', password='Solidworks1212',
                                  host='pmelikov.ru',
                                  port='46306',
                                  database='hackinhome')
    if request.json and 'url' in request.json:
        print(request.json)
        c = con.cursor(dictionary=True)
        c.execute(f"""insert into quiz(url,name) values('{request.json['url']}','{request.json['name']}')""")
        con.commit()
        c.close()
        send_quiz(url=request.json['url'])
    return jsonify({"result": "ok"}), 201


@app.route('/response_appeal', methods=['POST'])
def response_appeal():
    if request.json and 'chat_id' in request.json:
        r = requests.post(' https://api.telegram.org/bot1618058420:AAEubhAUSpbOQ7GKPNlQxlpEPrhdC72BF6g/sendMessage',json={'chat_id': int(request.json['chat_id']), 'text': str(request.json['response']), 'reply_to_message_id': int(request.json['message_id'])})
        print("Ответ отправлен")
        if int(request.json['status']) == 3:
            con = mysql.connector.connect(user='Solidworks', password='Solidworks1212',
                                          host='pmelikov.ru',
                                          port='46306',
                                          database='hackinhome')
            c = con.cursor(dictionary=True)
            c.execute(f"""UPDATE appeal SET state = 3 WHERE id = {request.json['appeal_id']}""")
            con.commit()
            c.close()
        print(r.text)
    return jsonify({"result": "ok"})


@app.route('/get_form', methods=['POST'])
def get_form():
    print(request.json)

    dic = dict()
    res = re.split('\\n\\n', request.json['params']['answers'])
    for i in res:
        res_local = re.split('\\n', i)
        print(res_local)
        dic[str(res_local[0])] = str(res_local[1])
    # form = request.get_data(as_text=True)
    dic['form_id'] = request.json['params']['form_id']
    dic['form_name'] = request.json['params']['form_name']

    con = mysql.connector.connect(user='Solidworks', password='Solidworks1212',
                                  host='pmelikov.ru',
                                  port='46306',
                                  database='hackinhome')
    c = con.cursor(dictionary=True)
    print(f""" INSERT INTO {request.json['params']['form_id']} {tuple(dic.keys())} VALUES {tuple(dic.values())}""")
    c.execute(f""" INSERT INTO {request.json['params']['form_id']} {tuple(dic.keys())} VALUES {tuple(dic.values())}""")
    con.commit()
    c.close()
    return jsonify({"result": "ok"})


@app.route('/get_departments2')
def get_departments2():
    con = mysql.connector.connect(user='Solidworks', password='Solidworks1212',
                                  host='pmelikov.ru',
                                  port='46306',
                                  database='hackinhome')
    c = con.cursor(dictionary=True)
    for row in c:
        print(row.get('chat_id'))
    c.close()
    return jsonify({"departments":"dep"})


if __name__ == "__main__":
    app.run(host='192.168.100.160', port=5000, use_reloader=True)
    # app.run(host='localhost', port=5000, use_reloader=True, debug=True)