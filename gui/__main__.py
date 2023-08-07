import io
import os
from sizebased_img_compress import smart_compress

import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showinfo, showwarning, showerror
import sv_ttk
from tkinter.ttk import *
import cv2
from pathlib import Path
import functools
from PIL import ImageTk, Image
from enum import Enum
import numpy as np 
# Decorator for actions
# Call self.update_ui() automaticlly
def ui_action(f):
    @functools.wraps(f)
    def wrapped(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        self.update_ui()
        return ret
    return wrapped

def smart_fit(size,limit):
    '''limit and size should be Tuple[int, int]'''
    w,h = size
    wlim, hlim = limit

    wh_ratio = w / h
    wh_lim_ratio = wlim / hlim

    if wh_ratio >= wh_lim_ratio: # 如果原图更宽
        return wlim, int(wlim/wh_ratio)
    else:
        return int(hlim*wh_ratio), hlim


class USize:
    class Unit(Enum):
        KB = 1024 # Default
        B  = 1
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
UI_IMAGE_SIZE=(400,300)
class MainFrame(Frame):
    def __init__(self, root=None):
        self.root = root
        Frame.__init__(self, root, width=1024, height=600)
        self.pack()

        self.states()
        self.ui()
        self.update_ui()

    def states(self):
        # States should be as less as possible, do not mind performance, human's time is most valuable
        self.isDarkMode = tkinter.BooleanVar(self) # 2-direction works fine
        self.src_path :Path  = None
        self.src_file_size = 0
        self.target_size_num :float = 0
        self.target_size_unit       = tkinter.StringVar(self, USize.Unit.B._name_) # 不得已啊，OptionMenu必须用tkinter的变量形式
        self.dst_img_bytes = None
        self.quality :int = -1

    def ui(self):
        # Widgets
        self.srcButton = Button(self, text='Select File', command=self.set_src)
        self.srcSizeLabel = Label(self)
        def onTargetSizeSpinChanged():
            self.target_size_num = float(self.targetSizeSpin.get())
            self.update_ui()
        self.targetSizeSpin = Spinbox(self, increment=1, command=onTargetSizeSpinChanged, width=10)
        self.targetSizeSpin.set(0)
        self.targetSizeSpin.bind('<KeyRelease>',lambda e: onTargetSizeSpinChanged())
        self.targetSizeUnitMenu = OptionMenu(self, self.target_size_unit, 'KB', *USize.Unit.__members__.keys(), command=lambda _: self.update_ui())
        self.targetSizeLabel = Label(self)

        self.compressButton = Button(self, text='Compress', command=self.compress_img)
        self.qualityLabel = Label(self)
        self.dstSizeLabel = Label(self)
        self.dstImgLabel = Label(self, width=40)
        self.srcImgLabel = Label(self, width=40)
        self.saveButton = Button(self, text='Save', command=self.save_dst)

        # Geometry
        # col 0..3 is for src and 5..8 is for dst
        self.rowconfigure(0, minsize=300, pad=5)
        self.rowconfigure(1, pad=5)
        self.rowconfigure(2, pad=5)
        self.rowconfigure(3, pad=5)

        self.srcImgLabel.grid(       row=0, column=0, columnspan=4)
        self.srcSizeLabel.grid(      row=1, column=0, columnspan=4 )

        self.targetSizeLabel.grid(   row=2, column=0 )
        self.targetSizeSpin.grid(    row=2, column=1, columnspan=2 )
        self.targetSizeUnitMenu.grid(row=2, column=3 )

        self.srcButton.grid(         row=3, column=0 )
        self.compressButton.grid(    row=2, column=4 )


        self.dstImgLabel.grid(       row=0, column=5, columnspan=4)
        self.dstSizeLabel.grid(      row=1, column=5, columnspan=2)
        self.qualityLabel.grid(      row=1, column=7, columnspan=2)

        self.saveButton.grid(        row=2, column=5, columnspan=4 )

        # Menu
        self.menu = tkinter.Menu(self)
        menu_help = tkinter.Menu(self.menu, tearoff=False)
        menu_help.add_command(label="About", command=lambda: None)
        menu_help.add_checkbutton(label="Dark Mode", command=lambda: sv_ttk.set_theme("dark" if self.isDarkMode.get() else 'light'), variable=self.isDarkMode)
        self.menu.add_cascade(label='Help', menu=menu_help)
        self.root.config(menu = self.menu)


    # UI = f(state), this is the `f`
    def update_ui(self):
        self.srcSizeLabel['text'] = f"{USize(self.src_file_size)}"
        if self.dst_img_bytes != None:
            self.dstSizeLabel['text'] = f"{USize(len(self.dst_img_bytes))}"
        #self.targetSizeSpin['to'] = self.src_file_size
        #self.targetSizeSpin['from'] = self.src_file_size // 20
        self.targetSizeLabel['text'] = f"Target:"
        self.qualityLabel['text'] = f"Quality: {self.quality}%"

        if(self.dst_img_bytes != None):
            self.dstImage = ImageTk.PhotoImage(Image.open(io.BytesIO(self.dst_img_bytes)).resize( smart_fit(self.src_img_size, UI_IMAGE_SIZE)) ) # use self. to Avoid GC
            self.dstImgLabel['image'] = self.dstImage #, size=None  # ToDo: Auto size


    @ui_action
    def set_src(self):
        src_path = Path(askopenfilename(filetypes= [('Image','*.jpg *.png')] ))
        if not (src_path.exists() and src_path.is_file()):
            return
        
        self.src_path = src_path
        self.src_file_size = os.path.getsize(self.src_path)

        src_img = Image.open(self.src_path)
        self.src_img_size = src_img.size
        self.srcImage = ImageTk.PhotoImage(Image.open(self.src_path).resize( smart_fit(self.src_img_size, UI_IMAGE_SIZE)) ) #, size=None # use self.srcImage to Avoid GC # ToDo: Auto size
        self.srcImgLabel['image'] = self.srcImage #, size=None  # ToDo: Auto size

    @ui_action
    def compress_img(self):
        target_size = int(USize(self.target_size_num, self.target_size_unit.get()))

        if self.src_file_size <= target_size:
            showinfo("Already satisfied", "File size already satisfied")
            return

        src_img_cv2 = cv2.imdecode(np.fromfile(self.src_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED) # cv2.imread does not support Unicode, use cv2.imdecode(np.fromfile(...)) instead

        try:
            self.quality, self.dst_img_bytes = smart_compress.smart_compress( src_img_cv2 , target_size) # ToDo: Avoid twice read, try convert from src_img_pil or use bytes
        except UserWarning as err:
            showwarning("Warning", str(err))
            return
        except Exception as err:
            showerror("Error", err)
            return

    @ui_action
    def save_dst(self):
        dst_io = asksaveasfile(mode='wb', confirmoverwrite=True, defaultextension='jpg',initialfile='compressed.jpg', filetypes= [('Image','*.jpg')])
        if dst_io==None:
            return
        
        dst_io.write(self.dst_img_bytes)
        dst_io.close()


if __name__=='__main__':
    root = tkinter.Tk()
    root.geometry("1024x600")

    mainframe = MainFrame(root)
    # 设置窗口标题:
    mainframe.master.title('Size Based Img Compressor')

    # This is where the magic happens
    sv_ttk.set_theme("light")

    # 主消息循环:
    root.mainloop()