import io
import os
from sizebased_compress_lib import smart_compress

import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfile
import sv_ttk
from tkinter.ttk import *
import cv2
from pathlib import Path
import functools
from PIL import ImageTk, Image
from enum import Enum
# Decorator for actions
# Call self.update_ui() automaticlly
def ui_action(f):
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


class USize:
    class Unit(Enum):
        B  = 1
        KB = 1024
        MB = 1024*1024

    def __init__(self, size, unit :Unit = Unit.B) -> None: # Size: int | float, unit: Unit | str
        if isinstance(unit, str):
            unit = USize.Unit.__members__[unit]
        elif isinstance(unit, USize.Unit):
            pass
        else:
            raise TypeError('USize.__init__ need Unit | str for unit')

        if isinstance(size, float) or isinstance(size, int):
            self.unit = unit
            self.size = int(size * unit._value_)
        else:
            raise TypeError('USize.__init__ need float | int for size')
            
    
    def __int__(self) -> int:
        return self.size
    
    def __str__(self) -> str:
        size = self.size

        unit = None
        if size >= 1024*1024:
            unit = USize.Unit.MB
        elif size >= 1024:
            unit = USize.Unit.KB
        else:
            unit = USize.Unit.B
        
        return f"{round(size/unit._value_,2)} {unit._name_}"

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
        self.target_size_num :float = 0
        self.target_size_unit       = tkinter.StringVar(self, USize.Unit.B._name_) # 不得已啊，OptionMenu必须用tkinter的变量形式
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
            self.target_size_num = float(self.targetSizeSpin.get())
            self.update_ui()
        self.targetSizeSpin = Spinbox(self, increment=1, command=onTargetSizeSpinChanged, from_=0, to=0)
        self.targetSizeSpin.set(0)
        self.targetSizeSpin.bind('<KeyRelease>',lambda e: onTargetSizeSpinChanged())

        self.targetSizeUnitMenu = OptionMenu(self, self.target_size_unit, *USize.Unit.__members__.keys(), command=lambda _: self.update_ui())

        self.targetSizeLabel = Label(self)
        self.targetSizeSpin.pack()
        self.targetSizeUnitMenu.pack(side='top')
        self.targetSizeLabel.pack()

        self.compressButton = Button(self, text='Compress', command=self.compress_img).pack()
        self.qualityLabel = Label(self)
        self.qualityLabel.pack()

        self.dstSizeLabel = Label(self)
        self.dstSizeLabel.pack()
        self.dstImgLabel = Label(self)
        self.dstImgLabel.pack()

        self.saveButton = Button(self, text='Save', command=self.save_dst).pack()



    def update_ui(self):
        self.srcSizeLabel['text'] = f"Original Size: {USize(self.src_size)}"
        self.dstSizeLabel['text'] = f"Dst Size: {USize(self.dst_size)}"
        self.targetSizeSpin['to'] = self.src_size
        self.targetSizeSpin['from'] = self.src_size // 20
        self.targetSizeLabel['text'] = f"Target Size (B): {USize(self.target_size_num, self.target_size_unit.get())}"
        self.qualityLabel['text'] = f"quality = {self.quality}"


    @ui_action
    def set_src(self):
        self.src_path = Path(askopenfilename(filetypes= [('Image','*.jpg *.png')] ))
        self.src_size = os.path.getsize(self.src_path)
        #self.src_img_pil = Image.open(self.src_path)
        #self.srcImage = ImageTk.PhotoImage(self.src_img_pil, size=None) #, size=None # use self.srcImage to Avoid GC # ToDo: Auto size
        #self.srcImgLabel = Label(self, image=self.srcImage).pack()

    @ui_action
    def compress_img(self):
        src_img_cv2 = cv2.imread(str(self.src_path), cv2.IMREAD_UNCHANGED)
        quality, self.dst_img_bytes = smart_compress.smart_compress( src_img_cv2 , int(USize(self.target_size_num, self.target_size_unit.get()))) # ToDo: Avoid twice read, try convert from src_img_pil or use bytes
        self.dst_size=len(self.dst_img_bytes)
        self.quality = quality

        self.dstImage = ImageTk.PhotoImage(Image.open(io.BytesIO(self.dst_img_bytes))) # use self. to Avoid GC
        self.dstImgLabel['image'] = self.dstImage #, size=None  # ToDo: Auto size

    @ui_action
    def save_dst(self):
        with asksaveasfile(mode='wb', confirmoverwrite=True, defaultextension='jpg',initialfile='compressed.jpg', filetypes= [('Image','*.jpg')]) as save_file:
            save_file.write(self.dst_img_bytes)
        



if __name__=='__main__':
    root = tkinter.Tk()

    mainframe = MainFrame(root)
    # 设置窗口标题:
    mainframe.master.title('Size Based Img Compressor')

    # This is where the magic happens
    sv_ttk.set_theme("light")

    # 主消息循环:
    root.mainloop()