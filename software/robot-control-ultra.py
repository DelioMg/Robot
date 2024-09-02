import struct
import serial
import time
import wiringpi as wp

# Configurações de comunicação
PORT = '/dev/ttyUSB0'  # Substitua pelo porto serial correto
BAUDRATE = 115200
TIMEOUT = 1

# Configurações de movimento
VELOCITYCHANGE = 200
ROTATIONCHANGE = 300

# Pinos dos sensores ultrassônicos
TRIG_PIN = 0  # GPIO.0 (Ajuste conforme necessário)
ECHO_PIN = 1  # GPIO.1 (Ajuste conforme necessário)

# Inicializa a conexão serial
try:
    connection = serial.Serial(PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    print("Conectado ao iRobot Create 2!")
except serial.SerialException:
    print("Falha na conexão com o iRobot Create 2.")
    connection = None

# Inicializa a biblioteca GPIO
wp.wiringPiSetup()
wp.pinMode(TRIG_PIN, wp.OUTPUT)
wp.pinMode(ECHO_PIN, wp.INPUT)

# Funções de controle
def sendCommandRaw(command):
    global connection
    if connection is not None:
        connection.write(command)
        connection.flush()
    else:
        print("Não está conectado ao robô.")

def sendCommandASCII(command):
    cmd = bytes([int(v) for v in command.split()])
    sendCommandRaw(cmd)

def drive(velocity, rotation):
    vr = int(velocity + (rotation / 2))
    vl = int(velocity - (rotation / 2))
    cmd = struct.pack(">Bhh", 145, vr, vl)
    sendCommandRaw(cmd)

def measure_distance():
    # Envia um pulso de trigger
    wp.digitalWrite(TRIG_PIN, wp.LOW)
    time.sleep(0.02)
    wp.digitalWrite(TRIG_PIN, wp.HIGH)
    time.sleep(0.01)
    wp.digitalWrite(TRIG_PIN, wp.LOW)

    # Espera pelo pulso de eco
    while wp.digitalRead(ECHO_PIN) == wp.LOW:
        pulse_start = time.time()

    while wp.digitalRead(ECHO_PIN) == wp.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Velocidade do som é 34300 cm/s, dividido por 2
    distance = round(distance, 2)

    return distance

def avoid_obstacles():
    distance = measure_distance()
    if distance < 20:  # Distância limite para evitar obstáculos
        print(f"Obstáculo detectado a {distance} cm! Parando o robô.")
        drive(0, 0)
        return True
    return False

# Funções de controle de estado
def setPassiveMode():
    sendCommandASCII('128')

def setSafeMode():
    sendCommandASCII('131')

def setFullMode():
    sendCommandASCII('132')

def clean():
    sendCommandASCII('135')

def dock():
    sendCommandASCII('143')

def reset():
    sendCommandASCII('7')

def defineTones():
    # Toque de inicialização
    sendCommandASCII('140 0 4 72 16 76 16 79 16 83 16')
    # Toque de ligar
    sendCommandASCII('140 1 4 60 16 64 16 67 16 72 16')
    # Toque de obstáculo
    sendCommandASCII('140 2 1 55 32')

def playStartupTone():
    sendCommandASCII('141 0')

def playPowerOnTone():
    sendCommandASCII('141 1')

def playObstacleTone():
    sendCommandASCII('141 2')

# Função principal
def main():
    setPassiveMode()
    time.sleep(1)
    setSafeMode()
    defineTones()
    playStartupTone()

    try:
        while True:
            if avoid_obstacles():
                playObstacleTone()
                time.sleep(1)  # Espera 1 segundo antes de continuar para evitar colisões repetidas
                continue

            drive(VELOCITYCHANGE, 0)  # Continua dirigindo para frente se não há obstáculos

            time.sleep(0.1)  # Ajuste conforme necessário para a taxa de verificação dos sensores

    except KeyboardInterrupt:
        print("Programa interrompido pelo usuário.")
    finally:
        if connection is not None:
            connection.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    main()
