import logging
from datetime import datetime, timedelta
import calendar
import locale
import requests
import json


from flask import Flask, g, request, abort, flash, render_template, make_response, session, redirect, url_for
from flaskext.mysql import MySQL
from passlib import pwd
from passlib.hash import argon2, sha256_crypt


log = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', level=logging.DEBUG)

app = Flask(__name__, template_folder='./templates')
mysql = MySQL(app)

refreshdate = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'weatherstation-admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'adminpassword'
app.config['MYSQL_DATABASE_DB'] = 'weatherstation'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# session config
# app.secret_key = pwd.genword(entropy=128)
app.secret_key = 'test123'


def get_data(sql, params=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    records = []
    try:
        log.debug(sql)
        cursor.execute(sql, params)
        result = cursor.fetchall()
        for row in result:
            records.append(list(row))
    except Exception as e:
        log.exception("Fout bij het ophalen van data: {0})".format(e))
    cursor.close()
    conn.close()

    return records


def set_data(sql, params=None):
    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        log.debug(sql)
        cursor.execute(sql, params)
        conn.commit()
        log.debug("SQL uitgevoerd")

    except Exception as e:
        log.exception("Fout bij uitvoeren van sql: {0})".format(e))
        return False

    cursor.close()
    conn.close()

    return True


def pullforecast(local=True, postcode='1000', country='Belgium'):
    # ! ------------------------------------------ Getting the Location Key -------------------------------------------

    countrycode = ''
    locationname = ''
    # ?  With JSON File
    if local:
        with open('samplelocation.json', 'r') as f:
            location = json.load(f)
    # ?  With JSON Request to API
    else:
        locationrequest = requests.get('http://dataservice.accuweather.com/locations/v1/search?apikey=AneUd8b4EYWwFILuTKQzoXuHrAnNttnn&q=' + postcode + '%20' + country + '&details=true')
        location = locationrequest.json()
    for i in location:
        logging.debug(i['Country']['EnglishName'])

        if i['Country']['EnglishName'] == country:
            locationname = i['LocalizedName']
            countrycode = i['Key']

    logging.debug('countrycode')
    logging.debug('-------------------------------------------------------------------------------')
    logging.debug(countrycode)
    logging.debug('-------------------------------------------------------------------------------')

    # ! ----------------------------------------- Getting the WeatherForecast -----------------------------------------

    # ?  With JSON File
    if local:
        with open('sampleweather.json', 'r') as f:
            forecast = json.load(f)

    # ?  With JSON Request to API
    else:
        forecastrequest = requests.get('http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + str(countrycode) + '?apikey=AneUd8b4EYWwFILuTKQzoXuHrAnNttnn&details=true&metric=true')
        forecast = forecastrequest.json()

    # !  ---------------------------------------- Putting forecast data in order --------------------------------------
    forecastdata = [[datetime.strptime(forecast['DailyForecasts'][0]['Date'][0:10], '%Y-%m-%d').strftime('%a %d/%m'), forecast['DailyForecasts'][0]['Temperature']['Minimum']['Value'], forecast['DailyForecasts'][0]['Temperature']['Maximum']['Value'], forecast['DailyForecasts'][0]['Day']['PrecipitationProbability'], forecast['DailyForecasts'][0]['Day']['Wind']['Speed']['Value']],
                    [datetime.strptime(forecast['DailyForecasts'][1]['Date'][0:10], '%Y-%m-%d').strftime('%a %d/%m'), forecast['DailyForecasts'][1]['Temperature']['Minimum']['Value'], forecast['DailyForecasts'][1]['Temperature']['Maximum']['Value'], forecast['DailyForecasts'][1]['Day']['PrecipitationProbability'], forecast['DailyForecasts'][1]['Day']['Wind']['Speed']['Value']],
                    [datetime.strptime(forecast['DailyForecasts'][2]['Date'][0:10], '%Y-%m-%d').strftime('%a %d/%m'), forecast['DailyForecasts'][2]['Temperature']['Minimum']['Value'], forecast['DailyForecasts'][2]['Temperature']['Maximum']['Value'], forecast['DailyForecasts'][2]['Day']['PrecipitationProbability'], forecast['DailyForecasts'][2]['Day']['Wind']['Speed']['Value']],
                    [datetime.strptime(forecast['DailyForecasts'][3]['Date'][0:10], '%Y-%m-%d').strftime('%a %d/%m'), forecast['DailyForecasts'][3]['Temperature']['Minimum']['Value'], forecast['DailyForecasts'][3]['Temperature']['Maximum']['Value'], forecast['DailyForecasts'][3]['Day']['PrecipitationProbability'], forecast['DailyForecasts'][3]['Day']['Wind']['Speed']['Value']],
                    [datetime.strptime(forecast['DailyForecasts'][4]['Date'][0:10], '%Y-%m-%d').strftime('%a %d/%m'), forecast['DailyForecasts'][4]['Temperature']['Minimum']['Value'], forecast['DailyForecasts'][4]['Temperature']['Maximum']['Value'], forecast['DailyForecasts'][4]['Day']['PrecipitationProbability'], forecast['DailyForecasts'][4]['Day']['Wind']['Speed']['Value']],
                    ]
    logging.debug(forecastdata)
    return {'forecastdata': forecastdata, 'locationname': locationname}


forecastglobaldata = ''
locationnameglobal = ''


def updateforecastdata(manualmode=False, country='Belgium', postcode='1000'):
    global refreshdate
    global forecastglobaldata
    global locationnameglobal
    logging.debug(refreshdate)
    logging.debug(datetime.today().strftime('%Y-%m-%d'))

    if (refreshdate != datetime.today().strftime('%Y-%m-%d'))or manualmode:

        logging.debug('updateforecastdata function triggered')
        logging.debug('-------------------------------------------------------------------------------')
        logging.debug(country)
        logging.debug(postcode)
        logging.debug('-------------------------------------------------------------------------------')
        refreshdate = datetime.today().strftime('%Y-%m-%d')

        returndata = pullforecast(False, postcode, country)
        forecastdata = returndata['forecastdata']
        locationnameglobal = returndata['locationname']
        forecastglobaldata = forecastdata
        return forecastdata
    logging.debug('-------------------------------------------------------------------------------')

    return forecastglobaldata


def indexgatherer():
    data = get_data('SELECT * FROM weatherstation.sensordata order by `currentdatetime` desc limit 1')[0]
    historydata = get_data('SELECT * FROM weatherstation.history order by `currentdatetime` desc limit 5')
    username = session['username']
    userlocation = get_data('SELECT postcode,country FROM users where username=%s', (username))[0]

    logging.debug(userlocation)
    logging.debug(userlocation[0])
    logging.debug(userlocation[1])

    history = [[historydata[4][0].strftime('%a %d/%m'), (historydata[4][3] + historydata[4][9]) / 2, historydata[4][6], historydata[4][18], historydata[4][15]],
               [historydata[3][0].strftime('%a %d/%m'), (historydata[3][3] + historydata[3][9]) / 2, historydata[3][6], historydata[3][18], historydata[3][15]],
               [historydata[2][0].strftime('%a %d/%m'), (historydata[2][3] + historydata[2][9]) / 2, historydata[2][6], historydata[2][18], historydata[2][15]],
               [historydata[1][0].strftime('%a %d/%m'), (historydata[1][3] + historydata[1][9]) / 2, historydata[1][6], historydata[1][18], historydata[1][15]],
               [historydata[0][0].strftime('%a %d/%m'), (historydata[0][3] + historydata[0][9]) / 2, historydata[0][6], historydata[0][18], historydata[0][15]]]

    currentweather = [data[3], data[2], data[6], data[4], data[5]]

    forecast = updateforecastdata(False, userlocation[1], userlocation[0])

    return [currentweather, history, forecast]


@app.route('/')
def index():

    if session.get('username') is not None:
        data = indexgatherer()
        return render_template('index.html', data=data[0], historydata=data[1], forecastdata=data[2], locationname=locationnameglobal, history=False)
    else:
        return redirect(url_for('login'))


@app.route('/indexh')
def indexh():
    data = indexgatherer()
    if session.get('username') is not None:
        return render_template('index.html', data=data[0], historydata=data[1], forecastdata=data[2], locationname=locationnameglobal, history=True)
    else:
        return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    username = session['username']

    data = get_data('SELECT * FROM weatherstation.sensordata order by `currentdatetime` desc limit 1')[0]
    data2 = get_data('SELECT * FROM users where username=%s', (username))[0]

    weatherdata = [data[3], data[2], data[6], data[4], data[5]]
    settingdata = [data2[4], data2[5], data2[3], data2[6]]

    if request.method == 'POST':

        try:
            username = session['username']
            unit_selection = request.form.get('units')
            postcode = request.form.get('postcode')
            frequency = request.form.get('frequency')
            country = request.form.get('country')
            logging.debug(set_data("UPDATE users SET unit_selection=%s, postcode=%s,country=%s,frequency=%s WHERE username=%s", (unit_selection, postcode, country, frequency, username)))

            updateforecastdata(False, country, postcode)
            return render_template('settings.html', data=weatherdata, settingdata=settingdata, accepted=1)

        except e as identifier:
            logging.debug(e)
            return False

    return render_template('settings.html', data=weatherdata, settingdata=settingdata)


def registerfunc(username, pwd, email):

    try:
        set_data("INSERT INTO users (username,email,password) VALUES (%s,%s,%s)", (username, email, pwd))

    except Exception as e:
        logging.debug(e)
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username') is None:

        if request.method == 'POST':
            username = request.form.get('username')
            userpassword = request.form.get('password')
            logging.debug(userpassword)
            if request.form['submit'] == 'Login':
                data = get_data("SELECT * FROM users WHERE (username=%s) OR (email=%s)",  (username, username))
                if len(data) != 0:
                    if not sha256_crypt.verify(userpassword, data[0][2]):
                        return render_template('login.html', failed=1)
                    else:
                        session['username'] = username
                        set_data("UPDATE users SET active='1' WHERE username=%s", (username))
                        if data[0][5] == None:
                            logging.debug('data[0]')
                            return redirect(url_for('settings'))
                        else:
                            return redirect(url_for('index'))
                else:
                    return render_template('login.html', failed=1)

        return render_template('login.html')
    else:
        return redirect(url_for('logout'))


@app.route('/logout')
def logout():
    username = session['username']
    set_data("UPDATE users SET active='0' WHERE username=%s", (username))
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if request.form['submit'] == 'Register':
            passwordencrypt = sha256_crypt.encrypt(password)
            registerfunc(username, passwordencrypt, email)
            return redirect(url_for('login'))
    return render_template('register.html')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log.info("Flask app starting")
    app.run(host='0.0.0.0', debug=True)
