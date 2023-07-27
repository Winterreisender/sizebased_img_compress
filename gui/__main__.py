import sizebased_compress_lib

import tkinter
import sv_ttk
from tkinter.ttk import *

# An object-oriented way instead of a procedural one
class MainFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        # Some dummy widgets
        self.helloLabel = Label(self, text='Hello, world!').pack()
        self.imgLable = Label(self, text='Waiting for the picture').pack()
        self.getButton = Checkbutton(self, text='Get', command=lambda: None).pack()
        self.quitButton = Button(self, text='Quit', command=lambda: None).pack()



if __name__=='__main__':
    root = tkinter.Tk()

    mainframe = MainFrame(root)
    # 设置窗口标题:
    mainframe.master.title('GetCNBingPic')

    # This is where the magic happens
    sv_ttk.set_theme("light")

    # 主消息循环:
    root.mainloop()