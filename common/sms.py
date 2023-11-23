import os
import requests


def send_text_message(to, body):
    """Send SMS using 46elks. Returns JSON response."""

    # check number format
    if not to.startswith('+'):
        raise ValueError('Phone number must start with +')

    # make API call
    response = requests.post(
        'https://api.46elks.com/a1/sms',
        auth = (os.environ["ELKS_USERNAME"], os.environ["ELKS_PASSWORD"]),
        data = {
            'from': 'Canceration',
            'to': to,
            'message': body,
            'dryrun': "yes" # !!!!!!!!!!!!!!!!!! TEMPORARY !!!!!!!!!!!!!!!!!!
        }
    )
    return response.json()
