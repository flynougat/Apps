import cv2, time
from datetime import datetime
import pandas

video = cv2.VideoCapture(1) # number of camera
first_frame = None
a=1 #check how many frames are generated
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

while True:
    a=a+1
    check, frame = video.read()
    status = 0

    #print(check)
    #print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    if first_frame is None:
        first_frame = gray
        continue
    
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=2)

    (cnts, _) = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    status_list.append(status)
    status_list = status_list[-2:] #use only the last 2 items for the following if. Save computer memory

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    #time.sleep(3)
    cv2.imshow("Capturing", gray)
    cv2.imshow("delta frame", delta_frame)
    cv2.imshow("Threshold frame", thresh_delta)
    cv2.imshow("Color frame", frame)

    key = cv2.waitKey(1) 
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

df.to_csv("Record_Time.csv") #store time data into csv
#print(a)
video.release()
cv2.destroyAllWindows
