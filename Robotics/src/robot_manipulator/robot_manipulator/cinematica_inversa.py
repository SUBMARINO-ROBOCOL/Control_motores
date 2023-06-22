#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np
import serial
import time
import time  # Importa la librería time
from std_msgs.msg import String


class inverseKinect(Node):
    def __init__(self):
        super().__init__('inverse')

        # Conectar a través de la conexión serial
        self.serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.serial.flush()
        self.pub = self.create_publisher(String, 'esp32_response', 10)
        self.contador = 0  # Inicializa el contador



    def calculate_angles(self, x, y, l1=0.19, l2=0.11):
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

        # Ajustar el ángulo de la segunda articulación para que sea relativo a la primera articulación
        theta2 -= theta1

        return theta1, theta2


    def mover_brazo(self,angle1,angle2):
        angle1, angle2 = int(angle1), int(angle2)
        message = f"{angle1}"
        # Envia el mensaje
        self.serial.write(message.encode())
        response = self.serial.readline().decode('utf-8').rstrip()
        print("Respuesta de ESP32: {}".format(response))
        print("Respuesta de ESP32: {}".format(response))
        response = self.serial.readline().decode('utf-8').rstrip()
        print("Respuesta de ESP32: {}".format(response))
        print("Respuesta de ESP32: {}".format(response))
        message = f"{angle2}"
        self.serial.write(message.encode())
        # Lee la respuesta de la ESP32
        response = self.serial.readline().decode('utf-8').rstrip()
        print("Respuesta de ESP32: {}".format(response))
        print("Respuesta de ESP32: {}".format(response))
        response = self.serial.readline().decode('utf-8').rstrip()
        print("Respuesta de ESP32: {}".format(response))
        print("Respuesta de ESP32: {}".format(response))


def main(args=None):
    rclpy.init(args=args)
    serial_tester = inverseKinect()
    
    
    x=float(input("Ingrese el valor de la posicion x en metros"))
    y=float(input("Ingrese el valor de la posicion y en metros"))
    theta1, theta2 =serial_tester.calculate_angles(x,y)
    print("para la posicion ",x,y,"se calcularon los angulios: ",theta1,theta2 )
    serial_tester.mover_brazo(theta1,theta2)

    
    

    # Mantener el nodo activo
    rclpy.spin(serial_tester)

    # Destruir el nodo y cerrar la conexión serial
    serial_tester.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
