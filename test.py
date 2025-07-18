import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
available_fonts = tkFont.families()
for font in sorted(available_fonts):
    print(font)
root.destroy()