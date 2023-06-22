#importar los tres srv
from proyecto_interfaces.srv import StartNavigationTest
from proyecto_interfaces.srv import StartPerceptionTest
from proyecto_interfaces.srv import StartManipulationTest
#librerias usadas
import rclpy
from std_msgs.msg import String
from rclpy.node import Node


class TestService(Node):
    def __init__(self):
        super().__init__('test_service')
        self.perception_srv = self.create_service(StartPerceptionTest, '/group_6/start_perception_test_srv', self.perception_test_callback)
        self.navigation_srv = self.create_service(StartNavigationTest, '/group_6/start_navigation_test_srv', self.navigation_test_callback)
        self.manipulation_srv = self.create_service(StartManipulationTest, '/group_6/start_manipulation_test_srv', self.manipulation_test_callback)
        self.rutinas_publisher = self.create_publisher(String, 'rutinas', 10)

    def perception_test_callback(self, request, response):
        # Aquí es donde procesarías la solicitud y generas la respuesta
        # Por ahora, vamos a simular las coordenadas de los banners
        banner_a_coords = (10, 20)
        banner_b_coords = (30, 40)
        if (str(request.banner_a) =="1" and str(request.banner_b) =="2") or (str(request.banner_a) =="2" and str(request.banner_b) =="1"):
            msg = String()
            msg.data = "12.csv"
        if (str(request.banner_a) =="1" and str(request.banner_b) =="3") or (str(request.banner_a) =="3" and str(request.banner_b) =="1"):
            msg = String()
            msg.data = "13.csv"
        if (str(request.banner_a) =="3" and str(request.banner_b) =="2") or (str(request.banner_a) =="2" and str(request.banner_b) =="3"):
            msg = String()
            msg.data = "32.csv"
        self.rutinas_publisher.publish(msg)
        response.answer = f"Debo identificar el banner {request.banner_a} que se encuentra en las coordenadas {banner_a_coords} y el banner {request.banner_b} que se encuentra en las coordenadas {banner_b_coords}."
        self.get_logger().info(response.answer)

        return response

    def navigation_test_callback(self, request, response):
        # Aquí es donde procesarías la solicitud y generas la respuesta
        # Por ahora, vamos a suponer que el servicio siempre se aprueba
        response.answer = "True"
        msg = String()
        msg.data = "navegacion1.csv"
        self.rutinas_publisher.publish(msg)
        self.get_logger().info(response.answer)
        
        return response

    def manipulation_test_callback(self, request, response):
        # Aquí es donde procesarías la solicitud y generas la respuesta
        # Por ahora, vamos a suponer que la ficha siempre se encuentra y se lleva a la plataforma
        otra=""
        print(type(request.platform))
        if str(request.platform) =="platform_1":
            msg = String()
            msg.data = "brazo1.csv"
            self.rutinas_publisher.publish(msg)
            otra=2
        else:
            msg = String()
            msg.data = "brazo2.csv"
            self.rutinas_publisher.publish(msg)
            otra=1

        response.answer = f"La ficha de tipo {request.x} se encuentra en la plataforma {request.platform} y la llevaré a la plataforma {otra}."
        self.get_logger().info(response.answer)
        return response

def main(args=None):
    rclpy.init(args=args)

    test_service = TestService()

    rclpy.spin(test_service)

    test_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
