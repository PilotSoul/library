import cv2
import os
import webbrowser


def barcode_open(barcode: str):
    url = f"https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode={barcode}"
    webbrowser.open(url, new=0, autoraise=True)


# define a video capture object
# RTSP_URL = "rtsp://admin:admin@192.168.100.6:1935"
RTSP_URL = "rtsp://admin:admin@172.20.10.14:1935"

skip = False
count = 0

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
# vid = cv2.VideoCapture(0) # webcam
vid = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)  # rtsp codec usage

bardet = cv2.barcode_BarcodeDetector()
while True:
    ret, frame = vid.read()

    ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(frame)
    if ok:
        pt1 = corners[0][1]
        pt2 = corners[0][3]

        pt1 = (int(corners[0][1][0]), int(corners[0][1][1]))
        pt2 = (int(corners[0][3][0]), int(corners[0][3][1]))
        cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 3)

    if ok and not skip:
        if len(decoded_info[0]) > 12:
            # передаем barcode
            barcode_open(decoded_info[0])
            cv2.imshow('frame', frame)
            skip = True
            cv2.waitKey(0)
    if skip:
        count += 1
    if count == 300:
        skip = False
        count = 0
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('f'):
        input()

vid.release()
cv2.destroyAllWindows()
