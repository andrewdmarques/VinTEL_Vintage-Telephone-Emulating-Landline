#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# make_skit.py (v1.08) Helps organize the skit file based on the input files.
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

##########################################################################
# Run
##########################################################################
print('Running...')

import csv
import os
import PySimpleGUI as sg

def get_user_input(values):
    if values['dial']:
        return 'dial', sg.popup_get_text('User dial input:')
    elif values['hook']:
        return 'hook', 'hook-on'
    elif values['audio']:
        return 'audio', sg.popup_get_text('User audio keywords input:')
    else:
        return '', ''

layout = [
    [sg.Text('Name for skit file:\t'), sg.InputText(key='skit_file')],
    [sg.Text('')],
    [sg.Text('Current file:\t'), sg.InputText(key='from')],
    [sg.Checkbox('First file to be played in skit?', key='first_file')],
    [sg.Text('User input type:\t')],
    [sg.Radio('Dial', 'RADIO1', key='dial'), sg.Radio('Hook', 'RADIO1', key='hook'), sg.Radio('Audio', 'RADIO1', key='audio')],
    [sg.Text('Next file:\t\t'), sg.InputText(key='to')],
    [sg.Table(values=[],
              headings=['Current File', 'First File', 'Input Type', 'Input Value', 'Next File'],
              display_row_numbers=False,
              auto_size_columns=True,
              num_rows=10,
              key='input_table')],
    [sg.Button('Add Interaction'), sg.Button('Delete Selected'), sg.Button('Submit')]
]

window = sg.Window('VinTEL Skit Creator', layout)

def create_csv_file(file_path, input_data):
    with open(file_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Current_File', 'First_File', 'Input_Type', 'Input_Value', 'Next_File'])  # Write header row
        for row in input_data:
            csvwriter.writerow(row)
    print(f'CSV file created with {len(input_data)} rows')

input_data = []

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Add Interaction':
        input_type, input_value = get_user_input(values)
        new_input = [values['from'], 'yes' if values['first_file'] else 'no', input_type, input_value, values['to']]
        input_data.append(new_input)

        window['input_table'].update(values=input_data)
        window['from'].update('')
        window['to'].update('')
        window['first_file'].update(False)

    if event == 'Delete Selected':
        selected_item = values['input_table']
        if selected_item:
            index_to_remove = selected_item[0]
            input_data.pop(index_to_remove)
            window['input_table'].update(values=input_data)

    if event == 'Submit':
        skit_file = values['skit_file']

        if skit_file:
            dir_audio = 'path/to/your/audio/files'
            file_path = dir_audio + '/' + skit_file + '.csv'

            if os.path.isfile(file_path):
                os.remove(file_path)

            create_csv_file(file_path, input_data)

            window['skit_file'].update('')
            window['from'].update('')
            window['to'].update('')
            window['first_file'].update(False)
            input_data = []
            window['input_table'].update(values=input_data)

window.close()

