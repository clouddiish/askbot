#!/bin/bash

# add the default route
sudo ip route add default via 192.168.1.1

# Wait for the network to be ready
while ! ping -c 1 -W 1 google.com; do
    echo "Waiting for network..."
    sleep 5
done

cd /home/pi/askbot

source /home/pi/askbot/myenv/bin/activate

# Log Python and pip paths for debugging
echo "Using Python: $(which python)" >> /home/pi/logs/cron_debug.log
echo "Using pip: $(which pip)" >> /home/pi/logs/cron_debug.log

/home/pi/askbot/myenv/bin/python3 -m bot
