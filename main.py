import cv2
import time
import numpy

video = cv2.VideoCapture(0)

# Take a photo and save on disk
check1, frame1 = video.read()
img_f1 = numpy.array(frame1)
cv2.imwrite('imgf1.png', img_f1)
time.sleep(1)
print(check1)

# Capture video
while True:
    check, frame = video.read()
    cv2.imshow('Main Camera', frame)

    key = cv2.waitKey(1)

    # process the frame

    if key == ord('q'):
        break

video.release()
