import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3
import random

class PositionPublisher(Node):

    def __init__(self):
        super().__init__('position_publisher')
        self.publisher_ = self.create_publisher(Vector3, 'robot_manipulator_position', 10)
        self.timer_period = 0.5  # segundos
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Vector3()
        msg.x = random.uniform(-10, 10)  # Genera un número aleatorio entre -10 y 10
        msg.y = random.uniform(-10, 10)  # Genera un número aleatorio entre -10 y 10
        msg.z = random.uniform(-10, 10)  # Genera un número aleatorio entre -10 y 10
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)

def main(args=None):
    rclpy.init(args=args)

    position_publisher = PositionPublisher()

    try:
        rclpy.spin(position_publisher)
    except KeyboardInterrupt:
        pass  # Permitir que Ctrl-C detenga el proceso

    position_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
