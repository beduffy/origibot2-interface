import base64
import json
import time
import sys

import numpy as np
import cv2
import requests
#from bluetooth import *
import bluetooth
from flask import Flask, render_template, request, jsonify, send_from_directory


app = Flask(__name__, static_url_path='')
sock = None
CAMERA_FRAME_IP_ANDROID = 'http://192.168.0.31:8080/shot.jpg'
camera_server_online = False


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
    #import pdb;pdb.set_trace()
    try:
        response = requests.get(CAMERA_FRAME_IP_ANDROID) #, retries=0)  # won't work
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        print('Android camera at address: {} is not hosting'.format(CAMERA_FRAME_IP_ANDROID))
        return 'No camera feed'
        #sys.exit('')
    if response.status != 200:
        return 'No camera feed'
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
    #import pdb;pdb.set_trace()
    print('addr: {}'.format(addr))
    service_matches = bluetooth.find_service(address=addr)

    print('All service matches:')
    print(service_matches)
    if len(service_matches) == 0:
        print("couldn't find the Origibot2 bluetooth service =(")
        sys.exit(0)

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("connecting to \"%s\" on %s" % (name, host))

    # Create the client socket
    global sock
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))


if __name__ == '__main__':
    try:
        # todo only setup bluetooth if clicked in browser
        addr = None
        # if len(sys.argv) < 2:
        #     print("no device specified.  Searching all nearby bluetooth devices for")
        #     print("the SampleServer service")  # todo keep
        # else:
        #     addr = sys.argv[1]
        #     print("Searching for SampleServer on %s" % addr)
        addr = '00:1B:10:61:13:82'  # default

        setup_bluetooth_socket(addr)

        '''
        # todo could set it up at the start or could allow it to be dynamically added? Set it up at start is more principled, later is cooler.
        # do both
        try:
            response = requests.get(CAMERA_FRAME_IP_ANDROID) #, retries=0)  # won't work
            if response
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
            print('Android camera at address: {} is not hosting'.format(CAMERA_FRAME_IP_ANDROID))
            return 'No camera feed'''
        

        #app.run(port=8080, debug=True)  # oh shit, this is what is busy?
        app.run(port=8080)
    except Exception as e:
        # todo how to recover from bad failures with device busy?
        print('Error within app')
        print(e)
        if sock:
            time.sleep(2)
            sock.close()
