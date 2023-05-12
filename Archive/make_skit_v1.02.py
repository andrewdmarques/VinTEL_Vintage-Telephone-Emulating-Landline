#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# make_skit.py (v1.02) Helps organize the skit file based on the input files.
# The curator would fill out the forms for this.
##########################################################################
# Load libraries
##########################################################################

import time
from datetime import datetime
import csv
import os
import re
import random # For selecting a random file to play from.
import PySimpleGUI as sg # For GUI

##########################################################################
# User input variables
##########################################################################

config_file = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'

##########################################################################
# Initialize
##########################################################################
print('Initializing')

# Open the configuration file and read the data
dir_status = '/home/pi/Desktop/VinTEL/Bin/Status'
with open(config_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['variable'] == 'dir_status':
            dir_status = row['directory']
        if row['variable'] == 'dir_effects':
            dir_effects = row['directory']
        if row['variable'] == 'dir_scripts':
            dir_scripts = row['directory']
        if row['variable'] == 'dir_audio':
            dir_audio = row['directory']
        if row['variable'] == 'dir_skits':
            dir_skits = row['directory']

# file_main     = dir_status + '/main-on.txt'       # The file that indicates the main switch is toggled to the on position.
# file_hook_on  = dir_status + '/hook-on.txt'       # The file that indicates the handset was picked up, the hook is toggled to the on position.
# file_hook_off = dir_status + '/hook-off.txt'      # The file that indicates the handset was placed down, the hook is toggled to the off position.
# file_call_on  = dir_status + '/call-on.txt'       # The file that indicates there is already a call in progress.
# file_dialed   = dir_status + '/dial-complete.txt' # The file that indicates that a number is completed being dialed.
# file_number   = dir_status + '/Dial/number.txt'   # The file containing the dialed numbers on the first line.
# file_skit_on  = dir_status + '/skit-on.txt'       # The file that indicates that a skit should be played, beginning skit-player.py.
# file_player_on = dir_scripts + '/player-on.txt'   # The file that indicates that that vlc should be activated and begin playing the selected audio file.
# file_temp     = dir_scripts + '/temp.py'          # The file that contains the commands to play the specified audio file.


##########################################################################
# Run
##########################################################################
print('Running...')

# Define the layout of the PySimpleGUI form
layout = [
    [sg.Text('From:'), sg.InputText(key='from')],
    [sg.Text('Input:'), sg.InputText(key='input')],
    [sg.Text('Type:')],
    [sg.Radio('Audio', 'RADIO1', key='audio', default=True), sg.Radio('Python File', 'RADIO1', key='python_file')],
    [sg.Text('To:'), sg.InputText(key='to')],
    [sg.Listbox([], size=(60, 10), key='input_list')],
    [sg.Button('Add Another Input'), sg.Button('Delete Selected'), sg.Button('Submit')]
]

# Create the PySimpleGUI window
window = sg.Window('Create CSV File', layout)

# Define the function to create the CSV file
def create_csv_file(file_path, input_data):
    with open(file_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in input_data:
            csvwriter.writerow(row)
    print(f'CSV file created with {len(input_data)} rows')

# Initialize the input data list
input_data = []

# Run the PySimpleGUI event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Add Another Input':
        # Add the current input data to the list
        if values['audio']:
            type_value = 'audio'
        elif values['python_file']:
            type_value = 'python_file'
        else:
            type_value = ''
        new_input = [values['from'], values['input'], type_value, values['to']]
        input_data.append(new_input)

        # Update the Listbox and clear the form values
        window['input_list'].update([str(item) for item in input_data])
        window['input'].update('')
        window['to'].update('')

    if event == 'Delete Selected':
        selected_item = values['input_list'][0]
        index_to_remove = input_data.index(eval(selected_item))
        input_data.pop(index_to_remove)
        window['input_list'].update([str(item) for item in input_data])

    if event == 'Submit':
        # Create the CSV file with the input data
        file_path = os.path.join(os.path.expanduser("~"), 'Desktop', 'VinTEL', 'Audio', '113_skit.csv')
        create_csv_file(file_path, input_data)

        # Clear the form values and input data list
        window['from'].update('')
        window['input'].update('')
        window['to'].update('')
        input_data = []
        window['input_list'].update([])

# Close the PySimpleGUI window
window.close()

