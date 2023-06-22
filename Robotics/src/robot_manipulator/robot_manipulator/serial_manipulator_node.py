#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np
import serial
import time  # Importa la librería time
from std_msgs.msg import String


class SerialTester(Node):
    def __init__(self):
        print("spiderman")
        super().__init__('serial_brazo')

        # Conectar a través de la conexión serial
        self.serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.serial.flush()
        self.pub = self.create_publisher(String, 'esp32_response', 10)
        self.contador = 0  # Inicializa el contador

        # Crear un subscriptor al tópico "robot_cmdVel"
        self.subscription = self.create_subscription(
            String,
            'manipulator_ang',
            self.cmd_vel_callback,
            10)

    # ...
    

    def calculate_angles(x, y, l1=0.19, l2=0.11):
        # Calcular la distancia al punto objetivo
        d = np.sqrt(x**2 + y**2)

        # Asegurarse de que el punto objetivo está al alcance del brazo
        if d > l1 + l2:
            raise ValueError("El punto objetivo está fuera del alcance del brazo")

        # Calcular los ángulos utilizando la ley del coseno
        theta2 = np.arccos((d**2 - l1**2 - l2**2) / (2 * l1 * l2))
        theta1 = np.arctan2(y, x) - np.arctan2(l2 * np.sin(theta2), l1 + l2 * np.cos(theta2))

        # Convertir los ángulos a grados
        theta1, theta2 = np.degrees([theta1, theta2])

        return theta1, theta2

    def cmd_vel_callback(self, msg):
        if ( "\n"in msg.data):
            msg.data = msg.data.replace("\n","")
        
        self.contador += 1  # Incrementa el contador
        start_time = time.time()  # Guarda el tiempo actual
        #pinza
        if msg.data == "z":
            self.serial.write(b'5')
            print("5")
        elif msg.data == "x":
            self.serial.write(b'6')
            print("6")
        #negro
        elif msg.data == "u":
            print("hola")
            self.serial.write(b'7')
            print("7")
        elif msg.data == "o":
            self.serial.write(b'8')
            print("8")
        #rojo
        elif msg.data == "i":
            self.serial.write(b'9')
            print("9")
        elif msg.data == "k":
            self.serial.write(b'10')
            print("10")
        #base
        elif msg.data == "j":
            self.serial.write(b'11')
            print("11")
        elif msg.data == "l":
            self.serial.write(b'12')
            print("12")
        
        
        # Lee la respuesta de la ESP32
        response = self.serial.readline().decode('utf-8').rstrip()
        elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
        print("Tiempo de respuesta: {:.2f} segundos".format(elapsed_time))
        print("Respuesta de ESP32: {}".format(response))
        print("Respuesta de ESP32: {}".format(response))

def main(args=None):
    rclpy.init(args=args)
    serial_tester = SerialTester()

    # Mantener el nodo activo
    rclpy.spin(serial_tester)

    # Destruir el nodo y cerrar la conexión serial
    serial_tester.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
