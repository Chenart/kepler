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
num_orbitals = 100

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
        init_x = self.width * self.orbital/(2.0 * num_orbitals)
        curr_x = init_x + 2 * self.curr_time
        curr_y = 0.5 * self.height + 0.5 * self.height * math.sin(2 * math.pi * (curr_x - init_x)/self.width)
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