import RPi.GPIO as GPIO
import tkinter as tk

# Inicialización  de los puertos GPIO a usar
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)


def io_inversor(instruccion):
    """
    Función que enciende o apaga el switch del inversor

    Args:
        instruccion (int): recibe un 1 para encender o un 0 para apagar
    """
    if instruccion == 0:
        GPIO.output(6,GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(6,GPIO.HIGH)
    else:
        print("Instrucción no encontrada")


def io_bateria(instruccion):
    """
    Función que enciende o apaga el switch de la bateria

    Args:
        instruccion (int): recibe un 1 para encerder o un 0 para apagar
    """
    if instruccion == 0:
        GPIO.output(5,GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(5,GPIO.HIGH)
    else:
        print("Instrucción no encontrada")



def color_inversor():
    global color_in
    print(color_in,color_ba)
    if color_in==1:
        btn1.configure(bg="red")
        io_inversor(0)
        color_in = 0   
    else:
        btn1.configure(bg="green")
        io_inversor(1)
        color_in = 1
        

def color_bateria():
    global color_ba
    print(color_in,color_ba)
    if color_ba==1:
        btn2.configure(bg="red")
        io_bateria(0)
        color_ba = 0
    else:
        btn2.configure(bg="green")
        io_bateria(1)
        color_ba = 1
    
    



w = tk.Tk()
w.title("Switches")
#Frame
fm = tk.Frame(w)
fm.grid(row = 0, column = 0)
color_in = 0
color_ba = 0
#Boton 1
btn1 = tk.Button(fm, text = "Inversor", command=color_inversor, height= 2, width= 20,bg="red",fg="white")
btn1.grid(row= 1, column= 0)
#Boton2
btn2 = tk.Button(fm, text = "Bateria", command=color_bateria, height= 2, width= 20,bg="red",fg="white")
btn2.grid(row= 2, column= 0)
print(color_in,color_ba)
w.mainloop()
GPIO.cleanup()
print("Fin de programa")