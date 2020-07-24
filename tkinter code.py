import numpy as np
import keras
import tensorflow as tf
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras import backend as K
from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image


model = load_model('mnist_model.h5')

def predict_digit(img):
    #resizing image
    img = img.resize((28,28))
    
    img = img.convert('L') #convert to grayscale
    img = np.array(img)
    img = img.reshape(1,28,28,1)
    img = img/255.0 #normalizing
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        
        
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "black", cursor="cross")
        self.canvas.old_coords = None
        self.label = tk.Label(self, text="Draw a number from 0 to 9", font=("Helvetica", 16), )
        self.classify_btn = tk.Button(self, text = "Classify", command = self.predict_handwriting)   
        self.button_clear = tk.Button(self, text = "Clear", command = self.delete_all)
       
        # layout of grid
        self.canvas.grid(row=0, column=0, pady=2, sticky=W)
        self.label.grid(row=2, column=0,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=0, pady=0, padx=0, ipady = 0, sticky="E")
        self.button_clear.grid(row=1, column=0, pady=0, ipadx = 0, sticky="W")
        
        self.canvas.bind("<B1-Motion>", self.draw)
        
        
    def draw(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.old_coords = self.x, self.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='white', outline='white')
        
        
    def predict_handwriting(self):
        handle_canvas = self.canvas.winfo_id()  
        rect = win32gui.GetWindowRect(handle_canvas)  
        a,b,c,d = rect
        rect=(a+4,b+4,c-4,d-4)
        img = ImageGrab.grab(rect)

        digit, acc = predict_digit(img)
        self.label.configure(text= 'Predicted number: '+ str(digit)+'\n'+ 'Confidence percent: ' + str(int(acc*100))+'%')
       
    def delete_all(self):
        self.canvas.delete("all")
        
app = Window()
mainloop()



