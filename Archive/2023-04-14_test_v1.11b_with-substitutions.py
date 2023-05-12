import csv

# Create an empty dictionary to store the mapping between variables and directories
directory_mapping = {}

# Open the CSV file and read its contents
try:
    with open('/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv', 'r') as csvfile:
        config_reader = csv.DictReader(csvfile)

        # Loop through each row in the CSV file
        for row in config_reader:
            # Store the mapping between the variable and the directory
            directory_mapping[row['variable']] = row['directory']
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

# Open the CSV file again to update the command_on and command_off columns
with open('/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv', 'r') as csvfile:
    config_reader = csv.DictReader(csvfile)

    # Loop through each row in the CSV file
    for row in config_reader:
        # Check if the variable exists in any of the strings in the command_on or command_off columns
        variable = row['variable']
        command_on = row['command_on']
        command_off = row['command_off']

        # Replace the variable substring with the corresponding directory
        for var, dir in directory_mapping.items():
            command_on = command_on.replace(var, dir)
            command_off = command_off.replace(var, dir)

        # Print the updated row
        print(f"{variable},{command_on},{command_off}")
