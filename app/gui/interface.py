import tkinter as tk
import customtkinter
import src.generator as generator

class App:
    def __init__(self):
        #All of the modes
        data=("Terra", "Dagobah", "Tatooine", "Hoth", "Kashyyyk", "Kamino", "Mustafar")
        
        #frames&windows
        self.framesSetUp()

        #vars
        self.variableSetUp()

        #labels
        self.labelSetUp()

        #Combobox
        self.cb= customtkinter.CTkComboBox(self.frame_cb, values=data, state='readonly', 
                                            variable=self.var_cb, width=100, text_color='black')

        #sliders
        self.sliderSetUp()

        #entries
        self.entriesSetUp()

        #buttons
        self.generate_button = customtkinter.CTkButton(self.root, width=100, height=75, text="Generate island!",command=self.Generate)

        #switches
        self.switchesSetUp()

        #pack everything to the window
        self.setAppearance()

        self.pack_widgets()
        self.grid_it()
        self.generate_button.pack() #Saved as the last widget

    def Generate(self):
        """
        The main passing function connecting graphical interfaces and backend code.
        passes chosen values to the createNoise method used for generation of noises.
        """
        util_d = {
        "Mode": self.var_cb.get(),
        "Width": int(self.width_entry.get()),
        "Height": int(self.height_entry.get()),
        "Octaves": self.slider_octav.get(),
        "Persistence": self.slider_persi.get(),
        "Lacunarity": self.slider_lacun.get(),
        "Print3d": self.noise_3d.get(),
        'Custom': self.custom_noise.get(),
        'Save': self.save_images.get(),
        'Mapping': self.mapping.get()
    }
        generator.createNoise(util_d)

    def validate(self, input):
        #Checks the input of the entries. Only int is OK.
        if str.isdigit(input) or input == "":
            return True
        return False

    def Update_per(self, input):
        #persistance
        self.var_persi_str.set( round(input,2) )
    
    def Update_lac(self, input):
        #lacunarity
        self.var_lacun_str.set( round(input,2) )

    def Update_oct(self, input):
        #octaves
        self.var_octav.set( int(input) )

    def changeSwitchMapping(self):
        self.noise_3d.deselect()

    def changeSwitch3DPlot(self):
        self.mapping.deselect()

    def framesSetUp(self):
        self.root = customtkinter.CTk()
        self.root.resizable(False,False)
        self.frame = customtkinter.CTkFrame(self.root)
        self.frame_cb = customtkinter.CTkFrame(self.root)
        self.frame_entries = customtkinter.CTkFrame(self.root)
        self.frame_switches = customtkinter.CTkFrame(self.root)
    
    def variableSetUp(self):
        self.var_cb = tk.StringVar()
        self.var_cb.set("Terra")
        self.var_octav = tk.IntVar()
        self.var_octav.set(7)
        self.var_persi = tk.DoubleVar()
        self.var_persi.set(0.6)
        self.var_lacun = tk.DoubleVar()
        self.var_lacun.set(2.0)
        self.var_persi_str = tk.StringVar()
        self.var_persi_str.set( round(self.var_persi.get(),2) )
        self.var_lacun_str = tk.StringVar()
        self.var_lacun_str.set( round(self.var_lacun.get(),2) )

    def labelSetUp(self):
        self.main_label = customtkinter.CTkLabel(self.root, text="Configurations:", pady=20,
                                                font=customtkinter.CTkFont("Arial", 30, 'bold'))
        self.label_cb = customtkinter.CTkLabel(self.frame_cb, text='Choose mode: ', width=15)
        self.label_entry_height = customtkinter.CTkLabel(self.frame_entries, text="Height:")
        self.label_entry_width = customtkinter.CTkLabel(self.frame_entries, text="Width:")
        self.label_slid_oct = customtkinter.CTkLabel(self.frame, text="Octaves")
        self.label_slid_per = customtkinter.CTkLabel(self.frame, text="Persistance")
        self.label_slid_lac = customtkinter.CTkLabel(self.frame, text="Lacunarity")
        self.label_val_oct = customtkinter.CTkLabel(self.frame, textvariable=self.var_octav)
        self.label_val_per = customtkinter.CTkLabel(self.frame, textvariable= self.var_persi_str)
        self.label_val_lac = customtkinter.CTkLabel(self.frame, textvariable= self.var_lacun_str)

    def sliderSetUp(self):
        self.vcmd = (self.root.register(self.validate)) #command handler for the entries
        self.slider_octav = customtkinter.CTkSlider(self.frame, from_=1, to=10, orientation=tk.HORIZONTAL,
                                                width=200, variable=self.var_octav, command=self.Update_oct)
        self.slider_persi = customtkinter.CTkSlider(self.frame, from_=0.1, to=1.0, number_of_steps=9,
                                                orientation=tk.HORIZONTAL, width=200,
                                                variable=self.var_persi, command=self.Update_per)
        self.slider_lacun = customtkinter.CTkSlider(self.frame, from_=0.1, to=3.0, orientation=tk.HORIZONTAL,
                                                number_of_steps=29, width=200,
                                                variable=self.var_lacun, command=self.Update_lac)

    def switchesSetUp(self):
        self.save_images = customtkinter.CTkSwitch(self.frame_switches, text="Save Images")
        self.custom_noise = customtkinter.CTkSwitch(self.frame_switches, text="Custom Noise", width=130)
        self.noise_3d = customtkinter.CTkSwitch(self.frame_switches, text="3D Plot", command=self.changeSwitch3DPlot)
        self.mapping = customtkinter.CTkSwitch(self.frame_switches, text="Mapping", width=130, command=self.changeSwitchMapping)

    def setAppearance(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.root.title('Procedural island generator')
        self.root.geometry("700x400")

    def entriesSetUp(self):
        self.width_entry = customtkinter.CTkEntry(self.frame_entries, width=100, validate='all', validatecommand=(self.vcmd, '%P'))
        self.height_entry = customtkinter.CTkEntry(self.frame_entries, width=100, validate='all', validatecommand=(self.vcmd, '%P'))
        self.width_entry.insert(0, 1024)
        self.height_entry.insert(0, 1024)


    def pack_widgets(self):
        self.main_label.pack(pady=10)
        self.frame.pack(pady=5)
        self.frame_cb.pack(pady=5)
        self.frame_entries.pack(anchor='w', pady=5, padx=50)
        self.frame_switches.place(x=420, y=250)

    def grid_it(self):
        #Grids everything nicely to the frames for better appearence
        self.label_slid_oct.grid(row= 0,column= 0)
        self.label_slid_per.grid(row= 0,column= 1)
        self.label_slid_lac.grid(row= 0,column= 2)
        self.slider_octav.grid(row=1,column=0)
        self.slider_persi.grid(row=1,column=1)
        self.slider_lacun.grid(row=1,column=2)
        self.label_val_oct.grid(row=2,column=0)
        self.label_val_per.grid(row=2,column=1)
        self.label_val_lac.grid(row=2,column=2)
        self.cb.grid(row=0, column=1)
        self.label_cb.grid(row=0, column=0)
        self.label_entry_width.grid(row=0, column=0)
        self.label_entry_height.grid(row=0, column=1)
        self.width_entry.grid(row=1,column=0)
        self.height_entry.grid(row=1,column=1)
        self.save_images.grid(row=0, column=0, padx=10)
        self.custom_noise.grid(row=0, column=1)
        self.noise_3d.grid(row=1,column=0)
        self.mapping.grid(row=1,column=1)