import sizebased_compress_lib

import tkinter
import sv_ttk
from tkinter.ttk import *

# An object-oriented way instead of a procedural one
class MainFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!').pack()
        self.imgLable = Label(self, text='Waiting for the picture').pack()
        self.getButton = Checkbutton(self, text='Get', command=lambda: None).pack()
        self.quitButton = Button(self, text='Quit', command=lambda: None).pack()

        self.canvas = tkinter.Canvas(self, width=800, height=600, bg="#aaaaaa")
        triangle = self.canvas.create_polygon(100,100, 200,200, 100,300,  fill='#00ffff')
        triangle = self.canvas.create_polygon(400,400, 450,400, 450,450, 400,450,  fill='#00ff00')


        self.canvas.pack()

        my_style = Style()
        my_style.configure('TEntry', font=("微软雅黑"))
        self.cleanButton = Button(self, text='Clear清除三角', command=lambda: self.canvas.delete(triangle)).pack()


if __name__=='__main__':
