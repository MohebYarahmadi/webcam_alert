import cv2
import time
import numpy

video = cv2.VideoCapture(0)

# Take a photo and save on disk
def snapshot():
    img_f1 = numpy.array(frame)
    cv2.imwrite('imgf1.png', img_f1)
    time.sleep(1)
    print(check)


first_frame = None

# Capture video
while True:
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Take the reference frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # Check for differences
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Make silouhet frame
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('Main Camera', contours)

    # Mark objects
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
    
    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
