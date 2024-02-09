import cv2 as cv
import numpy as np
import mediapipe as mp
import pickle

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

cap = cv.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)

labels_dict = {0: '0',
               1: '1',
               2: '2',
               3: '3',
               4: '4',
               5: '5',
               6: '6',
               7: '7',
               8: '8',
               9: '9',
               10: '+',
               11: '=',
               12: '?',
               13: '?'}

frame_counter = 0
input_sequence = []

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, slika = cap.read()
    slika_rgb = cv.cvtColor(slika, cv.COLOR_BGR2RGB)
    results = hands.process(slika_rgb)
    slika2 = cv.flip(slika, 1)
    cv.imshow("slika", slika2)
    cv.waitKey(25)

    if frame_counter % 35 == 0:
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    slika2,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

                prediction = model.predict([np.asarray(data_aux)])

                predicted_character = labels_dict[int(prediction[0])]

                input_sequence.append(predicted_character)

        current_input = ''.join(input_sequence)
        print(current_input)

        if current_input.endswith('?'):
            print("DZONI BIL ME KRSTIO? <3333")

        if current_input.endswith('='):
            result = eval(current_input[:-1])
            print(f"Rezultat: {result}")
            break

    frame_counter += 1

cap.release()
cv.destroyAllWindows()
