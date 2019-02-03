# DRIST
Driving Route Internet Speed Test: Created something hacky with python, iperf and AWS EC2 Machine. Essentially Macbook runs iperf to AWS EC2 Machine every 10s. While phone logs location through SensorLog app. All this time Macbook is tethered to phone's cellular network (e.g. AT&T).

## Prerequisits
* Macbook (or another laptop)
* AWS EC2 machine (or any other server)
* SensorLog App (e.g. https://itunes.apple.com/us/app/sensorlog/id388014573?mt=8)

## Runbook

#### Step 1
Run iperf server on AWS EC2 Machine, e.g.
```
ssh ubuntu@EC2_PUBLIC_DNS
tmux
iperf -s | ts "%Y-%m-%d %H:%M:%.S %z" | tee iperf_server.log
```

#### Step 2
On Macbook, run iperf every 10s to AWS EC2 Machine attempting to push 15mbps traffic for 1s, e.g.:
```
while : ; do sleep 10; iperf -t 1 -b 15M -c EC2_PUBLIC_DNS; done
```
Might need to run e.g. Amphetamine app to force Macbook not go to sleep.

#### Step 3
In SensorLog app go to settings (tap gear), use logging format json, recording rate 1Hz, HTTP disabled and log data to file. Tap Done. Tap REC

#### Step 4
Drive to places, while logs gets collected.

#### Step 5
When done. Stop logging SensorLog (tap X). Copy the generated log file.

#### Step 6
Stop iperf on Macbook, and scp logs from AWS EC2 Machine.

### Step 7
Open Run `create_map.py` and set values of constants. Run `python3 create_map.py` to generate `output_map.html`.
