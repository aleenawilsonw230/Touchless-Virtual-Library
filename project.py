import cv2
import numpy as np
import textwrap
import os
import mediapipe as mp
import re
import winsound

# MEDIAPIPE
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7,min_tracking_confidence=0.7)

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(min_detection_confidence=0.7,min_tracking_confidence=0.7)

mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

WIDTH = 1300
HEIGHT = 800

cv2.namedWindow("Touchless Virtual Library", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Touchless Virtual Library", WIDTH, HEIGHT)

books = {
    "Pride and Prejudice": "prideandprejudice.txt",
    "Sherlock Holmes": "sherlockholmes.txt",
    "Alice in Wonderland": "aliceinwonderland.txt",
    "Frankenstein": "Frankenstein.txt",
    "Dracula": "Dracula.txt"
}

cover_images = {
    "Pride and Prejudice": "pride.jpg",
    "Sherlock Holmes": "sherlock.jpg",
    "Alice in Wonderland": "alice.jpg",
    "Frankenstein": "Frank.jpg",
    "Dracula": "dracula.jpg"
}

selected_book = None
current_page = 0
pages = []

smooth_x, smooth_y = 0, 0
alpha = 0.2

hover_frames = 0
hovered_book = None
HOLD_THRESHOLD = 30

zoom_level = 1
MAX_ZOOM = 3
pinch_ready = True

tilt_cooldown = 0
TILT_DELAY = 25

zone_cooldown = 0
ZONE_DELAY = 25

back_cooldown = 0
BACK_DELAY = 40


def play_page_sound():
    try:
        winsound.PlaySound("page.wav",winsound.SND_FILENAME | winsound.SND_ASYNC)
    except:
        pass


def get_finger_states(hand_landmarks):
    fingers = []
    fingers.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)
    fingers.append(1 if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y else 0)
    fingers.append(1 if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y else 0)
    fingers.append(1 if hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y else 0)
    fingers.append(1 if hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y else 0)
    return fingers


def load_book(filename):
    with open(filename, "r", encoding="utf-8-sig", errors="ignore") as f:
        text = f.read()

    text = re.sub(r'[^\x00-\x7F]+', '', text)
    words = text.split()
    PAGE_SIZE = 250

    return [" ".join(words[i:i+PAGE_SIZE])
            for i in range(0, len(words), PAGE_SIZE)]


