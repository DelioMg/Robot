import struct
import serial
import time

# Configurações de comunicação
PORT = '/dev/ttyUSB0'  
BAUDRATE = 115200
TIMEOUT = 1

# Configurações de movimento
VELOCITYCHANGE = 200 # Velocidade de Movimentação frente e tras
ROTATIONCHANGE = 300 # Velocidade de Giro do robo

# Limite de bateria baixa
LOW_BATTERY_THRESHOLD = 0.10  # 10%

# Inicializa a conexão serial
try:
    connection = serial.Serial(PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    print("Conectado com sucesso")
except serial.SerialException:
    print("Falha ao se conectar.")
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

def stop():
    drive(0, 0)  # Para o robô enviando velocidade zero para frente/trás e rotação

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

# Função para verificar o nível da bateria
def checkBatteryLevel():
    global connection
    if connection is not None:
        sendCommandASCII('142 25')  # Solicita a carga da bateria (Packet ID 25)
        battery_charge_data = connection.read(2)
        sendCommandASCII('142 26')  # Solicita a capacidade total da bateria (Packet ID 26)
        battery_capacity_data = connection.read(2)

        if battery_charge_data and battery_capacity_data:
            battery_charge = struct.unpack('>H', battery_charge_data)[0]  # Carga da bateria
            battery_capacity = struct.unpack('>H', battery_capacity_data)[0]  # Capacidade total

            if battery_capacity > 0:
                battery_percentage = battery_charge / battery_capacity
                print(f"Nível da bateria: {battery_percentage * 100:.2f}%")
                if battery_percentage < LOW_BATTERY_THRESHOLD:
                    playLowBatteryTone()  # Toca o aviso de bateria baixa
                return battery_percentage
    return None

# Definições de tons
def defineTones():
    sendCommandASCII('140 0 4 72 16 76 16 79 16 83 16')  # Toque de inicialização
    sendCommandASCII('140 1 4 60 16 64 16 67 16 72 16')  # Toque de desligar
    sendCommandASCII('140 2 1 55 32')  # Toque de obstáculo
    sendCommandASCII('140 3 1 69 32')  # Toque de buzina - nota A4 com duração de 0.5 segundos
    sendCommandASCII('140 4 2 60 32 55 32')  # Toque de bateria baixa - duas notas


def playStartupTone():
    sendCommandASCII('141 0')  # Toca o tom de Inicialização (música 0)

def playPowerOffTone():
    sendCommandASCII('141 1')  # Toca o tom de Desligamento (música 1)

def playObstacleTone():
    sendCommandASCII('141 2')  # Toca o tom de obstáculo (música 2)

def playHorn():
    sendCommandASCII('141 3')  # Toca a buzina (música 3)

def playLowBatteryTone():
    sendCommandASCII('141 4')  # Avisa Bateria Baixa (música 4)

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

# Função principal
def main():
    setPassiveMode()
    time.sleep(1)
    setSafeMode()
    defineTones()
    playStartupTone()

    try:
            print("Precione 1 para modo Passivo, 2 para modo Full, 3 modo SafeMode, 4 ClearMode e 5 para Dockmode.")
            print("Precione Espaço para buzina e R para Resetar e Q para sair.")
            print("Precione W/A/S/D para Movimentar: ")
    
            while True:
                # Verifica continuamente a presença de obstáculos
                if checkObstacles():
                    #drive(-VELOCITYCHANGE, 0)  # Move para trás
                    time.sleep(0.5)  # Espera 1 segundo após detectar um obstáculo antes de continuar
                    stop()
                    continue  # Volta para o loop sem processar mais comandos enquanto o obstáculo não for resolvido

                # Verifica o nível da bateria continuamente
                checkBatteryLevel()

                command = input("Insira").strip().lower()
                if command == 'w':
                    drive(VELOCITYCHANGE, 0)
                    stop()
                elif command == 's':
                    drive(-VELOCITYCHANGE, 0)
                    stop()
                elif command == 'a':
                    drive(0, ROTATIONCHANGE)
                    stop()
                elif command == 'd':
                    drive(0, -ROTATIONCHANGE)
                    stop()
                elif command == '1':
                    setPassiveMode()
                elif command == '2':
                    setFullMode()
                elif command == '3':
                    setSafeMode()    
                elif command == '4':
                    clean()
                elif command == '5':
                    dock()
                elif command == 'r':
                    reset()
                elif command == 'space':
                    playHorn()
                elif command == 'q':
                    break
                else:
                    print("Comando não reconhecido.")

    except KeyboardInterrupt:
        print("Programa interrompido pelo usuário.")
        playPowerOffTone()
    finally:
        if connection is not None:
            connection.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    main()
