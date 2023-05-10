from socketIO_client import SocketIO
import numpy as np
import cv2
import time

def readFrameAndSend(camera, hsv_min, hsv_max, ip_address, port, id):
    cap = cv2.VideoCapture(camera)
    lower_color_limit = np.array([hsv_min[0], hsv_min[1], hsv_min[2]],np.uint8)
    upper_color_limit = np.array([hsv_max[0], hsv_max[1], hsv_max[2]],np.uint8)

    print("Conectando...")
    socketIO = SocketIO(ip_address, port)
    print("Conectado al servidor.")

    while True:
        ok, frame =cap.read()
        if not ok:
            continue

        #height, width, channels = frame.shape
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame_HSV,lower_color_limit, upper_color_limit)
        # cv2.imshow('mask', mask)
        contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(frame, contours, -1, (0,255,0), 3)
        # print(contours)

        for contour in contours:
            if cv2.contourArea(contour) > 100:
                M = cv2.moments(contour)
                X = int(M["m10"] / M["m00"])
                Y = int(M["m01"] / M["m00"])
                cv2.circle(frame,(X,Y), 5, (0,255,0), 3)
                cv2.putText(frame, "X={},Y={}".format(X,Y), (X-25, Y-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

                cv2.drawContours(frame, contour, -1, (0,0,255), 3)
                message = "{\"id\":\""+str(id)+"\","+"\"x\":"+str(X)+",\"y\":"+str(Y)+"}"
                socketIO.emit("position",message)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
        time.sleep(0.005)

    cap.release()
    cv2.destroyAllWindows() 
