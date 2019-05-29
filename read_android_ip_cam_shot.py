import numpy as np
import cv2
import requests

while True:
    response = requests.get('http://192.168.0.31:8080/shot.jpg')
    # import pdb;pdb.set_trace()

    # nparr = np.fromstring(response.text, np.uint8)
    # # img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
    # img = cv2.imdecode(nparr, 1)

    img_arr = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    cv2.imshow('frame', img)


    cv2.waitKey(1)
    print(img.shape)
    # import pdb; pdb.set_trace()
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
