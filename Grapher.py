"""""""""""""""""""""""""""""""""
       AUTHOR: PIERO PASTOR
"""""""""""""""""""""""""""""""""

#Importando todas las librerías necesarias
from glob import glob
from re import A
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import BOTTOM, Toplevel, messagebox
import os
from math import *

#Iniciamos a programar la graficadora
#Programamos la interfaz inicial
window = tk.Tk()
window.title("GRAFICADORA DE REGRESIÓN LINEAL")
window.geometry("900x800")
style.use("fivethirtyeight")
figure = Figure()
ploteo=figure.add_subplot(111)

#Graficadora mediante matplotlib
canvas = FigureCanvasTkAgg(figure, window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas, window)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#Programamos las entradas y variables auxiliares
x = []
y = []
sumaXY = 0
sumaX = 0
sumaY = 0
sumaX2 = 0
mayorX = -999999999999999999999999999999999999999999999999
menorX = 9999999999999999999999999999999999999999999999999
mayorY = -999999999999999999999999999999999999999999999999
menorY = 9999999999999999999999999999999999999999999999999
n = 0

#A pesar de no tener una función iterativa, al presionar el botón, esta itera
def plotLine():
    ploteo.clear()
    ploteo.axhline(0, color="gray")
    ploteo.axvline(0, color="gray")
    
    global x_var
    global y_var
    global sumaXY
    global sumaX
    global sumaY
    global sumaX2
    global mayorX
    global menorX
    global menorY
    global mayorY
    global x
    global y

    #Recogemos el valor del entry y lo volvemos float
    if x_var.get() != "" and y_var.get() != "":
        insert_x = float(x_var.get())
        insert_y = float(y_var.get())
    if x_var.get() == "" and y_var.get() != "":
        insert_x = 0
        insert_y = float(y_var.get())
        messagebox.showwarning("Syntax Error!","Falta de valores, estableciendo los puntos vacíos en 0.")
    if y_var.get() == "" and x_var.get() != "":
        insert_y = 0
        insert_x = float(x_var.get())
        messagebox.showwarning("Syntax Error!","Falta de valores, estableciendo los puntos vacíos en 0.")
    if x_var.get() == "" and y_var.get() == "":
        insert_x = 0
        insert_y = 0
        messagebox.showwarning("Syntax Error!","Falta de valores, estableciendo los puntos vacíos en 0.")

    #Se insertan los valores de x & y en cada lista para poder plotearla, además actualiza el rango de visualizacion
    x.insert(len(x), insert_x)
    y.insert(len(y), insert_y)
    n = len(x)
    #actualizamos límites
    if insert_x <= menorX:
        menorX = insert_x
    if insert_x >= mayorX:
        mayorX = insert_x
    if insert_y <= menorY:
        menorY = insert_y
    if insert_y >= mayorY:
        mayorY = insert_y

    #Se realizan las sumatorias necesarias al actualizarse
    sumaX = sumaX + insert_x
    sumaY = sumaY + insert_y
    sumaXY = sumaXY + (insert_x * insert_y)
    sumaX2 = sumaX2 + (insert_x ** 2)

    #Para cuando el dividendo es diferente de 0, se opera y plotea la regresión con a=pendiente y b=constante
    if (n * sumaX2 - (sumaX ** 2)) != 0:
        a = (n * sumaXY - sumaX * sumaY) / (n * sumaX2 - (sumaX ** 2))
        b = (sumaY - a * sumaX) / n

        #Se define la función lineal
        def f(x):
          return a * x + b
        
        #Se definen los límites a mostrar para una visualización más óptima
        menorX = int(menorX)
        mayorX = int(mayorX)
        ploteo.set_xlim([menorX - 2, mayorX + 2])
        ploteo.set_ylim([menorY - 2, mayorY + 2])

        #Plotea la función y anima en un frame para que sea automático
        x_plot = range(menorX - 9999, mayorX + 9999)
        ploteo.plot(x_plot, [f(i) for i in x_plot], color='lime')
        ploteo.plot(x, y, "o", color='purple', alpha=0.7)
        FuncAnimation(figure, f, frames=1, blit=True)
        plt.show()
        print("y = ", a, " * x + ", b)
        print("Las relaciones de x & y son: ")
        print("x: ", x)
        print("y: ", y)
        
    #Se grafican los puntos en caso el dividendo sea igual a 0
    if (n * sumaX2 - (sumaX ** 2)) == 0:
        ploteo.plot(x, y, "o", color='purple', alpha=0.7)
        FuncAnimation(figure, [x, y], frames=1, blit=True)
        plt.show()
        print("Las relaciones de x & y son: ")
        print("x: ", x)
        print("y: ", y)

#Función para predecir
def predict():
    global predict_var
    global sumaX2
    global sumaX
    global sumaY
    global sumaXY
    global x
    global y

    numero = len(x)

    if predict_var.get() == "":
        x_predict = 0
    else:
        x_predict = float(predict_var.get())
        if (numero * sumaX2 - (sumaX ** 2)) != 0:
            pendiente = (numero * sumaXY - sumaX * sumaY) / (numero * sumaX2 - (sumaX ** 2))
            constante = (sumaY - pendiente * sumaX) / numero
            prediction = pendiente * x_predict + constante
            messagebox.showinfo("PREDICTION", f"The prediction is y = {prediction}.")

            #Graficamos el punto
            ploteo.plot(x_predict, prediction, "o", color='black', alpha=0.7)
            FuncAnimation(figure, [x_predict, prediction], frames=1, blit=True)
        else:
            None

#Espacios para colocar los puntos
bo1 = tk.Button(window, text="Plot", command=plotLine)
x_var = tk.Entry(window, width=60)
y_var = tk.Entry(window, width=60)
bo1.pack(side=tk.BOTTOM)
y_var.pack(side=tk.RIGHT)
x_var.pack(side=tk.LEFT)
#Se colocan valores para predecir
predict_var = tk.Entry(window, width=30)
predict_var.pack(side=tk.TOP)
bo2 = tk.Button(window, text="Predict", command=predict)
bo2.pack(side=tk.BOTTOM)


#Loopea la interfaz
window.mainloop()