from datetime import datetime
from gmplot import gmplot
import numpy as np
import json

# set it to zero if "date" cmd on aws-ec2 machine is accurate
EC2_TO_LOCAL_OFFSET = -360
# e.g."2019-01-26 05:10:06.552 -0800"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f %z"
# https://developers.google.com/maps/documentation/embed/get-api-key
# Renders dark without the key
GMAP_API_KEY = ""
# file generated from iperf server
IPERF_SERVER_LOG_NAME = "iperf_server.log"
# file generated from SensorLog mobile app
SENSOR_LOG_NAME = "my_iOS_device_2019-01-26_05-10-05_-0800.json"

sensor_logs = json.loads(open(SENSOR_LOG_NAME).read())
iperf_logs = open(IPERF_SERVER_LOG_NAME).readlines()
iperf_logs = [l for l in iperf_logs if "sec" in l and "SUM" not in l]

times = [int(datetime.strptime(l["loggingTime"], TIME_FORMAT).timestamp()) for l in sensor_logs]
num = max(times) - min(times) + 1
off = min(times)

def get_nan(shape):
    nan_arr = np.empty(shape)
    nan_arr[:] = np.nan
    return nan_arr

lats = get_nan((num))
longs = get_nan((num))
speeds = get_nan((num))

for i, l in enumerate(sensor_logs):
    np_idx = times[i] - min(times)
    lats[np_idx] = float(l["locationLatitude"])
    longs[np_idx] = float(l["locationLongitude"])

for row in iperf_logs:
    cols = row.split()
    time = " ".join(cols[:3])
    time = int(datetime.strptime(time, TIME_FORMAT).timestamp()) + EC2_TO_LOCAL_OFFSET
    if time < min(times) or time > max(times):
        continue
    speed = float(cols[-2])
    if cols[-1] == "Mbits/sec":
        speed *= 1000
    elif cols[-1] == "bits/sec":
        speed /= 1000
    np_idx = time - min(times)
    speeds[np_idx] = speed
    
shape_2d = (int(num / 15), 15)
num_2d = int(num / 15) * 15
lats = lats[:num_2d].reshape(shape_2d)
longs = longs[:num_2d].reshape(shape_2d)
speeds = speeds[:num_2d].reshape(shape_2d)
speeds = np.nanmean(speeds, axis=1)
lats = np.nanmean(lats, axis=1)
longs = np.nanmean(longs, axis=1) 
    
gmap = gmplot.GoogleMapPlotter(np.nanmean(lats), np.nanmean(longs), 12, apikey=GMAP_API_KEY)
for i in range(len(lats) -1):
    avg_speed = (speeds[i] + speeds[i + 1]) / 2
    color = ""
    if avg_speed >= 1000:
        color = "green"
    elif avg_speed < 1000 and avg_speed > 1:
        color = "orange"
    elif avg_speed <= 1:
        color = "red"
    else:
        color = "black"
    gmap.plot(lats[i:i+2], longs[i:i+2], color=color, alpha=0.5, edge_width=10)
gmap.draw("output_map.html")
