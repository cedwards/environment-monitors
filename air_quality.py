#!/usr/bin/env python3
# christer.edwards@gmail.com
# read air quality from SDS011 (PM2.5 and PM10 values)
# intended to be run via cron each minute

import serial

ser = serial.Serial('/dev/ttyU0', timeout=1)

data = []
for index in range(0,10):
    datum = ser.read()
    data.append(datum)

print(data)
pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

with open('/var/tmp/node_exporter/air_quality.prom', 'w') as _prom:
    print('# HELP node_sds011_aqi_pm2 This is the PM2.5 particulate reading by the SDS011', file=_prom)
    print('# TYPE node_sds011_aqi_pm2 gauge', file=_prom)
    print("node_sds011_aqi_pm2 %s" % (pmtwofive), file=_prom)
    print('# HELP node_sds011_aqi_pm10 This is the PM10 particulate reading by the SDS011', file=_prom)
    print('# TYPE node_sds011_aqi_pm10 gauge', file=_prom)
    print("node_sds011_aqi_pm10 %s" % (pmten), file=_prom)

print("2.5: %d" % (pmtwofive))
print("10: %d" % (pmten))
