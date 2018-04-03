from tkinter import Tk, StringVar, Frame, BOTH, Message, Label, END
from tkinter import ttk
import tkinter as tk
import os
import sys
from PIL import ImageTk, Image
Image.MAX_IMAGE_PIXELS = 1000000000
import requests
from io import BytesIO
import math

# phi, theta
orbitals = [[0, 0], [60, 45], [34, 60], [24,80]]

class Example(Frame):
    def __init__(self, parent):
        frame = Frame.__init__(self, parent, background="white")   
        self.parent = parent

        self.orbital = 0
        self.curr_long = 0
        self.curr_lat = 0
        self.vspeed = 0
        self.hspeed = 0

        self._job = None

        self.image = Image.open('map.jpg')
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
        img = ImageTk.PhotoImage(self.image.crop(
            (
                self.curr_long - 100,
                self.curr_lat - 100,
                self.curr_long + 100,
                self.curr_lat + 100)
            ))

        self.panel.configure(image = img)
        self.panel.image = img

        self.curr_long += self.vspeed
        self.curr_lat += self.hspeed

        if self.curr_long < 100:
            self.curr_long = self.height - 100

        if self.curr_long > self.height - 100:
            self.curr_long = 100

        if self.curr_lat < 100:
            self.curr_lat = self.width - 100

        if self.curr_lat > self.width - 100:
            self.curr_lat = 100


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

        self.curr_lat = self.height/2.0
        self.curr_long = self.width * (0.5 + math.sin(orbitals[self.orbital][0])/2)
        self.vspeed = 2 * math.sin(orbitals[self.orbital][1])
        self.hspeed = 2 * math.cos(orbitals[self.orbital][1])

        self.pan()



def main():
	root = Tk()
	root.geometry("1000x900+300+300")
	app = Example(root)
	root.mainloop()  

if __name__ == '__main__':
	main()