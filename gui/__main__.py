import io
import os
from sizebased_compress_lib import smart_compress

import tkinter
from tkinter.filedialog import askopenfilename
import sv_ttk
from tkinter.ttk import *
import cv2
from pathlib import Path
import functools
from PIL import ImageTk, Image
from enum import Enum, auto
# Decorator for actions
# Call self.update_ui() automaticlly
def ui_action(f):
    print(f)
    @functools.wraps(f)
    def wrapped(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        self.update_ui()
        return ret
    return wrapped

# Maybe?
class UiContext:
    def __init__(self, main) -> None:
        self.main = main

    def __enter__(self) -> None:
        pass

    def __exit__(self) -> None:
        self.main.update_ui()

# Maybe?
class USize:
    @classmethod
    def __str2int(cls, s) -> int:
        pass
    
    @classmethod
    def __int2str(cls, i) -> str:
        pass

    def __init__(self, size) -> None:
        if isinstance(size, int):
            self.size = size
        elif isinstance(size, str):
            self.size = USize.__str2int(size)
        else:
            raise TypeError('USize.__init__ need int | str')
    
    def __int__(self) -> int:
        return self.size
    
    def __str__(self) -> str:
        return USize.__int2str(self.size)


# An object-oriented way instead of a procedural one
class MainFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.states()
        self.ui()
        self.update_ui()

    def states(self):
        self.isDarkMode = tkinter.BooleanVar(self) # 2-direction works fine
        self.src_path :Path  = None
        self.src_img_pil :Image = None
        self.src_size = 0
        self.target_size :int = 0
        self.dst_size :int = 0
        self.dst_img = None
        self.quality :int = 100

    def ui(self):
        self.darkModeButton = Checkbutton(self, text='Dark Mode', command=lambda: sv_ttk.set_theme("dark" if self.isDarkMode.get() else 'light'), variable=self.isDarkMode)
        self.darkModeButton.pack()

        self.srcButton = Button(self, text='Select File', command=self.set_src)
        self.srcSizeLabel = Label(self)
        self.srcButton.pack()
        self.srcSizeLabel.pack()

        # Target Size
        def onTargetSizeSpinChanged():
            self.target_size = int(self.targetSizeSpin.get())
            self.update_ui()
        self.targetSizeSpin = Spinbox(self, increment=1, command=onTargetSizeSpinChanged, from_=0, to=0)
        self.targetSizeSpin.set(0)
        self.targetSizeSpin.bind('<KeyRelease>',lambda e: onTargetSizeSpinChanged())
        self.targetSizeLabel = Label(self)
        self.targetSizeSpin.pack()
        self.targetSizeLabel.pack()

        self.compressButton = Button(self, text='[TODO]Compress', command=self.compress_img).pack()
        self.qualityLabel = Label(self)
        self.qualityLabel.pack()

        self.dstSizeLabel = Label(self)
        self.dstSizeLabel.pack()
        self.dstImgLabel = Label(self)
        self.dstImgLabel.pack()


    def update_ui(self):
        self.srcSizeLabel['text'] = f"Original Size: {self.src_size}"
        self.dstSizeLabel['text'] = f"Dst Size: {self.dst_size}"
        self.targetSizeSpin['to'] = self.src_size
        self.targetSizeSpin['from'] = self.src_size // 5
        self.targetSizeLabel['text'] = f"Target Size: {self.target_size}"
        self.qualityLabel['text'] = f"{self.quality}"


    @ui_action
    def set_src(self):
        self.src_path = Path(askopenfilename(filetypes= [('Image','*.jpg, *.png')] ))
        self.src_size = os.path.getsize(self.src_path)

        #self.src_img_pil = Image.open(self.src_path)
        #self.srcImage = ImageTk.PhotoImage(self.src_img_pil, size=None) #, size=None # use self.srcImage to Avoid GC # ToDo: Auto size
        #self.srcImgLabel = Label(self, image=self.srcImage).pack()

    @ui_action
    def compress_img(self):
        src_img_cv2 = cv2.imread(str(self.src_path), cv2.IMREAD_UNCHANGED)
        quality, self.dst_img_bytes = smart_compress.smart_compress( src_img_cv2 , self.target_size) # ToDo: Avoid twice read, try convert from src_img_pil or use bytes
        self.dst_size=len(self.dst_img_bytes)
        self.quality = quality

        self.dstImage = ImageTk.PhotoImage(Image.open(io.BytesIO(self.dst_img_bytes))) # use self. to Avoid GC
        self.dstImgLabel['image'] = self.dstImage #, size=None  # ToDo: Auto size

        
        



if __name__=='__main__':
    root = tkinter.Tk()

    mainframe = MainFrame(root)
    # 设置窗口标题:
    mainframe.master.title('Size Based Img Compressor')

    # This is where the magic happens
    sv_ttk.set_theme("light")

    # 主消息循环:
    root.mainloop()