while True:

    suc, cam_frame = cap.read()
    if not suc:
        continue

    cam_frame = cv2.flip(cam_frame, 1)
    rgb = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)
    face_results = face_mesh.process(rgb)

    cursor_x, cursor_y = smooth_x, smooth_y

    # HAND TRACKING
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(cam_frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

            finger_states = get_finger_states(hand_landmarks)

            if selected_book is not None and finger_states == [0,0,0,0,0]:
                if back_cooldown == 0:
                    selected_book = None
                    back_cooldown = BACK_DELAY

            index_tip = hand_landmarks.landmark[8]
            raw_x = int(index_tip.x * WIDTH)
            raw_y = int(index_tip.y * HEIGHT)

            smooth_x = int(alpha * raw_x + (1 - alpha) * smooth_x)
            smooth_y = int(alpha * raw_y + (1 - alpha) * smooth_y)

            cursor_x, cursor_y = smooth_x, smooth_y

            thumb_tip = hand_landmarks.landmark[4]
            thumb_x = int(thumb_tip.x * WIDTH)
            thumb_y = int(thumb_tip.y * HEIGHT)

            distance = np.sqrt((thumb_x - raw_x)**2 + (thumb_y - raw_y)**2)

            if distance < 40 and pinch_ready:
                zoom_level += 1
                if zoom_level > MAX_ZOOM:
                    zoom_level = 1
                pinch_ready = False

            if distance > 60:
                pinch_ready = True

    if back_cooldown > 0:
        back_cooldown -= 1

    # HEAD TILT
    if face_results.multi_face_landmarks and selected_book is not None:

        for face_landmarks in face_results.multi_face_landmarks:

            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]

            x1, y1 = int(left_eye.x * WIDTH), int(left_eye.y * HEIGHT)
            x2, y2 = int(right_eye.x * WIDTH), int(right_eye.y * HEIGHT)

            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            angle = -angle

            if tilt_cooldown == 0:

                if angle > 15:
                    if current_page < len(pages) - 1:
                        current_page += 1
                        play_page_sound()
                    tilt_cooldown = TILT_DELAY

                elif angle < -15:
                    if current_page > 0:
                        current_page -= 1
                        play_page_sound()
                    tilt_cooldown = TILT_DELAY

    if tilt_cooldown > 0:
        tilt_cooldown -= 1

    frame = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 245

    # MENU
    if selected_book is None:

        cv2.putText(frame, "Touchless Virtual Library",
                    (360, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (50,50,50), 3)

        positions = [(120,150),(380,150),(640,150),(250,450),(510,450)]
        titles = list(books.keys())

        for i in range(5):

            title = titles[i]
            x, y = positions[i]

            if os.path.exists(cover_images[title]):
                cover = cv2.imread(cover_images[title])
                cover = cv2.resize(cover,(180,250))
                frame[y:y+250, x:x+180] = cover

            if x < cursor_x < x+180 and y < cursor_y < y+250:

                cv2.rectangle(frame,(x-8,y-8),(x+188,y+258),(0,0,255),4)
                cv2.rectangle(frame,(x-4,y-4),(x+184,y+254),(0,0,200),2)

                if hovered_book == i:
                    hover_frames += 1
                else:
                    hovered_book = i
                    hover_frames = 1

                if hover_frames > HOLD_THRESHOLD:
                    selected_book = i
                    pages = load_book(list(books.values())[i])
                    current_page = 0
                    hover_frames = 0
                    hovered_book = None
            else:
                if hovered_book == i:
                    hovered_book = None
                    hover_frames = 0

            cv2.putText(frame,f"{i+1}. {title}",
                        (x,y+280),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,(40,40,40),2)

        cv2.circle(frame,(cursor_x,cursor_y),10,(0,0,255),-1)

    # READING MODE
    else:

        title = list(books.keys())[selected_book]
        cv2.putText(frame,title.upper(),
                    (380,80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,(50,50,50),3)

        if pages:

            font_scale = 0.6 + 0.2*(zoom_level-1)
            wrap_width = 95 - 20*(zoom_level-1)
            line_gap = 28 + 6*(zoom_level-1)

            wrapped = textwrap.wrap(pages[current_page], width=wrap_width)

            y_text = 150
            for line in wrapped:

                text_size = cv2.getTextSize(line,
                                            cv2.FONT_HERSHEY_SIMPLEX,
                                            font_scale, 1)[0]

                # Highlight
                if 120 < cursor_x < 120 + text_size[0] and \
                   y_text - line_gap < cursor_y < y_text:

                    cv2.rectangle(frame,
                                  (115, y_text - line_gap + 5),
                                  (125 + text_size[0], y_text + 5),
                                  (200, 230, 255),
                                  -1)

                cv2.putText(frame,line,(120,y_text),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            font_scale,(20,20,20),1)

                y_text += line_gap

            page_text = f"Page {current_page+1}/{len(pages)}"
            text_size = cv2.getTextSize(page_text,
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.7, 2)[0]
            text_x = (WIDTH - text_size[0]) // 2

            cv2.putText(frame,page_text,
                        (text_x,750),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,(60,60,60),2)

        if zone_cooldown == 0:

            if cursor_x < 100:
                if current_page > 0:
                    current_page -= 1
                    play_page_sound()
                zone_cooldown = ZONE_DELAY

            elif cursor_x > WIDTH - 100:
                if current_page < len(pages) - 1:
                    current_page += 1
                    play_page_sound()
                zone_cooldown = ZONE_DELAY

        if zone_cooldown > 0:
            zone_cooldown -= 1

        cv2.putText(frame,
                    "Pinch = Zoom | Tilt = Page | Fist = Menu | Edge = Flip",
                    (250,780),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,(80,80,80),2)

    small_cam = cv2.resize(cam_frame,(220,150))
    frame[620:770,1050:1270] = small_cam
    cv2.rectangle(frame,(1050,620),(1270,770),(0,0,0),2)

    cv2.imshow("Touchless Virtual Library", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()