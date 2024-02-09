import os
import time
import cv2 as cv
import mediapipe as mp

DIR_PATH = 'C:\Programiranje\DataProjekatNANS'

if not os.path.exists(DIR_PATH):
    os.makedirs(DIR_PATH)

broj_prstiju = 14
set_size = 200

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

cap = cv.VideoCapture(0)

for j in range(broj_prstiju):
    if not os.path.exists(os.path.join(DIR_PATH, 'PRST_BROJ_', str(j))):
        os.makedirs(os.path.join(DIR_PATH, 'PRST_BROJ_', str(j)))

    print('Pravim set za prst {}.'.format(j))
    start_time = time.time()
    capture_started = False

    while True:
        success, img = cap.read()
        img2 = cv.flip(img, 1)
        cv.putText(img2, "Stisni 'p' da pocnes.", (100, 50), cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3)
        cv.imshow('Kamera', img2)
        key = cv.waitKey(1) & 0xFF
        if key == ord('p') or key == ord('P'):
            print("Snimanje pocinje za 3 sekunde...")
            start_time = time.time()  # Reset the start time
            capture_started = True  # Set the flag to indicate capture has started
        elif time.time() - start_time >= 3 and capture_started:
            print("Snimanje je pocelo!")
            break

    i = 0
    while i < set_size/2:
        success, img = cap.read()
        img2 = cv.flip(img, 1)
        img2_rgb = cv.cvtColor(img2, cv.COLOR_BGR2RGB)

        results = hands.process(img2_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img2,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        cv.imshow('Kamera', img2)
        cv.waitKey(250)
        cv.imwrite(os.path.join(DIR_PATH, 'PRST_BROJ_', str(j), '{}.jpg'.format(i)), img2)
        i += 1

    start_time = time.time()
    capture_started = False
    while True:
        success, img = cap.read()
        img2 = cv.flip(img, 1)
        text = "Sada koristi drugu ruku."
        text1 = "Stisni 'p' da pocnes."
        cv.putText(img2, text, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
        cv.putText(img2, text1, (50, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
        cv.imshow('Kamera', img2)
        key = cv.waitKey(1) & 0xFF
        if key == ord('p') or key == ord('P'):
            print("Snimanje pocinje za 3 sekunde...")
            start_time = time.time()  # Reset the start time
            capture_started = True  # Set the flag to indicate capture has started
        elif time.time() - start_time >= 3 and capture_started:
            print("Snimanje je pocelo!")
            break

    i = 100
    while i < set_size:
        success, img = cap.read()
        img2 = cv.flip(img, 1)
        img2_rgb = cv.cvtColor(img2, cv.COLOR_BGR2RGB)

        results = hands.process(img2_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img2,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        cv.imshow('Kamera', img2)
        cv.waitKey(250)
        cv.imwrite(os.path.join(DIR_PATH, 'PRST_BROJ_', str(j), '{}.jpg'.format(i)), img2)
        i += 1

cap.release()
cv.destroyAllWindows()

print("Uspesno prikupljanje slika!")
