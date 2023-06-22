import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from std_msgs.msg import Header, String
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import threading
from std_srvs.srv import Trigger
from my_service_pkg.srv import SetTrajectoryFile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class CombinedNode(Node):

    def __init__(self, graph_title, save_path):
        super().__init__('robot_interface')
        self.publisher_pose = self.create_publisher(PoseStamped, 'robot_pose', 10)
        self.subscription = self.create_subscription(Twist, 'robot_cmdVel', self.cmd_vel_callback, 10)
        self.current_pose = [0, 0, 0]
        self.dt = 0.1
        sns.set_style("whitegrid")
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')
        self.ax.set_title(graph_title)
        self.plot_data = []
        self.plot_line, = self.ax.plot([], [], 'o-')
        self.timer = self.create_timer(self.dt, self.update_plot)
        self.save_path = save_path
        if save_path:
            self.log_file = open(save_path, "w")
        self.file_path_client = self.create_client(SetTrajectoryFile, 'set_trajectory_file')
    def cmd_vel_callback(self, msg):
        linear_x = msg.linear.x
        lateral_y = msg.linear.y
        angular_z = msg.angular.z
        self.current_pose[0] += (linear_x * self.dt * math.cos(self.current_pose[2])) - (lateral_y * self.dt * math.sin(self.current_pose[2]))
        self.current_pose[1] += (linear_x * self.dt * math.sin(self.current_pose[2])) + (lateral_y * self.dt * math.cos(self.current_pose[2]))
        self.current_pose[2] += angular_z * self.dt
        self.publish_pose()
        with open(self.save_path, "a") as self.log_file:
            self.log_file.write(f"{linear_x} {lateral_y} \n")


    def send_trajectory_file(self, file_path):
        if not self.file_path_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('El servicio set_trajectory_file no está disponible')
            return
        request = SetTrajectoryFile.Request()
        request.file_path = file_path
        future = self.file_path_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info('Se envió el nombre del archivo de recorrido: %s' % file_path)
        else:
            self.get_logger().error('Error al enviar el nombre del archivo de recorrido')



    def publish_pose(self):
        pose_msg = PoseStamped()
        pose_msg.header = Header()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.pose.position.x = self.current_pose[0]
        pose_msg.pose.position.y = self.current_pose[1]
        pose_msg.pose.position.z = 0.0
        pose_msg.pose.orientation.x = 0.0
        pose_msg.pose.orientation.y = 0.0
        pose_msg.pose.orientation.z = math.sin(self.current_pose[2]/2)
        pose_msg.pose.orientation.w = math.cos(self.current_pose[2]/2)
        self.publisher_pose.publish(pose_msg)  # Cambiar "publisher" a "publisher_pose"

    def update_plot(self):
        self.plot_data.append((self.current_pose[0], self.current_pose[1]))
        self.plot_line.set_data(*zip(*self.plot_data))
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.set_xlim([min(p[0] for p in self.plot_data) - 1, max(p[0] for p in self.plot_data) + 1])
        self.ax.set_ylim([min(p[1] for p in self.plot_data) - 1, max(p[1] for p in self.plot_data) + 1])
        self.fig.canvas.draw()


    #def on_shutdown(self):
    #    if self.save_path:
    #        self.log_file.close()

def main():
    rclpy.init(args=None)
    node = None
    def on_start_button_click():
        graph_title = graph_title_entry.get()
        save_trajectory = save_trajectory_var.get()
        print("save path entry: ",save_trajectory)
        save_path = None
        if save_trajectory:           
            save_path = save_path_entry.get()
        file_path = file_path_entry.get()
        print("save path entry: ",file_path)

        graph_frame = ttk.Frame(app_window)
        graph_frame.grid(column=0, row=5, columnspan=2, padx=20, pady=20, sticky="nsew")
        app_window.columnconfigure(0, weight=1)
        app_window.rowconfigure(5, weight=1)

        node = CombinedNode(graph_title, save_path)
        canvas = FigureCanvasTkAgg(node.fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        node.send_trajectory_file(file_path)

        def spin():
            rclpy.spin(node)
            node.destroy_node()
            rclpy.shutdown()

        spin_thread = threading.Thread(target=spin)
        spin_thread.start()
        plt.show()

        # def on_shutdown():
        #     if node.save_path:
        #         node.log_file.close()

        #app_window.protocol("WM_DELETE_WINDOW", on_shutdown)

        ttk.Button(app_window, text="Save", command=lambda: save_plot(node)).grid(column=0, row=6, pady=(0, 20))

    app_window = tk.Tk()
    app_window.title("Robot Interface")

    ttk.Label(app_window, text="Graph title:").grid(column=0, row=0, padx=(20, 5), pady=(20, 5), sticky="w")
    graph_title_entry = ttk.Entry(app_window)
    graph_title_entry.grid(column=1, row=0, padx=(5, 20), pady=(20, 5), sticky="we")

    ttk.Label(app_window, text="Save trajectory:").grid(column=0, row=1, padx=(20, 5), pady=(5, 5), sticky="w")
    save_trajectory_var = tk.BooleanVar()
    ttk.Checkbutton(app_window, variable=save_trajectory_var).grid(column=1, row=1, padx=(5, 20), pady=(5, 5), sticky="w")

    ttk.Label(app_window, text="Save path:").grid(column=0, row=2, padx=(20, 5), pady=(5, 5), sticky="w")
    save_path_entry = ttk.Entry(app_window)
    save_path_entry.grid(column=1, row=2, padx=(5, 20), pady=(5, 5), sticky="we")

    ttk.Label(app_window, text="Trajectory file path:").grid(column=0, row=3, padx=(20, 5), pady=(5, 20), sticky="w")
    file_path_entry = ttk.Entry(app_window)
    file_path_entry.grid(column=1, row=3, padx=(5, 20), pady=(5, 20), sticky="we")
    ttk.Button(app_window, text="Start", command=on_start_button_click).grid(column=0, row=4, columnspan=2, pady=(0, 20))

    def save_plot(node):
        file_name = filedialog.asksaveasfilename(defaultextension=".png")
        if file_name:
            node.fig.savefig(file_name)


    # def close_app():
    #     node.on_shutdown()
    #     app_window.quit()
    #     app_window.destroy()
    #     rclpy.shutdown()

    save_button = ttk.Button(app_window, text="Save", command=save_plot)
    save_button.grid(column=0, row=6, columnspan=2, pady=(0, 20))

    #close_button = ttk.Button(app_window, text="Close", command=close_app)
    #close_button.grid(column=0, row=7, columnspan=2, pady=(0, 20))

    app_window.columnconfigure(1, weight=1)
    app_window.rowconfigure(0, weight=1)
    app_window.rowconfigure(1, weight=1)
    app_window.rowconfigure(2, weight=1)
    app_window.rowconfigure(3, weight=1)
    app_window.rowconfigure(6, weight=1)
    app_window.rowconfigure(7, weight=1)

    app_window.mainloop()

    app_window.mainloop()


if __name__ == '__main__':
    main()




