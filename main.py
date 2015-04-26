from flask import Flask, make_response, render_template, request
import logging
import json
import requests
import StringIO
import config

app = Flask(__name__)

CONTENT_TYPE = {'Content-Type': 'application/json;charset=UTF-8'}
IRKIT_ENDPOINT = 'https://api.getirkit.com'
DEVICE_ID = "B0BBC8C215F54D0398746E943D47EEA8"
CLIENT_KEY = "448A6806B8584B7A99B68607F0EA2772"

POWER_SIGNAL = '{"format":"raw","freq":38,"data":[17421,8755,1037,1037,1037,1037,1037,3341,1037,1037,1037,1037,1037,1037,1037,1037,1037,3341,1037,1037,1037,1037,1037,1037,1037,1037,1037,1037,1037,3341,1037,3341,1037,3341,1037,1037,1037,1037,1037,1037,1037,1037,1037,1037,1037,3341,1037,1037,1037,1037,1037,3341,1037,3341,1037,3341,1037,3341,1037,3341,1037,1037,1037,3341,1037,3341,1037,65535,0,20691,17421,4400,1037,65535,0,65535,0,58076,17421,4400,1037,65535,0,65535,0,58076,17421,4400,1037,65535,0,65535,0,58076,17421,4400,1037,65535,0,65535,0,58076,17421,4400,1111,65535,0,65535,0,58076,17421,4400,1037,65535,0,65535,0,58076,17421,4400,1111]}'
SLEEP_SIGNAL = '{"format":"raw","freq":38,"data":[17421,8755,1150,1002,1150,1002,1150,3228,1150,1002,1150,1002,1150,1002,1150,1002,1150,3228,1150,1002,1150,1002,1150,1002,1150,1002,1150,1002,1150,3228,1150,3228,1150,3228,1150,1002,1150,3228,1150,1002,1150,1002,1150,1002,1150,3228,1190,968,1150,968,1150,3228,1150,1002,1190,3228,1150,3228,1150,3228,1150,1002,1150,3228,1150,3228,1150]}'

def generate_response(output_speech, card_title="", card_subtitle="", card_content="", session_attributes={}, should_end_session=True):
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "user": {
                "name": "nelson"
            }
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": output_speech
            },
            "card": {
                "type": "Simple",
                "title": card_title,
                "subtitle": card_subtitle,
                "content": card_content
            },
            "shouldEndSession": should_end_session
        }
    }
    return json.dumps(response)


@app.route('/', methods=['POST'])
def post():
    logging.info(json.dumps(request.json, indent=4, sort_keys=False))

    response = ""

    try:
        action = request.json["request"]["intent"]["slots"]["action"]["value"]
    except TypeError:
        response = generate_response("Action not found.")
        return response, 200, CONTENT_TYPE

    logging.info("Action: %s" % action)

    # Query API to convert name to Symbol
    if action == "on":
        response = requests.post(IRKIT_ENDPOINT + '/1/messages', data={
            "deviceid": DEVICE_ID,
            "clientkey":CLIENT_KEY,
            "message": POWER_SIGNAL})

        speech = "TV on"

    elif action == "off":
        response = requests.post(IRKIT_ENDPOINT + '/1/messages', data={
            "deviceid": DEVICE_ID,
            "clientkey": CLIENT_KEY,
            "message": POWER_SIGNAL})

        speech = "TV off"

    elif action == "sleep":
        response = requests.post(IRKIT_ENDPOINT + '/1/messages', data={
            "deviceid": DEVICE_ID,
            "clientkey": CLIENT_KEY,
            "message": SLEEP_SIGNAL})

        response = requests.post(IRKIT_ENDPOINT + '/1/messages', data={
            "deviceid": DEVICE_ID,
            "clientkey": CLIENT_KEY,
            "message": SLEEP_SIGNAL})

        speech = "TV Sleep set to 30 mins"

    else:
        speech = "Action unknown"

    response = generate_response(
        output_speech=speech,
        card_title="Turn {} TV.".format(action),
        card_subtitle=speech,
        card_content="")

    logging.info(json.dumps(json.loads(response), indent=4, sort_keys=False))
    return response, 200, CONTENT_TYPE


if __name__ == '__main__':
    app.run()

