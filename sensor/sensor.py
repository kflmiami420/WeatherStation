import logging
from time import sleep
import mysql.connector as mariadb
from ADAFRUIT_BME280_LIBRARY import *
import SI1145
import MCP3008
import MyPyDHT


log = logging.getLogger(__name__)
logging.basicConfig(filename='main.log', level=logging.DEBUG)
running = True
sensor_temp_pressure = BME280(t_mode=BME280_OSAMPLE_8,
                              p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
sensor_UV = SI1145.SI1145()
mcp = MCP3008.MCP3008()


def get_data(sql, params=None):
    conn = mariadb.connect(database='project1', user='project1-sensor', password='sensorpassword')
    cursor = conn.cursor()
    records = []

    try:
        log.debug(sql)
        cursor.execute(sql, params)
        result = cursor.fetchall()
        for row in result:
            records.append(list(row))

    except Exception as e:
        log.exception("Error while fetching data: {0})".format(e))

    cursor.close()
    conn.close()

    return records


def save_sensor_value(temperature_dht, humidity_dht, temperature_bmp, pressure_bmp, UV_si1145, windspeed):
    try:
        conn = mariadb.connect(
            database='project1', user='project1-sensor', password='sensorpassword')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sensordata (temperature_dht,humidity_dht, temperature_bmp, pressure_bmp,UV_si1145, windspeed) VALUES (%s, %s, %s, %s, %s, %s)", (temperature_dht, humidity_dht, temperature_bmp, pressure_bmp, UV_si1145, windspeed))
        conn.commit()

        return True
    except Exception as e:
        log.exception("DB update failed: {!s}".format(e))


def setup():
    def shutdown(*args):
        global running
        running = False

    signal.signal(signal.SIGTERM, shutdown)


def loop():

    interval = get_data(
        "select frequency from users ")[0][0]
    UV = sensor_UV.readUV()
    degrees = sensor_temp_pressure.read_temperature()
    humidity, temperature = MyPyDHT.sensor_read(MyPyDHT.Sensor.DHT22, 4)

    pascals = sensor_temp_pressure.read_pressure()
    hectopascals = pascals / 100
    uvIndex = UV / 100.0
    windspeed = abs(round(MCP3008.value_to_kmh((mcp.read_channel(0))), 3))
    if windspeed < 1:
        windspeed = 0
    save_sensor_value(temperature, humidity, degrees,
                      hectopascals, uvIndex, windspeed)

    sleep(int(interval)*60)
