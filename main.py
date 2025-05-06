import cv2
import time
from threading import Thread
from datetime import datetime

import emailing

video = cv2.VideoCapture(0)

first_frame = None
status_list = []

# Capture video
while True:
    status = 0
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
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))

        # Trigger for entering object
        if rectangle.any():
            status = 1
            now = datetime.now()
            # Take Screenshot
            cv2.imwrite(f'images/screen_{now.strftime("%H:%M:%S")}.png', frame)

    # Monitor the object inside the frame
    status_list.append(status)
    status_list = status_list[-2:]

    # Send email when the object exit the frame. USE THREADS
    if status_list[0] == 1 and status_list[1] == 0:
        image_path = emailing.image_to_send()
        # Thread execution
        email_thread = Thread(target=emailing.send_email, args=(image_path, ))
        email_thread.daemon = True
        email_thread.start()
    
    cv2.putText(img=frame, text="Hanzo Sama", org=(10, 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(20, 20, 150),
                thickness=2, lineType=cv2.LINE_AA)
                
    cv2.imshow("Video", frame)


    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
