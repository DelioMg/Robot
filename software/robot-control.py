import struct
import serial
import time

# Configurações de comunicação
PORT = '/dev/ttyUSB0'  
BAUDRATE = 115200
TIMEOUT = 1

# Configurações de movimento
VELOCITYCHANGE = 200
ROTATIONCHANGE = 300

# Inicializa a conexão serial
try:
    connection = serial.Serial(PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    print("Conectado ao iRobot Create 2!")
except serial.SerialException:
    print("Falha na conexão com o iRobot Create 2.")
    connection = None

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

def readSensors():
    global connection
    if connection is not None:
        sendCommandASCII('142 7')  # Solicita dados do pacote de colisões e quedas de roda (Packet ID 7)
        data = connection.read(1)
        if data:
            return struct.unpack('B', data)[0]
    return None

def checkObstacles():
    sensor_data = readSensors()
    if sensor_data is not None:
        bump_right = sensor_data & 0x01
        bump_left = sensor_data & 0x02
        wheel_drop_right = sensor_data & 0x04
        wheel_drop_left = sensor_data & 0x08
        if bump_right or bump_left or wheel_drop_right or wheel_drop_left:
            print("Obstáculo detectado! Parando o robô.")
            drive(0, 0)
            playObstacleTone()  # Emite um beep quando um obstáculo é detectado
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

# Definições de tons
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
            if checkObstacles():
                time.sleep(1)  # Espera 1 segundo antes de continuar para evitar colisões repetidas
                continue

            command = input("Enter command (w/a/s/d for movement, q to quit): ").strip().lower()
            if command == 'w':
                drive(VELOCITYCHANGE, 0)
            elif command == 's':
                drive(-VELOCITYCHANGE, 0)
            elif command == 'a':
                drive(0, ROTATIONCHANGE)
            elif command == 'd':
                drive(0, -ROTATIONCHANGE)
            elif command == 'p':
                setPassiveMode()
            elif command == 'f':
                setFullMode()
            elif command == 'c':
                clean()
            elif command == 'd':
                dock()
            elif command == 'r':
                reset()
            elif command == 'b':
                playObstacleTone()
            elif command == 'q':
                break
            else:
                print("Comando não reconhecido.")

    except KeyboardInterrupt:
        print("Programa interrompido pelo usuário.")
    finally:
        if connection is not None:
            connection.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    main()
