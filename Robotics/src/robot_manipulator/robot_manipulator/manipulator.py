#!/usr/bin/env python3

import numpy as np
import rclpy
from std_msgs.msg import String
from pynput import keyboard
from rclpy.node import Node
from PIL import ImageTk, Image
import tkinter as tk
from geometry_msgs.msg import Vector3
import os
import numpy as np
import numpy as np
import csv
from datetime import datetime
from geometry_msgs.msg import Vector3


class Publicador(Node):

    def __init__(self):
        super().__init__('manipulator')
        self.publisher_ = self.create_publisher(String, 'manipulator_ang', 10)
        self.publisher2_ = self.create_publisher(Vector3, 'robot_manipulator_position', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.movement = String()
        self.presionado=False
        self.AngRed=90
        self.AngBlack=90
        # Solicita al usuario el nombre del archivo
        self.file_name = input('Ingrese el nombre del archivo: ')
        # Abre el archivo en modo escritura
        self.file = open(f'{self.file_name}.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
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
        movement_frame.grid_columnconfigure(3, weight=1)
        movement_frame.grid_columnconfigure(4, weight=1)
        
        movement_frame.grid_rowconfigure(0, weight=1)
        movement_frame.grid_rowconfigure(1, weight=1)
        movement_frame.grid_rowconfigure(2, weight=1)

        bg_label = tk.Label(movement_frame, image=bg_image)
        bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Crear botones de movimiento y hacerlos transparentes
        
        self.z_button = tk.Button(movement_frame, text="Z", width=5, height=5, command=lambda:self.grip_on(self,self.z_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.x_button = tk.Button(movement_frame, text="X", width=5, height=5, command=lambda:self.grip_off(self,self.x_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.u_button = tk.Button(movement_frame, text="U", width=5, height=5, command=lambda:self.antarm_forward(self,self.u_button), highlightthickness=0,bg='#191970', fg='white', font=('Arial', 16))
        self.o_button = tk.Button(movement_frame, text="O", width=5, height=5, command=lambda:self.antarm_backward(self,self.o_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.i_button = tk.Button(movement_frame, text="I", width=5, height=5, command=lambda:self.arm_forward(self,self.i_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.k_button = tk.Button(movement_frame, text="K", width=5, height=5, command=lambda:self.arm_backward(self,self.k_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.j_button = tk.Button(movement_frame, text="J", width=5, height=5, command=lambda:self.base_left(self,self.j_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.l_button = tk.Button(movement_frame, text="L", width=5, height=5, command=lambda:self.base_right(self,self.l_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        
        
        self.z_button.grid(row=2, column=0)
        self.x_button.grid(row=2, column=1)
        self.u_button.grid(row=0, column=2)
        self.o_button.grid(row=0, column=4)
        self.i_button.grid(row=0, column=3)
        self.k_button.grid(row=1, column=3) 
        self.j_button.grid(row=1, column=2)
        self.l_button.grid(row=1, column=4)                    


        # Asociar teclas del teclado con los botones de movimiento
        self.root.bind('<KeyPress-z>', lambda event: self.z_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-x>', lambda event: self.x_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-u>', lambda event: self.u_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-o>', lambda event: self.o_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-i>', lambda event: self.i_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-k>', lambda event: self.k_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-j>', lambda event: self.j_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-l>', lambda event: self.l_button.config(relief=tk.SUNKEN))

        self.root.bind('<KeyRelease-z>', lambda event: self.z_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-x>', lambda event: self.x_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-u>', lambda event: self.u_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-o>', lambda event: self.o_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-i>', lambda event: self.i_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-k>', lambda event: self.k_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-j>', lambda event: self.j_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-l>', lambda event: self.l_button.config(relief=tk.RAISED))

        # Iniciar listener de teclado
        self.key_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.key_listener.start()
        self.root.mainloop()




    def calculate_position(self,theta1, theta2, l1=0.19, l2=0.11):
        theta1, theta2 = np.radians([theta1, theta2])  # convertir a radianes

        # Calcula las posiciones x, y
        x = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
        y = l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2)
        
        # Creamos un Vector3 para guardar las posiciones
        position = Vector3()
        position.x = x
        position.y = y
        position.z = 0.0  # Puedes ajustar este valor si tienes alguna altura en la coordenada Z.

        return position

    
    def open_grip(self):
        button=self.z_button
        self.movement.data = "z"
        print(self.movement)
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def close_grip(self):
        button=self.x_button
        self.movement.data = "x"
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def antarm_forward(self): #negro
        self.AngBlack+=10
        position=self.calculate_position(self.AngRed,self.AngBlack)
        self.publisher2_.publish(position)
        button=self.u_button
        self.movement.data = "u"
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def antarm_backward(self):
        self.AngBlack-=10
        position=self.calculate_position(self.AngRed,self.AngBlack)
        self.publisher2_.publish(position)
        button=self.o_button
        self.movement.data = "o"
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')
        
    def arm_forward(self):
        self.AngRed+=10
        position=self.calculate_position(self.AngRed,self.AngBlack)
        self.publisher2_.publish(position)
        button=self.i_button
        self.movement.data = "i"
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def arm_backward(self):
        self.AngRed-=10
        position=self.calculate_position(self.AngRed,self.AngBlack)
        self.publisher2_.publish(position)
        button=self.k_button
        self.movement.data = "k"
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')    
        
    def base_left(self):
        button=self.j_button
        self.movement.data = "j"
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def base_right(self):
        button=self.l_button
        self.movement.data = "l"
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')
    
    def unopen_grip(self):
        button=self.z_button
        self.movement.data = "0.0"
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def unclose_grip(self):
        button=self.x_button
        self.movement.data = "0.0"
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def antarm_unforward(self):
        button=self.u_button
        self.movement.data = "0.0"
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def antarm_unbackward(self):
        button=self.o_button
        self.movement.data = "0.0"
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')
        
    def arm_unforward(self):
        button=self.i_button
        self.movement.data = "0.0"
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def arm_unbackward(self):
        button=self.k_button
        self.movement.data = "0.0"
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')
        
    def base_unleft(self):
        button=self.j_button
        self.movement.data = "0.0"
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def base_unright(self):
        button=self.l_button
        self.movement.data = "0.0"
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')


    def custom_cmd(self, cmd):
        self.get_logger().info('Custom command received: "%s"' % cmd)
        # Aquí puedes implementar lo que quieras que haga el robot cuando reciba un comando personalizado

    def on_press(self, key):
        try:
            # Registra solamente la tecla presionada
           
            # Mapear teclas de flechas a comandos de movimiento
            if key.char == 'z' and (not self.presionado):
                self.presionado=True
                self.open_grip()
            elif key.char == 'x'and (not self.presionado):
                self.presionado=True
                self.close_grip()
            elif key.char == 'u'and (not self.presionado):
                self.presionado=True
                self.antarm_forward()
            elif key.char == 'o' and (not self.presionado):
                self.presionado=True
                self.antarm_backward()
            elif key.char == 'i'and (not self.presionado):
                self.presionado=True
                self.arm_forward()
            elif key.char == 'k'and (not self.presionado):
                self.presionado=True
                self.arm_backward()
            elif key.char == 'j'and (not self.presionado):
                self.presionado=True
                self.base_left()
            elif key.char == 'l'and (not self.presionado):
                self.presionado=True
                self.base_right()
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
            if key.char == 'z'and (self.presionado):
                self.presionado=False
                self.unopen_grip()
            elif key.char == 'x'and (self.presionado):
                self.presionado=False
                self.unclose_grip()
            elif key.char == 'u'and ( self.presionado):
                self.presionado=False
                self.antarm_unforward()
            elif key.char == 'o'and ( self.presionado):
                self.presionado=False
                self.antarm_unbackward()
            elif key.char == 'i'and (self.presionado):
                self.presionado=False
                self.arm_unforward()
            elif key.char == 'k'and (self.presionado):
                self.presionado=False
                self.arm_unbackward()
            elif key.char == 'j'and ( self.presionado):
                self.presionado=False
                self.base_unleft()
            elif key.char == 'l'and ( self.presionado):
                self.presionado=False
                self.base_unright()
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