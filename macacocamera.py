
import cv2
import mediapipe as mp
import time
import numpy as np
import math

# =======================================
#  CONFIGURAÇÕES E INICIALIZAÇÃO
# =======================================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

TIP_IDS = [4, 8, 12, 16, 20]

WINDOW_MAIN_NAME = "Reconhecimento de Gestos"
WINDOW_X_NAME = "Imagem Gesto X"
WINDOW_Y_NAME = "Imagem Gesto Y"

# =================================================================
#  ### PONTO PARA MUDAR AS IMAGENS ###
#  Altere os caminhos "macacodedonaboca.jpg" e "dedopracima.jpg"
#  para os caminhos das suas imagens.
# =================================================================
try:
    img_x = cv2.resize(cv2.imread("macacodedonaboca.jpg"), (400, 400))
    img_y = cv2.resize(cv2.imread("dedopracima.jpg"), (400, 400))
except Exception as e:
    print(f"Erro ao carregar imagens: {e}")
    img_x, img_y = None, None

frame_count = 0
t0 = time.time()
active_gesture_window = None

# =======================================
#  FUNÇÃO PARA RECONHECER O GESTO
# =======================================
def get_gesture(hand_landmarks, face_landmarks, frame_shape):
    gesture_name = "..."
    if not hand_landmarks:
        return gesture_name

    landmarks = hand_landmarks.landmark
    
    is_index_up = landmarks[TIP_IDS[1]].y < landmarks[TIP_IDS[1] - 2].y
    is_middle_down = landmarks[TIP_IDS[2]].y > landmarks[TIP_IDS[2] - 2].y
    is_ring_down = landmarks[TIP_IDS[3]].y > landmarks[TIP_IDS[3] - 2].y
    is_pinky_down = landmarks[TIP_IDS[4]].y > landmarks[TIP_IDS[4] - 2].y

    if is_index_up and is_middle_down and is_ring_down and is_pinky_down:
        gesture_name = "Dedo para Cima"

    if face_landmarks and is_index_up:
        finger_tip = landmarks[TIP_IDS[1]]
        lip_upper = face_landmarks.landmark[13]
        lip_lower = face_landmarks.landmark[14]
        
        h, w, _ = frame_shape
        finger_tip_px = (int(finger_tip.x * w), int(finger_tip.y * h))
        lip_upper_px = (int(lip_upper.x * w), int(lip_upper.y * h))
        lip_lower_px = (int(lip_lower.x * w), int(lip_lower.y * h))
        
        mouth_center_px = ((lip_upper_px[0] + lip_lower_px[0]) // 2, (lip_upper_px[1] + lip_lower_px[1]) // 2)
        
        distance = math.sqrt((finger_tip_px[0] - mouth_center_px[0])**2 + (finger_tip_px[1] - mouth_center_px[1])**2)
        
        if distance < 15:
            gesture_name = "Dedo na Boca"
            
    return gesture_name

# =======================================
#  LOOP PRINCIPAL
# =======================================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERRO: Câmera não encontrada!")
    exit()

print("Pressione Q para sair")

cam_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results_hands = hands.process(frame_rgb)
    results_face = face_mesh.process(frame_rgb)

    hand_landmarks = results_hands.multi_hand_landmarks[0] if results_hands.multi_hand_landmarks else None
    face_landmarks = results_face.multi_face_landmarks[0] if results_face.multi_face_landmarks else None
    
    gesture = get_gesture(hand_landmarks, face_landmarks, frame.shape)

    # --- LÓGICA PARA ATUALIZAR JANELAS DE IMAGEM ---
    if gesture == "Dedo na Boca" and img_x is not None:
        if active_gesture_window == WINDOW_Y_NAME:
            cv2.destroyWindow(WINDOW_Y_NAME)
        if active_gesture_window != WINDOW_X_NAME:
            cv2.imshow(WINDOW_X_NAME, img_x)
            cv2.moveWindow(WINDOW_X_NAME, cam_width, 0)
            active_gesture_window = WINDOW_X_NAME
    elif gesture == "Dedo para Cima" and img_y is not None:
        if active_gesture_window == WINDOW_X_NAME:
            cv2.destroyWindow(WINDOW_X_NAME)
        if active_gesture_window != WINDOW_Y_NAME:
            cv2.imshow(WINDOW_Y_NAME, img_y)
            cv2.moveWindow(WINDOW_Y_NAME, cam_width, 0)
            active_gesture_window = WINDOW_Y_NAME
    else:
        if active_gesture_window is not None:
            cv2.destroyWindow(active_gesture_window)
            active_gesture_window = None

    # --- LÓGICA DE DESENHO ---
    if hand_landmarks:
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow(WINDOW_MAIN_NAME, frame)
    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =======================================
#  FINALIZAÇÃO
# =======================================
cap.release()
cv2.destroyAllWindows()
hands.close()
face_mesh.close()
