import rclpy
from rclpy.node import Node
from my_service_pkg.srv import SetTrajectoryFile
from std_srvs.srv import Trigger
from geometry_msgs.msg import Twist
import time

class TrajectoryReplayer(Node):

    def __init__(self):
        super().__init__('robot_player')
        self.publisher = self.create_publisher(Twist, 'manipulator_ang', 10)
        self.file_path = None
        self.dt = 2 # update frequency, debe coincidir con el utilizado en el RobotPositionTracker

        # crea el servicio que permite reproducir el archivo de recorrido
        self.service = self.create_service(SetTrajectoryFile, 'set_trajectory_file', self.set_trajectory_file_callback)


    def set_trajectory_file_callback(self, request, response):
        self.file_path = request.file_path
        print(self.file_path)
        response.success = True
        #response.message = f"Archivo de trayectoria establecido en {self.file_path}"
        with open(self.file_path, 'r') as file:
            for line in file:
                twist_msg = Twist()
                linear_x, lateral_y = map(float, line.strip().split())
                twist_msg.linear.x = linear_x
                twist_msg.linear.y = lateral_y

                self.publisher.publish(twist_msg)
                time.sleep(self.dt)

        response.success = True
        return response

 

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

