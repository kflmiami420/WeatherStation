from ADAFRUIT_BME280_LIBRARY import *
import time
import SI1145
import MCP3008
import MyPyDHT


sensor_temp_pressure = BME280(t_mode=BME280_OSAMPLE_8,
                              p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
mcp = MCP3008.MCP3008()

interval = 0.5
sensor_UV = SI1145.SI1145()
while True:
    humidity, temperature = MyPyDHT.sensor_read(MyPyDHT.Sensor.DHT22, 4)
    print(MyPyDHT.sensor_read(MyPyDHT.Sensor.DHT22, 4))
    vis = sensor_UV.readVisible()
    IR = sensor_UV.readIR()
    UV = sensor_UV.readUV()
    windspeed = abs(round(MCP3008.value_to_kmh((mcp.read_channel(0))), 3))
    degrees = sensor_temp_pressure.read_temperature()
    pascals = sensor_temp_pressure.read_pressure()
    hectopascals = pascals / 100
    uvIndex = UV / 100.0
    print('Temp BME280      {0:0.3f} deg C'.format(degrees))
    print('Temp DHT22       {0:0.3f} deg C'.format(temperature))
    print('Pressure:        {0:0.2f} hPa'.format(hectopascals))
    print('Humidity:        {0:0.2f} %'.format(humidity))
    print('UV Index:        ' + str(uvIndex))
    print('Windspeed:       ' + str(windspeed))

    time.sleep(interval)
