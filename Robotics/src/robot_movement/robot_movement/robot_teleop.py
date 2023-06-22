#!/usr/bin/env python3

import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from pynput import keyboard
from rclpy.node import Node
from PIL import ImageTk, Image
import tkinter as tk
import os




class Publicador(Node):

    def __init__(self):
        super().__init__('robot_teleop')
        self.publisher_ = self.create_publisher(Twist, 'robot_cmdVel', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.movement = Twist()
        self.presionado=False
        #por defecto la velocidades son 1 
        self.angular_value = 1.0
        self.linear_value = 1.0

        # Crear ventana de tkinter para la interfaz de movimiento
        self.root = tk.Tk()
        self.root.title("Robot Teleop")
        self.root.geometry("500x500")

        #mportar imagen de fondo
        ruta_imagen = os.path.abspath("imagen_de_fondo.jpg")
        image = Image.open(ruta_imagen)
        image = image.resize((500, 500), Image.ANTIALIAS) # Redimensionar la imagen
        bg_image = ImageTk.PhotoImage(image)
        # Crear un Label con la imagen de fondo
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

       

        # Crear marcos para los botones de movimiento y establecer la imagen de fondo
        self.defaultbg = self.root.cget('bg')
        movement_frame = tk.Frame(self.root, bg=self.defaultbg)
        movement_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
        movement_frame.grid_columnconfigure(0, weight=1)
        movement_frame.grid_columnconfigure(1, weight=1)
        movement_frame.grid_columnconfigure(2, weight=1)
        movement_frame.grid_rowconfigure(0, weight=1)
        movement_frame.grid_rowconfigure(1, weight=1)
        

        bg_label = tk.Label(movement_frame, image=bg_image)
        bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Crear botones de movimiento y hacerlos transparentes
        
        self.w_button = tk.Button(movement_frame, text="W", width=5, height=5, command=lambda:self.forward(self,self.w_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.a_button = tk.Button(movement_frame, text="A", width=5, height=5, command=lambda:self.left(self,self.a_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.s_button = tk.Button(movement_frame, text="S", width=5, height=5, command=lambda:self.backward(self,self.s_button), highlightthickness=0,bg='#191970', fg='white', font=('Arial', 16))
        self.d_button = tk.Button(movement_frame, text="D", width=5, height=5, command=lambda:self.right(self,self.d_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))

        self.w_button.grid(row=0, column=1)
        self.a_button.grid(row=1, column=0) 
        self.s_button.grid(row=1, column=1)
        self.d_button.grid(row=1, column=2)
                             


        # Asociar teclas del teclado con los botones de movimiento
        self.root.bind('<KeyPress-w>', lambda event: self.w_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-a>', lambda event: self.a_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-s>', lambda event: self.s_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-d>', lambda event: self.d_button.config(relief=tk.SUNKEN))

        self.root.bind('<KeyRelease-w>', lambda event: self.w_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-a>', lambda event: self.a_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-s>', lambda event: self.s_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-d>', lambda event: self.d_button.config(relief=tk.RAISED))

        # Iniciar listener de teclado
        self.key_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.key_listener.start()
        self.root.mainloop()

        
    def forward(self):
        button=self.w_button
        self.movement.linear.x = self.linear_value
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def backward(self):
        button=self.s_button
        self.movement.linear.x = -(self.linear_value)
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def left(self):
        button=self.a_button
        self.movement.linear.y = self.linear_value
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def right(self):
        button=self.d_button
        self.movement.linear.y =  -self.linear_value
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')
    def unforward(self):
        button=self.w_button
        self.movement.linear.x = 0.0
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def unbackward(self):
        button=self.s_button
        self.movement.linear.x = 0.0
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def unleft(self):
        button=self.a_button
        self.movement.linear.y  = 0.0
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def unright(self):
        button=self.d_button
        self.movement.linear.y  = 0.0
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')


    def custom_cmd(self, cmd):
        self.get_logger().info('Custom command received: "%s"' % cmd)
        # Aquí puedes implementar lo que quieras que haga el robot cuando reciba un comando personalizado

    def on_press(self, key):
        try:
            # Mapear teclas de flechas a comandos de movimiento
            if key.char == 'w' and (not self.presionado):
                self.presionado=True
                self.forward()
            elif key.char == 's'and (not self.presionado):
                self.presionado=True
                self.backward()

            elif key.char == 'a'and (not self.presionado):
                self.presionado=True
                self.left()
            elif key.char == 'd'and (not self.presionado):
                self.presionado=True
                self.right()
            else:
                # Si se presiona cualquier otra tecla, tomar el comando personalizado de la entrada de texto
                cmd = self.custom_cmd_entry.get()
                self.custom_cmd(cmd)
        except AttributeError:
            # Ignorar teclas de modificación (Shift, Ctrl, Alt, etc.)
            pass

    def on_release(self, key):
        # Detener el movimiento al soltar cualquier tecla de movimiento
        try:
            if key.char == 'w'and (self.presionado):
                self.presionado=False
                self.unforward()
            elif key.char == 's'and (self.presionado):
                self.presionado=False
                self.unbackward()
            elif key.char == 'a'and ( self.presionado):
                self.presionado=False
                self.unleft()
            elif key.char == 'd'and ( self.presionado):
                self.presionado=False
                self.unright()
        except AttributeError:
            # Ignorar teclas de modificación (Shift, Ctrl, Alt, etc.)
            pass

    def timer_callback(self):
        print(self.linear_speed_entry)
        print(self.angular_speed_entry)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)     
    publicador = Publicador()

    rclpy.spin(publicador)

    publicador.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
    print("¡El programa se ha ejecutado correctamente!")
