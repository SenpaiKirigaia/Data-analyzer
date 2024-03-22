import logging
from auth import url, headers

logging.basicConfig(level=logging.INFO)


def send_data(measurement, mac_address, session):
    """
    Send measurement to API, using given session.

    :param measurement: Dict
    :param mac_address: str
    :param session: requests.Session
    :return:
    """
    response = session.post(url=url,
                            json={"device_id": mac_address, "data": measurement},
                            headers=headers)
    logging.info("Status Code: " + str(response.status_code))
    logging.info("Response: " + response.text)
