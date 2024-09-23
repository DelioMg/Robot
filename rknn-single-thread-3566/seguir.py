import cv2
import time
from controle_robo import drive, stop, move_towards_person, close_connection
from reconhecimento_pessoa import detect_person

def follow_person():
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Detecta a pessoa no frame da câmera
            person_center = detect_person(frame)
            frame_center_x = frame.shape[1] // 2  # Ponto central da tela

            # Se uma pessoa for detectada, ajusta o movimento do robô
            if person_center:
                person_x, _ = person_center
                move_towards_person(person_x, frame_center_x)
            else:
                stop()  # Se não detectar, para o robô

            # Verifica se o usuário pressionou 'q' para sair
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.1)  # Pequeno atraso para não sobrecarregar

    except KeyboardInterrupt:
        print("Programa interrompido.")
    finally:
        cap.release()
        close_connection()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    follow_person()
