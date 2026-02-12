import requests

def send_slack_message(webhook_url : str , message : str):

    payload = {
        "text" : message
    }

    response = requests.post(webhook_url , json = payload)

    if response.status_code != 200:
        
        raise Exception("cannot send slack notification")
    
