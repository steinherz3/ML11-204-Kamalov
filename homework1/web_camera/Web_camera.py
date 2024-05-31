import cv2 
import mediapipe as mp

# Инициализация детекторов лиц и рук
mp_face_detection = mp.solutions.face_detection
mp_hands = mp.solutions.hands
face_detection = mp_face_detection.FaceDetection()
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)


# Функция для определения имени и фамилии
def determine_name_fingers(num_fingers):
    if num_fingers == 1:
        return "Name"
    elif num_fingers == 2:
        return "Family"
    else:
        return "Unknown"


# Открытие веб-камеры
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Обнаружение лиц
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results_face = face_detection.process(frame_rgb)

    if results_face.detections:
        for detection in results_face.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Обнаружение руки и подсчет пальцев
    results_hands = hands.process(frame_rgb)
    num_fingers = 0

    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            # Определение количества поднятых пальцев
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]

            fingers_up = [
                thumb_tip.y < hand_landmarks.landmark[3].y,
                index_tip.y < hand_landmarks.landmark[6].y,
                middle_tip.y < hand_landmarks.landmark[10].y,
                ring_tip.y < hand_landmarks.landmark[14].y,
                pinky_tip.y < hand_landmarks.landmark[18].y
            ]

            num_fingers += fingers_up.count(True)

    # Определение подписи
    name_fingers = determine_name_fingers(num_fingers)
    if results_face.detections:
        cv2.putText(frame, name_fingers, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
