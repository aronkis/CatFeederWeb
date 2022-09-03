from inspect import getframeinfo, currentframe
from datetime import datetime
from flask import request
import sqlite3
import pytz
import json

with open("timezones.json", "r") as f:
    dictTimezones = json.load(f)


def getTime(conn):
    try:
        regionS = conn.execute("SELECT timezoneRegion FROM db").fetchone()[0]
        if regionS == 'Select Region':
            regionS = 'Europe'
    except TypeError as e:
        print(e)
        regionS = 'Europe'
    try:
        cityS = conn.execute("SELECT timezoneCity FROM db").fetchone()[0]
        if regionS == 'Select Region':
            cityS = 'London'
        elif cityS == 'Select Country':
            cityS = dictTimezones[regionS][0]
    except TypeError as e:
        print(e)
        cityS = 'London'

    zone = regionS + '/' + cityS
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone(zone))
    try:
        time = pst_now.strftime("%H:%M:%S")
        date = pst_now.strftime("%d/%m/%Y")
    except TypeError as e:
        print(getframeinfo(currentframe()).lineno, " :: ", e)
    return time, date, zone


def getDataFromRequest(database, key, data):
    if int(data) > 35:
        data = 35
    updateDB(database, key, data)

# ???


def checkLength(database, numberOfFeedTimes, lenOffeedSchedulesKey):
    if numberOfFeedTimes > lenOffeedSchedulesKey:
        updateDB(database, 'numberOfFeedTimes', lenOffeedSchedulesKey)
        leng = lenOffeedSchedulesKey
    else:
        leng = int(numberOfFeedTimes)
    return leng


def getTimeFromRequest(database):
    conn = get_db_connection(database)
    feedSchedulesKey = request.args.get('feedSchedules', '').split(sep=',')
    if feedSchedulesKey[0] != '':
        numberOfFeedTimes = conn.execute(
            "SELECT numberOfFeedTimes FROM db").fetchone()[0]
        if (numberOfFeedTimes == 0):
            updateDB(database, 'numberOfFeedTimes', len(feedSchedulesKey))
        elif (numberOfFeedTimes != 0):
            leng = checkLength(conn, numberOfFeedTimes, len(feedSchedulesKey))
            conn.execute("DELETE FROM times")
            for i in range(0, leng):
                try:
                    conn.execute(
                        "INSERT INTO times(feedSchedules) VALUES(?)", (feedSchedulesKey[i],))
                except sqlite3.Error as e:
                    print(e)
    conn.commit()


def updateDB(database, dbEntry, value):
    conn = get_db_connection(database)
    select = conn.execute('SELECT {} FROM db'.format(dbEntry)).fetchone()
    if select is None:
        conn.execute(
            "INSERT INTO db ({}) VALUES (?)".format(dbEntry), (value,))
    else:
        conn.execute('UPDATE db SET {} = (?)'.format(dbEntry), (value,))
    conn.commit()


def updateTimes(database, times):
    conn = get_db_connection(database)
    conn.execute("DELETE FROM times")
    for time in times:
        conn.execute("INSERT INTO times(feedSchedules) VALUES (?)", (time,))
    conn.commit()


def get_db_connection(database):
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection


def getData(histories, page, offset=0, per_page=5):
    offset = (page - 1) * per_page
    return histories[offset: offset + per_page]


def getDataFromDB(conn):
    try:
        dbObj = conn.execute("SELECT * FROM db").fetchall()
        if len(dbObj) > 0:
            dbObj = dbObj[0]
        else:
            raise Exception("dbObj empty!")
        dbData = []
        for data in dbObj:
            dbData.append(data if data != None else '')
        return dbData
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)


def getTimesFromDB(conn):
    try:
        timesObj = conn.execute(
            'SELECT feedSchedules FROM times ORDER BY feedSchedules ASC').fetchall()
        if len(timesObj) > 0:
            times = []
            for row in timesObj:
                times.append(row[0])
            return times
        else:
            raise Exception("timesObj empty!")
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)


def getDataFromDatabase(database):
    conn = get_db_connection(database)
    dbData = getDataFromDB(conn)
    dbTimes = getTimesFromDB(conn)
    return dbData, dbTimes


def insertHistory(database, message):
    conn = get_db_connection(database)
    time = getTime(conn)[0]
    conn.execute("INSERT INTO history(date, log) VALUES (?,?)",
                 (time, message))
    conn.commit()


if __name__ == "__main__":
    dbData, dbTimes = getDataFromDatabase("database.db")
    print(dbData)
    print(dbTimes)
    
