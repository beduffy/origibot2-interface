import base64
import json
import time
import sys

import numpy as np
import cv2
import requests
from bluetooth import *
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__, static_url_path='')
sock = None
CAMERA_FRAME_IP_ANDROID = 'http://192.168.0.31:8080/shot.jpg'

@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/send_command", methods=['POST'])
def send_command():
    data = json.loads(request.data)
    print('Received data: {}'.format(data))
    sock.send(data['commandToSend'])
    return jsonify({}), 200

@app.route("/get_camera_frame")
def get_camera_frame():
    response = requests.get(CAMERA_FRAME_IP_ANDROID)
    #img_arr = np.array(bytearray(response.content), dtype=np.uint8)
    #img = cv2.imdecode(img_arr, -1)

    # cv2.imshow('frame', img)
    return base64.b64encode(response.content)

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

def setup_bluetooth_socket(addr):
    # search for the SampleServer service
    # uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    # uuid = "MakeBlock"
    # service_matches = find_service( uuid = uuid, address = addr )
    # service_matches = find_service( name = uuid, address = addr )
    print('addr: {}'.format(addr))
    service_matches = find_service(address=addr)

    print(service_matches)
    if len(service_matches) == 0:
        print("couldn't find the SampleServer service =(")
        sys.exit(0)

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("connecting to \"%s\" on %s" % (name, host))

    # Create the client socket
    global sock
    sock = BluetoothSocket(RFCOMM)
    sock.connect((host, port))


if __name__ == '__main__':
    try:
        # todo only setup bluetooth if clicked in browser
        addr = None
        if len(sys.argv) < 2:
            print("no device specified.  Searching all nearby bluetooth devices for")
            print("the SampleServer service")
        else:
            addr = sys.argv[1]
            print("Searching for SampleServer on %s" % addr)

        setup_bluetooth_socket('00:1B:10:61:13:82')
        # app.run(port=8080, debug=True)
        app.run(port=8080)
    except Exception as e:
        print('ERROR')
        print(e)
        time.sleep(1000)
        sock.close()
