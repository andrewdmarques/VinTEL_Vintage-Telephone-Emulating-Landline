import os
import csv

def update_config_file(csv_file_path):
    # Create an empty dictionary to store the mapping between variables and directories
    directory_mapping = {}

    # Open the CSV file and read its contents
    try:
        with open(csv_file_path, 'r') as csvfile:
            config_reader = csv.DictReader(csvfile)

            # Loop through each row in the CSV file
            for row in config_reader:
                # Store the mapping between the variable and the directory
                directory_mapping[row['variable']] = row['directory']
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Update the command_on and command_off columns
    updated_rows = []
    with open(csv_file_path, 'r') as csvfile:
        config_reader = csv.DictReader(csvfile)

        # Loop through each row in the CSV file
        for row in config_reader:
            # Update the command_on and command_off columns
            updated_row = {}
            for key, value in row.items():
                if key == 'command_on' or key == 'command_off':
                    # Replace the variable substring with the corresponding directory
                    for var, dir in directory_mapping.items():
                        value = value.replace(var, dir)
                updated_row[key] = value

            # Add the updated row to the list
            updated_rows.append(updated_row)

    # Save the updated config file
    output_file_path = os.path.join(os.path.dirname(csv_file_path), 'temp_config.csv')
    try:
        with open(output_file_path, 'w', newline='') as csvfile:
            fieldnames = updated_rows[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        return

update_config_file('/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv')
