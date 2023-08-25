import mediapipe as mp
import cv2
import numpy as np
import time

import pandas


class MediaPipeService:
    is_running = False
    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    def start(self, on_detected: callable = None):
        self.cap.open(0)
        self.is_running = True

        while self.is_running:
            with mp.solutions.hands.Hands(
                min_detection_confidence=0.5, min_tracking_confidence=0.5
            ) as hands:
                while self.cap.isOpened():
                    ret, frame = self.cap.read()

                    if not ret:
                        print("Gagal membaca frame")
                        break

                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False

                    results = hands.process(image)

                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp.solutions.drawing_utils.draw_landmarks(
                                image,
                                hand_landmarks,
                                mp.solutions.hands.HAND_CONNECTIONS,
                                mp.solutions.drawing_utils.DrawingSpec(
                                    color=(80, 22, 10), thickness=2, circle_radius=4
                                ),
                                mp.solutions.drawing_utils.DrawingSpec(
                                    color=(80, 44, 121), thickness=2, circle_radius=2
                                ),
                            )
                            hand_features = list(
                                np.array(
                                    [
                                        [
                                            landmark.x,
                                            landmark.y,
                                            landmark.z,
                                            landmark.visibility,
                                        ]
                                        for landmark in hand_landmarks.landmark
                                    ]
                                ).flatten()
                            )

                            on_detected(hand_features)
                            time.sleep(0.1)

                    windowName = "Raw Webcam Feed"
                    cv2.imshow(windowName, image)
                    key = cv2.waitKey(1) & 0xFF

                    if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
                        break

                    if key == ord("x"):
                        break

                    if cv2.waitKey(10) & 0xFF == ord("q"):
                        break
                cv2.destroyAllWindows()
                self.is_running = False

    def close(self):
        self.is_running = False
        self.cap.release()
        cv2.destroyAllWindows()

    def on_message(self, client, userdata, message):
        # Handle the MQTT message here
        if message.topic == "close_opencv":
            self.close()
