import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')

        self.DICT_POSE = {"1": 0.0, "2": 0.0, "3": 0.0, "4": 0.0, "5": 0.0, "6": 0.0, "BRAZO": 0.0}
        self.DICT_POSE_PAST = {"1": 0.0, "2": 0.0, "3": 0.0, "4": 0.0, "5": 0.0, "6": 0.0, "BRAZO": 0.0}
        self.x_ang = 0

        self.subscription_POSE = self.create_subscription(Pose, 'pre_cmd_vel', self.POSE_listener_callback, 10)
        self.subscription_IMU = self.create_subscription(Twist, 'Accel_giro', self.IMU_listener_callback, 10)

        self.publisher_POSE = self.create_publisher(Pose, 'cmd_vel', 10)
        timer_period = 0.5
        self.timer_PUB = self.create_timer(timer_period, self.timer_callback)

        # Parámetros del controlador PID
        self.error_integral = 0.0
        self.error_previo = 0.0
        self.Kp = 1.0  # Coeficiente proporcional
        self.Ki = 0.1  # Coeficiente integral
        self.Kd = 0.5  # Coeficiente derivativo

    def POSE_listener_callback(self, msg):
        self.DICT_POSE["1"] = msg.orientation.x
        self.DICT_POSE["2"] = msg.orientation.y
        self.DICT_POSE["3"] = msg.orientation.z
        self.DICT_POSE["4"] = msg.orientation.w

        self.DICT_POSE["5"] = msg.position.x
        self.DICT_POSE["6"] = msg.position.y
        self.DICT_POSE["BRAZO"] = msg.position.z

    def IMU_listener_callback(self, msg):
        self.x_ang = msg.angular.x

    def control(self):
        self.m_adelante_arriba = "1"
        self.m_atras_arriba = "2"
        self.valor_control = 50

        # Cálculo del controlador PID
        error = self.x_ang
        control_proporcional = self.Kp * error
        self.error_integral += error
        control_integral = self.Ki * self.error_integral
        control_derivativo = self.Kd * (error - self.error_previo)
        señal_control = control_proporcional + control_integral + control_derivativo

        # Actualización de los valores de control en DICT_POSE_PAST
        self.DICT_POSE_PAST[self.m_adelante_arriba] += señal_control
        self.DICT_POSE_PAST[self.m_atras_arriba] -= señal_control

        # Actualizar el error previo
        self.error_previo = error

    def timer_callback(self):
        msg = Pose()
        self.control()

        msg.orientation.x = self.DICT_POSE_PAST["1"]
        msg.orientation.y = self.DICT_POSE_PAST["2"]
        msg.orientation.z = self.DICT_POSE_PAST["3"]
        msg.orientation.w = self.DICT_POSE_PAST["4"]

        msg.position.x = self.DICT_POSE_PAST["5"]
        msg.position.y = self.DICT_POSE_PAST["6"]
        msg.position.z = self.DICT_POSE_PAST["BRAZO"]

        self.publisher_POSE.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()



