import rclpy
from rclpy.node import Node
from my_service_pkg.srv import SetTrajectoryFile
from std_srvs.srv import Trigger
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import time

class TrajectoryReplayer(Node):

    def __init__(self):
        super().__init__('robot_player')
        self.rutinas_subscriber = self.create_subscription(String, 'rutinas', self.rutinas_callback, 10)
        self.publisher = self.create_publisher(String, 'manipulator_ang', 10)
        self.dt = 0.5 # update frequency, debe coincidir con el utilizado en el RobotPositionTracker
        #self.dt = 2 # update frequency, debe coincidir con el utilizado en el RobotPositionTracker

    def rutinas_callback(self, msg):
        file_path = msg.data
        print(f"Archivo recibido: {file_path}")
        print(file_path)
        #response.message = f"Archivo de trayectoria establecido en {self.file_path}"
        with open(file_path, 'r') as file:
            for line in file:
                msg = String()
                msg.data=line
                print(msg.data)
                self.publisher.publish(msg)
                time.sleep(self.dt)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryReplayer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
