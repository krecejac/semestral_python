import tkinter as tk
import customtkinter
import src.generator as generator

class App:
    def validate(input):
        if str.isdigit(input) or input == "":
            return True
        return False
    
    def Generate(self):
        util_d = {
        "Mode": self.var_cb.get(),
        "Width": int(self.width_entry.get()),
        "Height": int(self.height_entry.get()),
        "Octaves": self.slider_octav.get(),
        "Persistence": self.slider_persi.get(),
        "Lacunarity": self.slider_lacun.get()
    } 
        generator.noise_create(util_d)

    data=("Terra", "Dagobah", "Tatooine", "Hoth", "Kashyyyk", "Kamino", "Mustafar")
    #frames&windows
    root = customtkinter.CTk()
    frame = customtkinter.CTkFrame(root)
    frame_cb = customtkinter.CTkFrame(root)
    frame_entries = customtkinter.CTkFrame(root)
    l_frames = [frame, frame_cb, frame_entries]

    #labels
    main_label = customtkinter.CTkLabel(root, text="Configurations", pady=20)
    label_cb = customtkinter.CTkLabel(frame_cb, text='Choose mode: ', width=15)
    label_entry_height = customtkinter.CTkLabel(frame_entries, text="Height:")
    label_entry_width = customtkinter.CTkLabel(frame_entries, text="Width:")
    label_slid_oct = customtkinter.CTkLabel(frame, text="Octaves")
    label_slid_per = customtkinter.CTkLabel(frame, text="Persistance")
    label_slid_lac = customtkinter.CTkLabel(frame, text="Lacunarity")
    l_labels = [main_label,label_cb,label_entry_height,label_entry_width]

    #vars
    var_cb = tk.StringVar()
    var_cb.set("Terra")
    var_octav = tk.IntVar()
    var_octav.set(7)
    var_persi = tk.DoubleVar()
    var_persi.set(0.6)
    var_lacun = tk.DoubleVar()
    var_lacun.set(2.0)
    
    #Combobox
    cb= customtkinter.CTkComboBox(frame_cb, values=data, state='readonly', variable=var_cb, width=100, text_color='black')

    #sliders
    vcmd = (root.register(validate)) #command handler
    slider_octav = customtkinter.CTkSlider(frame, from_=1, to=10, orientation=tk.HORIZONTAL,
                                            width=200, variable=var_octav)
    slider_persi = customtkinter.CTkSlider(frame, from_=0.1, to=1.0,
                                            orientation=tk.HORIZONTAL, width=200,
                                            variable=var_persi)
    slider_lacun = customtkinter.CTkSlider(frame, from_=0.1, to=3.0, orientation=tk.HORIZONTAL,
                                            width=200, variable=var_lacun)

    #entries
    width_entry = customtkinter.CTkEntry(frame_entries, width=100, validate='all', validatecommand=(vcmd, '%P'))
    height_entry = customtkinter.CTkEntry(frame_entries, width=100, validate='all', validatecommand=(vcmd, '%P'))

    #buttons
    
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.root.title('Procedural island generator')
        self.root.geometry("700x400")
        self.pack_widgets( [self.frame, self.frame_cb, self.frame_entries] )
        self.grid_it()
        generate_button = customtkinter.CTkButton(self.root, width=100, height=75, text="Generate island!",command=self.Generate)
        self.width_entry.insert(0, 1024)
        self.height_entry.insert(0, 1024)
        generate_button.pack()

    def pack_widgets(self, list_widgets:list):
        self.main_label.pack(pady=10)
        for frame in list_widgets:
            frame.pack(pady=5)

    def grid_it(self):
        self.label_slid_oct.grid(row= 0,column= 0)
        self.label_slid_per.grid(row= 0,column= 1)
        self.label_slid_lac.grid(row= 0,column= 2)
        self.slider_octav.grid(row=1,column=0)
        self.slider_persi.grid(row=1,column=1)
        self.slider_lacun.grid(row=1,column=2)
        self.cb.grid(row=0, column=1)
        self.label_cb.grid(row=0, column=0)
        self.label_entry_width.grid(row=0, column=0)
        self.label_entry_height.grid(row=0, column=1)
        self.width_entry.grid(row=1,column=0)
        self.height_entry.grid(row=1,column=1)