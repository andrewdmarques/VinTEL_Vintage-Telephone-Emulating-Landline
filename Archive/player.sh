#!/bin/bash
sleep 10
while :
do
	sleep 0.1
	FILE=/home/pi/Desktop/VinTEL/Bin/Scripts/player-on.txt
	if [ -f "$FILE" ]; then
		rm -r /home/pi/Desktop/VinTEL/Bin/Scripts/player-on.txt
		FILE=/home/pi/Desktop/VinTEL/Bin/Scripts/temp.py
		if [ -f "$FILE" ]; then
			chmod +x /home/pi/Desktop/VinTEL/Bin/Scripts/temp.py
			python3 /home/pi/Desktop/VinTEL/Bin/Scripts/temp.py > /home/pi/Desktop/VinTEL/Bin/Status/Logs/bash_log.text 2>&1
		fi
	fi
done

