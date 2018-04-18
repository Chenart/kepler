from tkinter import Tk, StringVar, Frame, BOTH, Message, Label, END
from tkinter import ttk
import tkinter as tk
import os
import sys
from PIL import ImageTk, Image
Image.MAX_IMAGE_PIXELS = 1000000000
import requests
from io import BytesIO
from math import sin, cos, pi, radians

# theta, phi
orbitals = [[0, 0], [3, 7], [3, 85], [3, 121], [3, 139], [3, 155], [3, 160], [3, 265], [5, 155], [6, 213], [10, 8], [13, 59], [13, 97], [15, 159], [16, 10], [16, 85], [16, 97], [16, 149], [17, 176], [20, 142], [20, 238], [21, 139], [21, 265], [22, 263], [22, 324], [23, 71], [23, 85], [23, 294], [23, 296], [24, 7], [27, 296], [27, 338], [28, 21], [29, 59], [29, 253], [29, 302], [30, 79], [30, 139], [30, 184], [31, 178], [31, 261], [32, 265], [32, 296], [32, 297], [32, 356], [36, 149], [38, 42], [42, 7], [42, 219], [42, 237], [42, 336], [45, 30], [45, 65], [45, 219], [45, 248], [45, 288], [46, 61], [46, 155], [46, 271], [47, 296], [49, 85], [51, 139], [53, 7], [53, 295], [56, 83], [56, 139], [56, 199], [58, 85], [58, 160], [64, 160], [64, 294], [65, 79], [65, 126], [69, 10], [69, 270], [71, 15], [71, 79], [71, 85], [71, 107], [71, 230], [71, 296], [71, 315], [73, 8], [73, 160], [73, 187], [73, 265], [73, 276], [74, 178], [76, 270], [76, 297], [79, 7], [79, 79], [79, 132], [79, 261], [79, 268], [79, 297], [80, 121], [81, 21], [81, 169], [82, 10], [82, 21], [82, 164], [82, 221], [82, 294], [85, 21], [87, 126], [87, 287], [87, 296], [88, 287], [90, 85]]

class Example(Frame):
    def __init__(self, parent):
        frame = Frame.__init__(self, parent, background="white")   
        self.parent = parent

        self.orbital = 0
        self.curr_time = 0

        self._job = None

        self.image = Image.open('bigmap.jpg')
        self.width, self.height = self.image.size
        self.image.crop((0,0,1,1))

        self.initUI()

    def initUI(self):
    	self.selector = ttk.Entry(self)
        self.selector.insert(END, "0")
    	self.selector.pack()

        self.launch = ttk.Button(self, text="Launch", command=lambda:self.launch_sim(), state = "enabled")
        self.launch.pack()

        self.arret = ttk.Button(self, text="Stop", command=lambda:self.stop(), state = "enabled")
        self.arret.pack()

        self.panel = ttk.Label(self)
        self.panel.pack()

        self.parent.title("KEPLER Satellite View")
        self.pack(fill=BOTH, expand=1)

    def pan(self):
        theta = radians(orbitals[self.orbital][0])
        phi = radians(orbitals[self.orbital][1] % 180)
        init_x = self.width * sin(phi)/2.0
        curr_x = init_x + 5 * self.curr_time
        curr_y = 0.5 * self.height + 0.5 * self.height * sin(theta) * sin(2 * pi * (curr_x - init_x)/self.width)
        if curr_x < 200:
            curr_x = 200
        elif curr_x > self.width - 200:
            curr_x = 200

        if curr_y < 200:
            curr_y = 200
        elif curr_y > self.height - 200:
            curr_y = self.height - 200
        img = ImageTk.PhotoImage(self.image.crop(
            (
                curr_x - 200,
                curr_y - 200,
                curr_x + 200,
                curr_y + 200)
            ))

        self.panel.configure(image = img)
        self.panel.image = img
        self.curr_time += 1

        self._job = self.panel.after(10, self.pan)

    def stop(self):
        if self._job is not None:
            self.panel.after_cancel(self._job)
            self._job = None

    def launch_sim(self):
        if self._job is not None:
            self.panel.after_cancel(self._job)
            self._job = None
        self.orbital =  int(self.selector.get())
        self.curr_time = 0

        self.pan()



def main():
	root = Tk()
	root.geometry("700x700+300+300")
	app = Example(root)
	root.mainloop()  

if __name__ == '__main__':
	main()