import cv2
import numpy as np

#
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

#
if not cap.isOpened():
    print("Normal")
    exit()

#
ret, old_frame = cap.read()
if not ret:
    print("Can't read video")
    exit()

old_frame = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# save video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Event.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

# ratio_threshold
ratio_threshold = 2.0  # (2:1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.subtract(frame_gray.astype(int), old_frame.astype(int))
    increase = np.clip(diff, 0, 255).astype(np.uint8)
    decrease = np.clip(-diff, 0, 255).astype(np.uint8)

    threshold = 30
    increase_event = (increase > threshold).astype(np.uint8) * 255
    decrease_event = (decrease > threshold).astype(np.uint8) * 255

    event_img = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    event_img[:, :, 2] = increase_event
    event_img[:, :, 0] = decrease_event

    #
    increase_count = np.sum(increase_event) / 255.0
    decrease_count = np.sum(decrease_event) / 255.0

    #
    if increase_count > decrease_count * ratio_threshold:
        cv2.putText(event_img, '++!Event!++', (frame.shape[1] - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif decrease_count > increase_count * ratio_threshold:
        cv2.putText(event_img, '--!Event!--', (frame.shape[1] - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("Event Camera", event_img)
    out.write(event_img)

    old_frame = frame_gray

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()