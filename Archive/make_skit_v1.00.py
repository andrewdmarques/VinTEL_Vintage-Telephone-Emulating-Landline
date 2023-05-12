import PySimpleGUI as sg

# Define the layout of the PySimpleGUI form
layout = [
    [sg.Text('From:'), sg.InputText(key='from')],
    [sg.Text('Input:'), sg.InputText(key='input')],
    [sg.Text('Type:')],
    [sg.Radio('Audio', 'RADIO1', key='audio', default=True), sg.Radio('Python File', 'RADIO1', key='python_file')],
    [sg.Text('To:'), sg.InputText(key='to')],
    [sg.Button('Submit')]
]

# Create the PySimpleGUI window
window = sg.Window('Create CSV File', layout)

# Define the function to create the CSV file
def create_csv_file(from_value, input_value, type_value, to_value):
    import csv
    with open('mycsvfile.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([from_value, input_value, type_value, to_value])
    print(f'CSV file created with values: {from_value}, {input_value}, {type_value}, {to_value}')

# Run the PySimpleGUI event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Submit':
        # Determine the value for the "type" column based on which radio button was clicked
        if values['audio']:
            type_value = 'audio'
        elif values['python_file']:
            type_value = 'python_file'
        else:
            type_value = ''

        # Create the CSV file with the form values
        create_csv_file(values['from'], values['input'], type_value, values['to'])

# Close the PySimpleGUI window
window.close()

