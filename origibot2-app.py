import json
import time
import sys

from bluetooth import *
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
sock = None

@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/send_command", methods=['POST'])
def send_command():
    data = json.loads(request.data)
    print('Received data: {}'.format(data))
    sock.send(data['commandToSend'])
    return jsonify({}), 200

def setup_bluetooth_socket(addr):
    # search for the SampleServer service
    # uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    # uuid = "MakeBlock"
    # service_matches = find_service( uuid = uuid, address = addr )
    # service_matches = find_service( name = uuid, address = addr )
    print('addr: {}'.format(addr))
    service_matches = find_service(address=addr)

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
