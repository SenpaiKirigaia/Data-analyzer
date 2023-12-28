import re
import json
import logging
from send_data import send_data

logging.basicConfig(level=logging.INFO)


def save_to_json(data: dict, filename: str):
    """
    Saves data to a JSON file.

    :param data: Data to be saved.
    :param filename: Path to the file to be saved.
    :return: None
    """
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        logging.error("Failed to save data: {}".format(e))


def get_data(filename: str):
    """
    Extracts data from a log file, sends measurements
     to the server and returns the result in JSON format.

    :param filename: Path to the log file to be processed.
    :return: A dictionary containing the device ID and the data extracted from the log file.
    """

    with open(filename, 'r') as file:
        content = file.read()
    mac_address_search = re.search(r"Connected to ((?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})", content)
    mac_address = mac_address_search.group(1) if mac_address_search else "UNKNOWN"

    # Regex patterns for data inside quotes
    regex = r'\"(.*?)\"'

    data_list = []

    # Get data for AND, WT-50 and Contour devices simultaneously
    for s in re.findall(regex, content, re.DOTALL):
        data_dict = {}

        # Values extracted from the string for AND device
        systolic = re.search(r'Systolic: (\d+\.\d+) (\w+)', s)
        diastolic = re.search(r'Diastolic: (\d+\.\d+) (\w+)', s)
        mean_ap = re.search(r'Mean AP: (\d+\.\d+) (\w+)', s)
        timestamp = re.search(r'Timestamp: (\d{2}:\d{2}:\d{2} \d{1,2}\.\d{1,2}\.\d{4})', s)
        pulse = re.search(r'Pulse: (\d+\.\d+) (\w+)', s)
        glucose = re.search(r'Glucose Concentration: (\d+\.\d+) (\w+/\w+)', s)

        # Try to extract error text (while trying thermometer log error occurs without it? not sure)
        try:
            error_text = s.split("Pulse: ")[1].split(" ")[2:]
        except IndexError:
            error_text = ""
        error_text = ' '.join(error_text)

        # Add extracted values to the dictionary
        if systolic:
            data_dict["Systolic"] = (float(systolic.group(1)), systolic.group(2))
        if diastolic:
            data_dict["Diastolic"] = (float(diastolic.group(1)), diastolic.group(2))
        if mean_ap:
            data_dict["Mean AP"] = (float(mean_ap.group(1)), mean_ap.group(2))
        if pulse:
            data_dict["Pulse"] = (float(pulse.group(1)), pulse.group(2))
        if error_text:
            data_dict["Error"] = error_text
        if timestamp:
            data_dict["Timestamp"] = timestamp.group(1)
        if glucose:
            data_dict["Glucose concentration"] = (float(glucose.group(1)), glucose.group(2))

        # WT-50 data extraction
        wt_match = re.search(r'(\d{2}\.\d{2})В°C', s)
        if wt_match:
            temperature = float(wt_match.group(1))
            data_dict["Temperature"] = temperature

        if data_dict:
            data_list.append(data_dict)

    # Send data to the server one by one
    send_data(data_list, mac_address)

    result = {
        "device_id": mac_address,
        "data": data_list
    }

    # Save the result to a JSON file
    save_to_json(result, 'output.json')
    return result
