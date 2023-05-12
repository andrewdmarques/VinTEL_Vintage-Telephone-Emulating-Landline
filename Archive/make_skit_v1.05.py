#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# make_skit.py (v1.05) Helps organize the skit file based on the input files.
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


def get_user_input(values):
    if values['dial']:
        return sg.popup_get_text('User dial input:')
    elif values['hook']:
        return 'hook-on'
    elif values['voice']:
        return sg.popup_get_text('User audio keywords input:')
    else:
        return ''

layout = [
    [sg.Text('Name for skit file:\t'), sg.InputText(key='skit_file')],
    [sg.Text('')],
    [sg.Text('Current file:\t'), sg.InputText(key='from')],
    [sg.Checkbox('First file to be played in skit?', key='first_file')],
    [sg.Text('User input type:\t')],
    [sg.Radio('Dial', 'RADIO1', key='dial'), sg.Radio('Hook', 'RADIO1', key='hook'), sg.Radio('Voice', 'RADIO1', key='voice')],
    [sg.Text('Next file:\t\t'), sg.InputText(key='to')],
    [sg.Listbox([], size=(60, 10), key='input_list')],
    [sg.Button('Add Interaction'), sg.Button('Delete Selected'), sg.Button('Submit')]
]

# Create the PySimpleGUI window
window = sg.Window('VinTEL Skit Creator', layout)

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
    if event == 'Add Interaction':
        # Add the current input data to the list
        input_value = get_user_input(values)
        new_input = [values['from'], input_value, input_value, values['to'], 'yes' if values['first_file'] else 'no']
        input_data.append(new_input)


        # Update the Listbox and clear the form values
        window['input_list'].update([str(item) for item in input_data])
        window['from'].update('')
        window['to'].update('')
        #window['input'].update('')
        window['first_file'].update(False)

    if event == 'Delete Selected':
        selected_item = values['input_list'][0]
        index_to_remove = input_data.index(eval(selected_item))
        input_data.pop(index_to_remove)
        window['input_list'].update([str(item) for item in input_data])

    if event == 'Submit':
        # Create the CSV file with the input data
        skit_file = values['skit_file']
            
        if skit_file:
            file_path = dir_audio + '/' + skit_file + '.csv'
            
            # Overwrite the previous file if it existed.
            if os.path.isfile(file_path):
                os.remove(file_path)
            
            create_csv_file(file_path, input_data)

            # Clear the form values and input data list
            window['skit_file'].update('')
            window['from'].update('')
            #window['input'].update('')
            window['to'].update('')
            window['first_file'].update(False)
            input_data = []
            window['input_list'].update([])

# Close the PySimpleGUI window
window.close()

