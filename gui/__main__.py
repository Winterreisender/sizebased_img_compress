from sizebased_compress_lib import smart_compress

import tkinter
from tkinter.filedialog import askopenfilename
import sv_ttk
from tkinter.ttk import *
import cv2
from pathlib import Path

from PIL import ImageTk, Image

# An object-oriented way instead of a procedural one
class MainFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        # States
        self.isDarkMode = tkinter.BooleanVar()
        self.src_path :Path  = None
        self.src_img_pil :Image = None
        self.target_size = tkinter.IntVar()
        self.dst_img = None
        self.quality = tkinter.IntVar()

        # Some dummy widgets
        # Dark Mode Button
        self.darkModeButton = Checkbutton(self, text='Dark Mode', command=lambda: sv_ttk.set_theme("dark" if self.isDarkMode.get() else 'light'), variable=self.isDarkMode).pack()
        self.srcButton = Button(self, text='Select File', command=self.set_src).pack()

        self.compressButton = Button(self, text='[TODO]Compress', command=self.compress_img).pack()

    def set_src(self):
        self.src_path = Path(askopenfilename(filetypes= [('Image','*.jpg, *.png')] ))
        print(self.src_path)
        self.src_img_pil = Image.open(self.src_path)
        self.srcImage = ImageTk.PhotoImage(self.src_img_pil, size=None) #, size=None # use self.srcImage to Avoid GC # ToDo: Auto size
        self.srcImgLabel = Label(self, image=self.srcImage, width=512).pack()


    def compress_img(self):
        
        quality, self.dst_img = smart_compress.smart_compress( cv2.imread(self.src_path, cv2.IMREAD_UNCHANGED) , self.target_size) # ToDo: Avoid twice read, try convert from src_img_pil or use bytes
        self.quality.set(quality)
        
        



if __name__=='__main__':
    root = tkinter.Tk()

    mainframe = MainFrame(root)
    # 设置窗口标题:
    mainframe.master.title('Size Based Img Compressor')

    # This is where the magic happens
    sv_ttk.set_theme("light")

    # 主消息循环:
    root.mainloop()