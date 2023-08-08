import cv2
import numpy as np

# open camera
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

# check
if not cap.isOpened():
    print("Normal")
    exit()

#
ret, old_frame = cap.read()
if not ret:
    print("Can't read video")
    exit()

old_frame = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

while True:
    #
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 计算亮度变化
    diff = cv2.subtract(frame_gray.astype(int), old_frame.astype(int))
    increase = np.clip(diff, 0, 255).astype(np.uint8)
    decrease = np.clip(-diff, 0, 255).astype(np.uint8)

    # 设置阈值来模拟事件相机的行为
    threshold = 30
    increase_event = (increase > threshold).astype(np.uint8) * 255
    decrease_event = (decrease > threshold).astype(np.uint8) * 255

    # 使用红色标记变亮的部分，使用蓝色标记变暗的部分
    event_img = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    event_img[:, :, 2] = increase_event  # Red channel
    event_img[:, :, 0] = decrease_event  # Blue channel

    # 显示事件
    cv2.imshow("Event Camera", event_img)

    # 更新旧帧
    old_frame = frame_gray

    # 按'q'退出循环
    if cv2.waitKey(1) == ord('q'):
        break

# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()