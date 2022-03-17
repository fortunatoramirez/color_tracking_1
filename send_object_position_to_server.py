from ColoTrackingAndTx import readFrameAndSend

camera = 1
hsv_min = (90, 101, 153)
hsv_max = (179, 255, 255)
ip_address = "201.174.122.202"
port = 5001
id = "19212402"

readFrameAndSend(camera, hsv_min, hsv_max, ip_address, port, id)