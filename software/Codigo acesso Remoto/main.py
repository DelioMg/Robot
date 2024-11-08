from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2
import serial
import struct
import sys
import glob

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
port = '/dev/ttyUSB0'
baudrate=115200 
timeout=1

# Variaveis Goblais 
connection = None
VELOCITYCHANGE = 200  # Velocidade de locomoção
ROTATIONCHANGE = 300  # Velocidade de Rotação
camera = cv2.VideoCapture(0)  # Abre camera principal

class TetheredDriveApp:
    def __init__(self):
        self.callbackKeyUp = False
        self.callbackKeyDown = False
        self.callbackKeyLeft = False
        self.callbackKeyRight = False
        self.callbackKeyLastDriveCommand = ''
        self.setup_serial_connection()

    def setup_serial_connection(self):
        global connection
        if connection is not None:
            connection.close()
        try:
            
            print("Tentando conectar à porta", port)
            connection = serial.Serial(port, baudrate, timeout)
            print("Conectado com sucesso!")

            # Coloca o robô no modo passivo e depois no modo seguro
            print("Entrando no modo passivo...")
            self.sendCommandASCII('128') #Modo passivo(128)
            print("Entrando no Modo seguro...")
            self.sendCommandASCII('131') #Modo seguro (131)
            print("Modo seguro ativado!")

        except Exception as e:
            print("Falha ao Conectar")
            connection = None

    def sendCommandASCII(self, command):
        cmd = bytes([int(v) for v in command.split()])
        self.sendCommandRaw(cmd)

    def sendCommandRaw(self, command):
        global connection
        try:
            if connection is not None:
                assert isinstance(command, bytes), 'Command must be of type bytes'
                connection.write(command)
                connection.flush()
            else:
                print("Nao esta conectado.")
        except serial.SerialException:
            print("conexao perdida")
            connection = None

    def getDecodedBytes(self, n, fmt):
        global connection
        try:
            return struct.unpack(fmt, connection.read(n))[0]
        except serial.SerialException:
            print("conexao perdida")
            connection = None
            return None
        except struct.error:
            print("Got unexpected data from serial port.")
            return None

    def get8Unsigned(self):
        return self.getDecodedBytes(1, "B")

    def get8Signed(self):
        return self.getDecodedBytes(1, "b")

    def get16Unsigned(self):
        return self.getDecodedBytes(2, ">H")

    def get16Signed(self):
        return self.getDecodedBytes(2, ">h")

    def handle_key_command(self, command):
        motionChange = False
        print(f"Comando para movimentação: {command}") #Depuração de codigos mandados para robo
        if command == 'P':
            self.sendCommandASCII('128')
        elif command == 'S':
            self.sendCommandASCII('131')
        elif command == 'F':
            self.sendCommandASCII('132')
        elif command == 'C':
            self.sendCommandASCII('135')
        elif command == 'D':
            self.sendCommandASCII('143')
        elif command == 'SPACE':
            self.sendCommandASCII('140 3 1 64 16 141 3')
        elif command == 'R':
            self.sendCommandASCII('7')
        elif command == 'UP':
            self.callbackKeyUp = True
            motionChange = True
        elif command == 'DOWN':
            self.callbackKeyDown = True
            motionChange = True
        elif command == 'LEFT':
            self.callbackKeyLeft = True
            motionChange = True
        elif command == 'RIGHT':
            self.callbackKeyRight = True
            motionChange = True
        elif command == 'UP_RELEASE':
            self.callbackKeyUp = False
            motionChange = True
        elif command == 'DOWN_RELEASE':
            self.callbackKeyDown = False
            motionChange = True
        elif command == 'LEFT_RELEASE':
            self.callbackKeyLeft = False
            motionChange = True
        elif command == 'RIGHT_RELEASE':
            self.callbackKeyRight = False
            motionChange = True

        if motionChange:
            print(f"Movimento alterado: Up={self.callbackKeyUp}, Down={self.callbackKeyDown}, Left={self.callbackKeyLeft}, Right={self.callbackKeyRight}")
            velocity = 0
            velocity += VELOCITYCHANGE if self.callbackKeyUp else 0
            velocity -= VELOCITYCHANGE if self.callbackKeyDown else 0
            rotation = 0
            rotation += ROTATIONCHANGE if self.callbackKeyLeft else 0
            rotation -= ROTATIONCHANGE if self.callbackKeyRight else 0

            vr = int(velocity + (rotation / 2))
            vl = int(velocity - (rotation / 2))

            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd

    def getSerialPorts(self):
        """Lists serial ports"""
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result    

tethered_drive_app = TetheredDriveApp()

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('command')
def handle_command(data):
    command = data.get('command', '')
    print(f"Comando recebido: {command}")# Depuração do comando recebido do socketio
    if command:
        tethered_drive_app.handle_key_command(command)
        emit('response', {'status': 'success', 'command': command})
    else:
        emit('response', {'status': 'failure', 'message': 'No command received'})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
