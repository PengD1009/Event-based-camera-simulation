import cv2

cv2.namedWindow("camera", 1)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 25)
cap.set(3, 1920)
cap.set(4, 1080)
cnt = 0


while True:
    # 时间+1
    cnt = cnt + 1

    # 读取帧
    ret, frame = cap.read()

    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 获取事件
    if cnt >= 2:
        event = gray - gray_time_1 + 80


    #
    gray_time_1 = gray

    #
    if cnt >= 2:
        cv2.imshow('DroidCam', event)

    #
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#
cap.release()
cv2.destroyAllWindows()

