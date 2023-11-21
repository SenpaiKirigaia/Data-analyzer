import logging
import requests
from auth import url, headers

last_sent_index = 0


def send_request(measurement, headers):
    """
    Send request to API.

    :param measurement: dict
    :param headers: dict
    :return: None
    """

    response = requests.post(url=url,
                             json=measurement,
                             headers=headers)
    logging.info("Status Code: " + str(response.status_code))
    logging.info("Response: " + response.text)


def send_data(mac_address, data_list):
    """
    Process data to send measurements one by one.
    Then sends requests to API.

    :param mac_address:
    :param data_list:
    :return:
    """

    global last_sent_index
    for index, measurement in enumerate(data_list[last_sent_index:], start=last_sent_index):
        send_request({"device_id": mac_address, "data": measurement}, headers)
        last_sent_index = index + 1
