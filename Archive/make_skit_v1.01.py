import csv
import os
import PySimpleGUI as sg

# Define the layout of the PySimpleGUI form
layout = [
    [sg.Text('From:'), sg.InputText(key='from')],
    [sg.Text('Input:'), sg.InputText(key='input')],
    [sg.Text('Type:')],
    [sg.Radio('Audio', 'RADIO1', key='audio', default=True), sg.Radio('Python File', 'RADIO1', key='python_file')],
    [sg.Text('To:'), sg.InputText(key='to')],
    [sg.Button('Add Another Input'), sg.Button('Submit')]
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
        input_data.append([values['from'], values['input'], type_value, values['to']])

        # Clear the form values
        window['input'].update('')
        window['to'].update('')
    if event == 'Submit':
        # Add the current input data to the list
        if values['audio']:
            type_value = 'audio'
        elif values['python_file']:
            type_value = 'python_file'
        else:
            type_value = ''
        input_data.append([values['from'], values['input'], type_value, values['to']])

        # Create the CSV file with the input data
        file_path = os.path.join(os.path.expanduser("~"), 'Desktop', 'VinTEL', 'Audio', '113_skit.csv')
        create_csv_file(file_path, input_data)

        # Clear the form values and input data list
        window['from'].update('')
        window['input'].update('')
        window['to'].update('')
        input_data = []

# Close the PySimpleGUI window
window.close()

