import struct
import serial
import time

# Configurações de comunicação e movimento
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
TIMEOUT = 1
VELOCITYCHANGE = 300
ROTATIONCHANGE = 300

# Inicializa a conexão serial
connection = serial.Serial(PORT, baudrate=BAUDRATE, timeout=TIMEOUT)

def sendCommandRaw(command):
    global connection
    if connection is not None:
        connection.write(command)
        connection.flush()

def drive(velocity, rotation):
    vr = int(velocity + (rotation / 2))
    vl = int(velocity - (rotation / 2))
    cmd = struct.pack(">Bhh", 145, vr, vl)
    sendCommandRaw(cmd)

def stop():
    drive(0, 0)

def checkObstacles():
    # Aqui reutilizamos a função existente para verificar obstáculos
    pass

# Função para movimentar o robô conforme a detecção da posição da pessoa
def move_towards_person(person_x, frame_center_x):
    if person_x < frame_center_x - 50:  # Se a pessoa estiver à esquerda
        drive(0, ROTATIONCHANGE)  # Gira para a esquerda
    elif person_x > frame_center_x + 50:  # Se a pessoa estiver à direita
        drive(0, -ROTATIONCHANGE)  # Gira para a direita
    else:
        drive(VELOCITYCHANGE, 0)  # Move para frente

def close_connection():
    if connection is not None:
        connection.close()
