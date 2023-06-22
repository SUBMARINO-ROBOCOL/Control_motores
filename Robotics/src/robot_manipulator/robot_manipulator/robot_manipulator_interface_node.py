import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog

class PositionSubscriber(Node):

    def __init__(self):
        super().__init__('position_subscriber')
        self.subscription = self.create_subscription(
            Vector3,
            'robot_manipulator_position',
            self.listener_callback,
            10)
        self.title = ""
        self.subscription
        self.position_list = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def listener_callback(self, msg):
        self.add_position(msg)

    def add_position(self, position):
        self.position_list.append(position)
    def reset_positions(self):
        self.position_list = []
        self.ax.cla()  # limpia la gráfica
        self.ax.set_title(self.title)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

    

class Application(tk.Tk):
    def __init__(self, node):
        tk.Tk.__init__(self)
        self.node = node
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = FigureCanvasTkAgg(node.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.title_entry = tk.Entry(self)
        self.title_entry.pack()
        self.reset_button = tk.Button(self, text='Reset', command=self.reset)
        self.reset_button.pack()
        self.set_title_button = tk.Button(self, text='Set title', command=self.set_title)
        self.reset_button= tk.Button(self, text='Reset', command=self.reset)
        self.set_title_button.pack()
        self.save_button = tk.Button(self, text='Save figure', command=self.save_fig)
        self.save_button.pack()
        self.update_plot()

    def set_title(self):
        self.node.title = self.title_entry.get()  # Guarda el título en la variable
        self.node.ax.set_title(self.node.title)  # Establece el título en el gráfico
        self.canvas.draw()

    def save_fig(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png')
        if file_path:
            self.node.fig.savefig(file_path)

    def update_plot(self):
        rclpy.spin_once(self.node)
        if self.node.position_list:
            self.node.ax.clear()
            self.node.ax.set_title(self.node.title) 
            x_list = [p.x for p in self.node.position_list]
            y_list = [p.y for p in self.node.position_list]
            z_list = [p.z for p in self.node.position_list]
            self.node.ax.scatter(x_list, y_list, z_list, c='r', marker='o')
            self.node.ax.set_xlabel('X')
            self.node.ax.set_ylabel('Y')
            self.node.ax.set_zlabel('Z')
            self.canvas.draw()
        self.after(500, self.update_plot)

    def on_closing(self):
        self.node.destroy_node()
        rclpy.shutdown()
        self.quit()
    def reset_positions(self):
        self.position_list = []
        self.ax.cla()  # limpia la gráfica
        self.ax.set_title(self.title)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
    def reset(self):
        print("reseteando...")
        self.node.reset_positions()
        self.canvas.draw()
def main(args=None):
    rclpy.init(args=args)
    position_subscriber = PositionSubscriber()

    app = Application(position_subscriber)
    app.mainloop()

    position_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
