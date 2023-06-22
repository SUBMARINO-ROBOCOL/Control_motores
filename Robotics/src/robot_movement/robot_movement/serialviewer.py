import rclpy
from rclpy.node import Node
import serial

class ESP32SerialNode(Node):
    def __init__(self):
        super().__init__('esp32_serial_node')
        self.get_logger().info('ESP32 Serial Node has been started.')

        # Parámetros de configuración del puerto serie
        port = '/dev/ttyUSB0'  # Ajusta esto al puerto correcto en tu sistema
        baudrate = 115200

        # Inicializar la conexión serie
        self.ser = serial.Serial(port, baudrate)
        self.timer = self.create_timer(0.1, self.read_from_serial)  # Ajusta la frecuencia de lectura según sea necesario

    def read_from_serial(self):
        if self.ser.in_waiting:
            received_data = self.ser.readline().decode('utf-8').rstrip()
            self.get_logger().info(f'Received: {received_data}')

def main(args=None):
    rclpy.init(args=args)
    esp32_serial_node = ESP32SerialNode()
    rclpy.spin(esp32_serial_node)

    esp32_serial_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
