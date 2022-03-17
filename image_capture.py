import cv2
cap = cv2.VideoCapture(1)
ok, frame =cap.read()
if ok:
    cv2.imshow('frame', frame)
    cv2.imwrite('frame.jpg',frame)
    
cap.release()
cv2.destroyAllWindows()