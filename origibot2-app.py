import sys

from bluetooth import *
from flask import Flask, render_template

app = Flask(__name__)
sock = None

@app.route("/")
def index_page():
    return render_template('index.html')

def setup_bluetooth_socket(addr):
    # search for the SampleServer service
    # uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    # uuid = "MakeBlock"
    # service_matches = find_service( uuid = uuid, address = addr )
    print('addr: {}'.format(addr))
    # service_matches = find_service( name = uuid, address = addr )
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
    sock = BluetoothSocket(RFCOMM)
    sock.connect((host, port))




if __name__ == '__main__':
    addr = None
    if len(sys.argv) < 2:
        print("no device specified.  Searching all nearby bluetooth devices for")
        print("the SampleServer service")
    else:
        addr = sys.argv[1]
        print("Searching for SampleServer on %s" % addr)

    # print("connected.  type stuff")
    # while True:
    #     data = input()
    #     if len(data) == 0: break
    #     sock.send(data)

    app.run(port=8080, debug=True)
    # sock.close()

