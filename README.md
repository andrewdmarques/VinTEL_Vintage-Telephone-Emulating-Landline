# VinTEL

VinTEL is an interactive telephone conversation simulator designed for educational purposes. It utilizes Raspberry Pi, GPIO, and various hardware components to create a realistic telephone experience.

## Features

- Simulates incoming and outgoing phone calls
- Provides interactive skits with audio playback
- Detects motion events to trigger phone interactions
- Indicates system status using an LED indicator
- Allows user interaction through handset pickup and dialing

## Hardware Requirements

To set up the VinTEL system, you will need the following hardware components:

- Raspberry Pi board (Raspberry Pi 3 or newer recommended)
- Handset (microphone and speaker)
- Motion sensor
- LED indicator
- Resistors, wires, and other necessary electronic components

Refer to the `Hardware/Schematics` directory for detailed circuit diagrams and wiring instructions.

## Software Requirements

The VinTEL system relies on the following software components:

- Raspbian OS
- Python 3
- RPi.GPIO library
- VLC media player

## First-Time Installation

Follow the steps below to install the VinTEL system for the first time:

### 1. Install Raspbian OS on the Raspberry Pi

Follow the instructions provided in the following guide to install Raspbian OS on your Raspberry Pi:
[Install Raspbian OS Guide](https://www.instructables.com/HOW-TO-INSTALL-RASPBIAN-OS-IN-YOUR-RASPBERRY-PI/)

### 2. Install Dependencies and Prepare Files

Using the command terminal, run the following commands to install dependencies and prepare the VinTEL files:
```
sudo apt update
sudo apt install htop
sudo apt install thonny
sudo apt install firefox-esr
pip3 install PySimpleGUI
```

### 3. Make Scripts Executable

Move the VinTEL system files to the `/home/pi/Desktop/VinTEL/Bin/Scripts/` directory and make them executable by running the following commands:
```
chmod +x /home/pi/Desktop/VinTEL/Bin/Scripts/.py
chmod +x /home/pi/Desktop/VinTEL/Bin/Scripts/.sh
```
### 4. Set Up Cron Jobs

Create a crontab file to schedule the execution of the VinTEL system scripts at reboot. Open the crontab file by running the following command:
```
crontab -e
```

Add the following lines to the crontab file:
```
@reboot python3 /home/pi/Desktop/VinTEL/Bin/Scripts/audio-selector.py 1> /home/pi/Desktop/VinTEL/Bin/Status/Logs/log-audio-selector.txt
@reboot python3 /home/pi/Desktop/VinTEL/Bin/Scripts/coins.py 1> /home/pi/Desktop/VinTEL/Bin/Status/Logs/log-coins.txt
@reboot python3 /home/pi/Desktop/VinTEL/Bin/Scripts/controller.py 1> /home/pi/Desktop/VinTEL/Bin/Status/Logs/log-controller.txt
@reboot python3 /home/pi/Desktop/VinTEL/Bin/Scripts/dialer.py 1> /home/pi/Desktop/VinTEL/Bin/Status/Logs/log-dialer.txt
#@reboot python3 /home/pi/Desktop/VinTEL/Bin/Scripts/led-controller.py 1> /home/pi/Desktop/VinTEL/Bin/Status/Logs/log-led-controller.txt
@reboot python3 /home/pi/Desktop/VinTEL/Bin/Scripts/motion-controller.py 1> /home/pi/Desktop/VinTEL/Bin/Status/Logs/log-motion-controller.txt
@reboot python3 /home/pi/Desktop/VinTEL/Bin/Scripts/skit-player.py 1> /home/pi/Desktop/VinTEL/Bin/Status/Logs/log-skit-player.txt
@reboot python3 /home/pi/Desktop/VinTEL/Bin/Scripts/skit-selector.py 1> /home/pi/Desktop/VinTEL/Bin/Status/Logs/log-skit-selector.txt
@reboot /home/pi/Desktop/VinTEL/Bin/Scripts/player.sh 1> /home/pi/Desktop/VinTEL/Bin/Status/Logs/log-bash-player.txt
```
Save the crontab file and exit.

### 5. Configure VLC Audio Output

Open VLC media player on the Raspberry Pi and follow these steps to configure the audio output:

1. Go to **Tools > Preferences**.
2. Under the **Audio** section, select **All** on the bottom left of the screen to show all settings.
3. Navigate to **Audio > Output modules > ALSA**.
4. Select the **VoD server module "bcm2835 Headphones, bcm2835 Headphones Default Audio Device"**.
5. Save the settings and exit VLC.

### 6. Add Audio Files

Add any audio files that you would like to include in the VinTEL system. Follow the information provided in the quick start section of this manual to organize the audio files in the appropriate directories.

## Usage

1. Connect the necessary hardware components, such as the handset, LED, and motion sensor, to the Raspberry Pi following the circuit diagrams.
2. Make sure the VinTEL system is properly powered.
3. Turn on the main switch indicated by `main-on.txt` in the `/home/pi/Desktop/VinTEL/Bin/Status` directory.
4. Interact with the VinTEL system by picking up the handset, dialing numbers, or triggering motion events according to the configured skits.

Refer to the detailed README file in each script's directory for more specific instructions on their usage.

## Important File Descriptions

- `Bin/Scripts`: Contains the main system scripts and the `configure.csv` file for system configuration.
- `Bin/Status`: Stores the status files indicating various system states.
  - `main-on.txt`: Indicates that the main switch is toggled to the on position.
  - `hook-on.txt`: Indicates that the handset was picked up and the hook is toggled to the on position.
  - `hook-off.txt`: Indicates that the handset was placed down and the hook is toggled to the off position.
  - `call-on.txt`: Indicates that there is already a call in progress.
  - `dial-complete.txt`: Indicates that a number has been completed being dialed.
  - `Dial/number.txt`: Contains the dialed numbers on the first line.
  - `skit-on.txt`: Indicates that a skit should be played, initiating `skit-player.py`.
  - `call-initiated.txt`: Indicates that a docent-triggered call has been initiated.
  - `call-initiated-unattended.txt`: Indicates that a motion sensor-triggered call has been initiated.
  - `system-working.txt`: Indicates the system status during skit playback.
- `Bin/Effects`: Contains audio effects and prompts used in skits.
- `Bin/Skits`: Holds the CSV files defining different skits and their sequences.
- `Bin/Audio`: Stores the audio files used in skits and prompts.
- `Hardware/Schematics`: Contains detailed circuit diagrams and wiring instructions for hardware components.
- `README.md`: Provides information about the VinTEL system and its setup.
- `LICENSE`: The license under which the VinTEL system is distributed.

## Script Descriptions

1. `controller.py`: This script is responsible for controlling the overall VinTEL system. It monitors various input signals, such as button presses and sensor detections, and triggers corresponding actions, such as initiating calls, playing audio files, or controlling LEDs.

2. `coins.py`: This script handles coin detection and interaction in the VinTEL system. It detects when coins are deposited and keeps track of the deposited amount, which can be used to trigger specific actions or play corresponding audio files.

3. `dialer.py`: The `dialer.py` script emulates a dialing mechanism for the VinTEL system. It listens for input from a rotary dial or keypad and simulates the dialing process by generating corresponding tones or signals. It can be used to initiate calls or navigate through menus.

4. `audio-selector.py`: This script manages the selection and playback of audio files in the VinTEL system. It allows users to choose specific audio files for playback, control the volume, and handle audio-related functions.

5. `led-controller.py`: The `led-controller.py` script controls the LEDs (Light Emitting Diodes) in the VinTEL system. It manages the states and behavior of the LEDs, such as turning them on or off, blinking patterns, or adjusting brightness, to provide visual indications or feedback.

6. `make-skit.py`: This script is used to create skit files for the VinTEL system. It allows users to define a sequence of actions, audio files, and interactive elements to create custom skits or scenarios that can be played by the system.

7. `motion-controller.py`: The `motion-controller.py` script handles motion detection in the VinTEL system. It monitors motion sensors and detects movement or activity in the designated areas. It can be used to trigger specific actions, such as playing an audio file or initiating a call, when motion is detected.

8. `player.sh`: The `player.sh` script is a shell script that interacts with the audio player component of the VinTEL system. It executes the necessary commands to play audio files, control playback, and manage audio-related functionalities.

9. `skit-selector.py`: This script enables the selection and initiation of pre-defined skits in the VinTEL system. It provides options for users to choose from a list of available skits and triggers the playback of the selected skit.

10. `system-blink.py`: The `system-blink.py` script controls the system status indicator, typically an LED, in the VinTEL system. It continuously monitors the presence of a specific file and adjusts the LED's state accordingly. It provides visual feedback to indicate the operational status of the system.

The important directories and files are described in the initial sections of this README.


## Directory Structure

The directory structure of the VinTEL system is as follows:

```
VinTEL
├── Bin
│   ├── Scripts
│   │   ├── audio-selector.py
│   │   ├── coins.py
│   │   ├── controller.py
│   │   ├── dialer.py
│   │   ├── led-controller.py
│   │   ├── motion-controller.py
│   │   ├── skit-player.py
│   │   └── skit-selector.py
│   ├── Status
│   │   ├── Logs
│   │   │   ├── log-audio-selector.txt
│   │   │   ├── log-coins.txt
│   │   │   ├── log-controller.txt
│   │   │   ├── log-dialer.txt
│   │   │   ├── log-led-controller.txt
│   │   │   ├── log-motion-controller.txt
│   │   │   ├── log-skit-player.txt
│   │   │   └── log-skit-selector.txt
│   │   ├── main-on.txt
│   │   ├── hook-on.txt
│   │   ├── hook-off.txt
│   │   ├── call-on.txt
│   │   ├── dial-complete.txt
│   │   ├── Dial
│   │   │   └── number.txt
│   │   ├── skit-on.txt
│   │   ├── call-initiated.txt
│   │   ├── call-initiated-unattended.txt
│   │   └── system-working.txt
│   ├── Effects
│   ├── Skits
│   └── Audio
├── Hardware
│   ├── Schematics
│   └── Components
├── README.md
└── LICENSE
```

## License

The VinTEL system is released under the [MIT License](LICENSE).

Feel free to modify and adapt the VinTEL system according to your educational needs and requirements.
