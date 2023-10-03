#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose


MAX_BUFF_LEN  = 255
ZERO = 1500.0
VELRIGHT_Z = 1200.0
VELRIGHT = 1400.0
VELLEFT = 1600.0    
VELLEFT_Z = 1800.0
ABRIR_IZQ = 1.0
ABRIR_DER = 2.0
CERRAR_IZQ = -1.0
CERRAR_DER = -2.0

class Ds4Control(Node):

    buttons = []
    axes = []

    def __init__(self):

        super().__init__("conversor")
        self.submarine = [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO]
        
        self.subscription = self.create_subscription(
            Joy,
            '/joy',
            self.listener_callback,
            10
        )

        self.publisher_ = self.create_publisher(Pose, '/cmd_vel', 10)

        self.flag = 0


    def listener_callback(self, msg):

        poseMessage = Pose()
        self.buttons = msg.buttons
        self.axes = msg.axes      


        self.submarine[0] = ZERO # Atras izquierda
        self.submarine[1] = ZERO # Arriba izquierda
        self.submarine[2] = ZERO # Adelante izquierda
        self.submarine[3] = ZERO # Adelante derecha
        self.submarine[4] = ZERO # Arriba derecha
        self.submarine[5] = ZERO # Atras derecha
        self.submarine[6] = ZERO # Garra izquierda / Garra derecha

        if self.axes[6] > 0: # Izquierda

            self.submarine[0] = VELLEFT
            self.submarine[3] = VELLEFT
            self.submarine[5] = VELRIGHT
            self.submarine[6] = VELLEFT

        if self.axes[6] < 0: # Derecha

            self.submarine[0] = VELRIGHT
            self.submarine[3] = VELRIGHT
            self.submarine[5] = VELLEFT
            self.submarine[6] = VELRIGHT
            
        if self.axes[7] > 0: # Adelante

            self.submarine[0] = VELRIGHT
            self.submarine[3] = VELLEFT
            self.submarine[5] = VELRIGHT
            self.submarine[6] = VELRIGHT

        if self.axes[7] < 0: # Atrás

            self.submarine[0] = VELLEFT
            self.submarine[3] = VELRIGHT
            self.submarine[5] = VELLEFT
            self.submarine[6] = VELLEFT
            

        if self.buttons[0] > 0: # Bajar

            self.submarine[1] = VELRIGHT_Z
            self.submarine[4] = VELRIGHT_Z

        if self.buttons[2] > 0: # Subir

            self.submarine[1] = VELLEFT_Z
            self.submarine[4] = VELLEFT_Z
            
        if self.buttons[4] > 0: # Abrir garra izquierda

            self.submarine[6] = ABRIR_IZQ #eva

        if self.buttons[5] > 0: # Abrir garra derecha

            self.submarine[6] = ABRIR_DER #eva

        if self.buttons[6] > 0: # Cerrar garra izquierda

            self.submarine[6] = CERRAR_IZQ #eva

        if self.buttons[7] > 0: # Cerrar garra derecha

            self.submarine[6] = CERRAR_DER #eva

        poseMessage.position.x = self.submarine[0]
        poseMessage.position.y = self.submarine[1]
        poseMessage.position.z = self.submarine[2]  
        poseMessage.orientation.x = self.submarine[3]
        poseMessage.orientation.y = self.submarine[4]
        poseMessage.orientation.z = self.submarine[5]
        poseMessage.orientation.w = self.submarine[6]

        self.publisher_.publish(poseMessage)

def main(args = None):
    rclpy.init(args = args)

    node = Ds4Control()
    node.create_rate(1)
    rclpy.spin(node)
    rclpy.shutdown()

    
if __name__ == '__main__':

    main()