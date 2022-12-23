import tkinter as tk
import customtkinter
from tkinter.ttk import Combobox
import src.generator as generator

def Generate():
    util_d = {
        "Mode": var_cb.get(),
        "Width": int(width_entry.get()),
        "Height": int(height_entry.get()),
        "Octaves": slider_octav.get(),
        "Persistence": slider_persi.get(),
        "Lacunarity": slider_lacun.get()
    } 
    generator.noise_create(util_d)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
bg_col = '#547890'
root = customtkinter.CTk()
#root.configure(background=bg_col)
data=("Terra", "Dagobah", "Tatooine", "Hoth", "Kashyyyk", "Kamino", "Mustafar")
root.title('Procedural island generator')
root.geometry("700x400")
main_label = customtkinter.CTkLabel(root, text="Configurations", pady=20)
main_label.pack()

frame = customtkinter.CTkFrame(root)
frame.pack()

frame_cb = customtkinter.CTkFrame(root)
frame_cb.pack()
label_cb = customtkinter.CTkLabel(frame_cb, text='Choose mode: ', width=15)

frame_entries = customtkinter.CTkFrame(root)
frame_entries.pack()
label_entry_width = customtkinter.CTkLabel(frame_entries, text="Width:")
label_entry_height = customtkinter.CTkLabel(frame_entries, text="Height:")

var_cb = tk.StringVar()
var_octav = tk.IntVar()
var_persi = tk.DoubleVar()
var_lacun = tk.DoubleVar()
var_cb.set("Terra")
var_octav.set(7)
var_persi.set(0.6)
var_lacun.set(2.0)
cb= customtkinter.CTkComboBox(frame_cb, values=data, state='readonly', variable=var_cb, width=20)
slider_octav = customtkinter.CTkSlider(frame, from_=1, to=10, orientation=tk.HORIZONTAL,
                                        width=200, variable=var_octav)
slider_persi = customtkinter.CTkSlider(frame, from_=0.1, to=1.0,
                                        orientation=tk.HORIZONTAL, width=200,
                                        variable=var_persi)
slider_lacun = customtkinter.CTkSlider(frame, from_=0.1, to=3.0, orientation=tk.HORIZONTAL,
                                        width=200, variable=var_lacun)

def validate(input):
    if str.isdigit(input) or input == "":
        return True
    return False

vcmd = (root.register(validate))
width_entry = customtkinter.CTkEntry(frame_entries, width=15, validate='all', validatecommand=(vcmd, '%P'))
width_entry.insert(0, 1024)
height_entry = customtkinter.CTkEntry(frame_entries, width=15, validate='all', validatecommand=(vcmd, '%P'))
height_entry.insert(0, 1024)

generate_button = customtkinter.CTkButton(root, text="Generate island!",command=Generate)

slider_octav.grid(row=0,column=0)
slider_persi.grid(row=0,column=1)
slider_lacun.grid(row=0,column=2)
cb.grid(row=0, column=1)
label_cb.grid(row=0, column=0)
label_entry_width.grid(row=0, column=0)
label_entry_height.grid(row=0, column=1)
width_entry.grid(row=1,column=0)
height_entry.grid(row=1,column=1)
generate_button.pack()