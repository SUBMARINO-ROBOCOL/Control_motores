#!/usr/bin/env python3

# Librerias MOVIMIENTO ROBOT

from geometry_msgs.msg import Twist
from rclpy.node import Node

# Librerias MANIPULATOR

from std_msgs.msg import String
from rclpy.node import Node
from geometry_msgs.msg import Vector3
import csv
from datetime import datetime

# Librerias de AMBOS

import tkinter as tk
import os
import numpy as np
import rclpy
from PIL import ImageTk, Image
from pynput import keyboard




class Publicador(Node):

    def __init__(self):

        # MOVIMIENTO
        super().__init__('manipulator')
        self.publisher_ = self.create_publisher(String, 'robot_cmdVel', 10)
        self.publisher2_ = self.create_publisher(String, 'manipulator_ang', 10)
    

        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.presionado=False
        
        self.movement = String()
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
        self.root.geometry("1000x1000")

        #importar imagen de fondo
        ruta_imagen = os.path.abspath("imagen_de_fondo.jpg")
        image = Image.open(ruta_imagen)
        image = image.resize((1000, 1000), Image.ANTIALIAS) # Redimensionar la imagen
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
        movement_frame.grid_columnconfigure(5, weight=1)
        movement_frame.grid_columnconfigure(6, weight=1)
        
        movement_frame.grid_rowconfigure(0, weight=1)
        movement_frame.grid_rowconfigure(1, weight=1)
        movement_frame.grid_rowconfigure(2, weight=1)

        bg_label = tk.Label(movement_frame, image=bg_image)
        bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Crear botones de movimiento y hacerlos transparentes
        
        # MOVIMIENTO ROBOT
        self.w_button = tk.Button(movement_frame, text="W", width=5, height=5, command=lambda:self.forward(self,self.w_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.a_button = tk.Button(movement_frame, text="A", width=5, height=5, command=lambda:self.left(self,self.a_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.s_button = tk.Button(movement_frame, text="S", width=5, height=5, command=lambda:self.backward(self,self.s_button), highlightthickness=0,bg='#191970', fg='white', font=('Arial', 16))
        self.d_button = tk.Button(movement_frame, text="D", width=5, height=5, command=lambda:self.right(self,self.d_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        

        self.w_button.grid(row=1, column=1)
        self.a_button.grid(row=2, column=0)
        self.s_button.grid(row=2, column=1)
        self.d_button.grid(row=2, column=2)


        # MOVIMIENTO BRAZO
        self.z_button = tk.Button(movement_frame, text="Z", width=5, height=5, command=lambda:self.grip_on(self,self.z_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.x_button = tk.Button(movement_frame, text="X", width=5, height=5, command=lambda:self.grip_off(self,self.x_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.u_button = tk.Button(movement_frame, text="U", width=5, height=5, command=lambda:self.antarm_forward(self,self.u_button), highlightthickness=0,bg='#191970', fg='white', font=('Arial', 16))
        self.o_button = tk.Button(movement_frame, text="O", width=5, height=5, command=lambda:self.antarm_backward(self,self.o_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.i_button = tk.Button(movement_frame, text="I", width=5, height=5, command=lambda:self.arm_forward(self,self.i_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.k_button = tk.Button(movement_frame, text="K", width=5, height=5, command=lambda:self.arm_backward(self,self.k_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.j_button = tk.Button(movement_frame, text="J", width=5, height=5, command=lambda:self.base_left(self,self.j_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.l_button = tk.Button(movement_frame, text="L", width=5, height=5, command=lambda:self.base_right(self,self.l_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        
        
        self.z_button.grid(row=2, column=5)
        self.x_button.grid(row=2, column=6)
        self.u_button.grid(row=0, column=4)
        self.o_button.grid(row=0, column=6)
        self.i_button.grid(row=0, column=5)
        self.k_button.grid(row=1, column=5) 
        self.j_button.grid(row=1, column=4)
        self.l_button.grid(row=1, column=6)                    

        
        # Asociar teclas del teclado con los botones de movimiento
        self.root.bind('<KeyPress-w>', lambda event: self.w_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-a>', lambda event: self.a_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-s>', lambda event: self.s_button.config(relief=tk.SUNKEN))
        self.root.bind('<KeyPress-d>', lambda event: self.d_button.config(relief=tk.SUNKEN))

        self.root.bind('<KeyRelease-w>', lambda event: self.w_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-a>', lambda event: self.a_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-s>', lambda event: self.s_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-d>', lambda event: self.d_button.config(relief=tk.RAISED))



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





    
    def open_grip(self):
        button=self.z_button
        self.movement.data = "z"
        print(self.movement)
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')

    def close_grip(self):
        button=self.x_button
        self.movement.data = "x"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')

    def antarm_forward(self): #negro
        self.AngBlack+=10
       
        button=self.u_button
        self.movement.data = "u"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')

    def antarm_backward(self):
        self.AngBlack-=10
        
        button=self.o_button
        self.movement.data = "o"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')
        
    def arm_forward(self):
        self.AngRed+=10
        button=self.i_button
        self.movement.data = "i"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')
      
        # Asegura que se escriban los datos en el archivo
       

    def arm_backward(self):
        self.AngRed-=10

        button=self.k_button
        self.movement.data = "k"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')    
       
        # Asegura que se escriban los datos en el archivo
        
        
    def base_left(self):
        button=self.j_button
        self.movement.data = "j"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')
       
        # Asegura que se escriban los datos en el archivo
       

    def base_right(self):
        button=self.l_button
        self.movement.data = "l"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')
        
        # Asegura que se escriban los datos en el archivo
        
    
    def unopen_grip(self):
        button=self.z_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')
      
        # Asegura que se escriban los datos en el archivo
       

    def unclose_grip(self):
        button=self.x_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')
        
        # Asegura que se escriban los datos en el archivo
       

    def antarm_unforward(self):
        button=self.u_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')
       
        # Asegura que se escriban los datos en el archivo
        

    def antarm_unbackward(self):
        button=self.o_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')
        
        # Asegura que se escriban los datos en el archivo
        
        
    def arm_unforward(self):
        button=self.i_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')
        
        # Asegura que se escriban los datos en el archivo
        

    def arm_unbackward(self):
        button=self.k_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')
        
    def base_unleft(self):
        button=self.j_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')

        # Asegura que se escriban los datos en el archivo
    

    def base_unright(self):
        button=self.l_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')
        
      
    # movimiento robot 
    #FUNCIONES MOVIMIENTO
    def forward(self):
        button=self.w_button
        self.movement.data = "w"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')
        self.writer.writerow(self.movement.data)

    def backward(self):
        button=self.s_button
        self.movement.data = "s"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')
        self.writer.writerow(self.movement.data)

    def left(self):
        button=self.a_button
        self.movement.data = "a"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')
        self.writer.writerow(self.movement.data)

    def right(self):
        button=self.d_button
        self.movement.data = "d"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#FFA500')
        self.writer.writerow(self.movement.data)

    def unforward(self):
        button=self.w_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')

    def unbackward(self):
        button=self.s_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')

    def unleft(self):
        button=self.a_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')

    def unright(self):
        button=self.d_button
        self.movement.data = "0.0"
        self.publisher2_.publish(self.movement)
        button.configure(bg='#191970')


    def custom_cmd(self, cmd):
        self.get_logger().info('Custom command received: "%s"' % cmd)
        # Aquí puedes implementar lo que quieras que haga el robot cuando reciba un comando personalizado

    def on_press(self, key):

        try:
            if key.char != 'w' and key.char != 's' and key.char != 'a' and key.char != 'd' :
                self.writer.writerow([ key.char])
                # Asegura que se escriban los datos en el archivo
                self.file.flush()
            if key.char == 'w' and (not self.presionado):
                self.presionado=True
                self.forward()
            if key.char == 's'and (not self.presionado):
                self.presionado=True
                self.backward()
            if key.char == 'a'and (not self.presionado):
                self.presionado=True
                self.left()
            if key.char == 'd'and (not self.presionado):
                self.presionado=True
                self.right()
            if key.char == 'z' and (not self.presionado):
                self.presionado=True
                self.open_grip()
            if key.char == 'x'and (not self.presionado):
                self.presionado=True
                self.close_grip()
            if key.char == 'u'and (not self.presionado):
                self.presionado=True
                self.antarm_forward()
            if key.char == 'o' and (not self.presionado):
                self.presionado=True
                self.antarm_backward()
            if key.char == 'i'and (not self.presionado):
                self.presionado=True
                self.arm_forward()
            if key.char == 'k'and (not self.presionado):
                self.presionado=True
                self.arm_backward()
            if key.char == 'j'and (not self.presionado):
                self.presionado=True
                self.base_left()
            if key.char == 'l'and (not self.presionado):
                self.presionado=True
                self.base_right()
            else:
                # Si se presiona cualquier otra tecla, tomar el comando personalizado de la entrada de texto
                cmd = self.custom_cmd.get()
                self.custom_cmd(cmd)
        except AttributeError:
            # Ignorar teclas de modificación (Shift, Ctrl, Alt, etc.)
            pass

    def on_release(self, key):
        # Detener el movimiento al soltar cualquier tecla de movimiento
        # Registra solamente la tecla presionada
        self.writer.writerow('0')
        # Asegura que se escriban los datos en el archivo
        self.file.flush()
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
