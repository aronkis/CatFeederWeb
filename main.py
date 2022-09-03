from flask_paginate import Pagination, get_page_args
from flask import Flask, request, render_template
import helpers
import sqlite3
import json

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

with open("timezones.json", "r") as f:
    dictTimezones = json.load(f)


@app.route('/')
def index():
    return info()


@app.route('/history', methods=['GET', 'POST'])
def history():

    conn = helpers.get_db_connection("database.db")
    try:
        dateObj = conn.execute(
            'SELECT date FROM history ORDER BY date DESC').fetchall()
        historyObj = conn.execute(
            'SELECT log FROM history ORDER BY date DESC').fetchall()
    except sqlite3.Error as e:
        print(e)
        dateObj = []
    histories = []
    for i in range(len(dateObj)):
        histories.append(historyObj[i][0] + " " + dateObj[i][0])
    page, per_page, offset = get_page_args(
        page='page', per_page_parameter='per_page')
    per_page = 5
    total = len(histories)
    paginationData = helpers.getData(histories, page, offset, per_page)
    pagination = Pagination(page=page, per_page=per_page,
                            total=total, css_framework='bootstrap4')
    return render_template('history.html', paginationData=paginationData, page=page, per_page=per_page, pagination=pagination)


@app.route('/info', methods=['GET', 'POST'])
def info():
    conn = helpers.get_db_connection("database.db")
    _, date, zone = helpers.getTime(conn)
    dbData, dbTimes = helpers.getDataFromDatabase("database.db")
    feedAmount = dbData[0] if dbData != None and dbData[0] != '' else 0
    treatAmount = dbData[1] if dbData != None and dbData[1] != '' else 0
    numberOfFeedings = dbData[2] if dbData != None and dbData[2] != '' else 0

    return render_template('info.html', zone=zone, date=date, feedAmount=feedAmount, treatAmount=treatAmount, numberOfFeedings=numberOfFeedings, times=dbTimes)


@app.route('/treatLeft', methods=['GET', 'POST'])
def treatLeft():
    if request.method == "POST":
        helpers.insertHistory("database.db", "Pet treated (Left) at: ")
    return info()


@app.route('/treatRight', methods=['GET', 'POST'])
def treatRight():
    if request.method == "POST":
        helpers.insertHistory("database.db", "Pet treated (Right) at: ")
    return info()


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        keys = ['feedAmount', 'treatAmount', 'numberOfFeedTimes']
        for key in keys:
            data = request.args.get(key, '')
            if data != '':
                helpers.getDataFromRequest("database.db", key, data)
        helpers.getTimeFromRequest("database.db")

    dbData, dbTimes = helpers.getDataFromDatabase("database.db")
    feedAmount = dbData[0] if dbData != None and dbData[0] != '' else 0
    treatAmount = dbData[1] if dbData != None and dbData[1] != '' else 0
    numberOfFeedings = dbData[2] if dbData != None and dbData[2] != '' else 0
    regionS = dbData[3] if dbData != None and dbData[3] != '' else "Select region"
    cityS = dbData[4] if dbData != None and dbData[4] != '' else "Select city"
    regions = dictTimezones.keys()

    return render_template('settings.html', timezones=dictTimezones, numberOfFeedings=numberOfFeedings, feedAmount=feedAmount, treatAmount=treatAmount, times=dbTimes, regions=regions, regionS=regionS, cityS=cityS)


@app.route('/setTimezone', methods=['GET', 'POST'])
def setTimezone():
    if request.method == 'POST':
        data = request.json
        helpers.updateDB("database.db", 'timezoneRegion', data['region'])
        helpers.updateDB("database.db", 'timezoneCity', data['city'])
        return {"OK": "OK"}

    return settings()


@app.route('/setFoodAmount', methods=['GET', 'POST'])
def setFoodAmount():
    if request.method == "POST":
        req = request.form['feedAmount']
        helpers.updateDB("database.db", "feedAmount", req)
    return settings()


@app.route('/setTreatAmount', methods=['GET', 'POST'])
def setTreatAmount():
    if request.method == "POST":
        req = request.form['treatAmount']
        helpers.updateDB("database.db", "treatAmount", req)
    return settings()


@app.route('/setnumberOfFeedTimes', methods=['GET', 'POST'])
def setnumberOfFeedTimes():
    if request.method == "POST":
        req = request.form['numberOfFeedTimes']
        helpers.updateDB("database.db", "numberOfFeedTimes", req)
    return settings()


@app.route('/setFeedingHours', methods=['GET', 'POST'])
def setFeedingHours():
    if request.method == "POST":
        data = request.json
        times = data['times']
        helpers.updateTimes("database.db", times)
        return {"OK": "OK"}
    return settings()
