import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import datasource
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.selectdata = None  # Placeholder for the data
        self.canvas1 = None  # Canvas for the first plot
        self.canvas2 = None  # Canvas for the second plot
        self.fig1 = None  # Figure for the first plot
        self.fig2 = None  # Figure for the second plot
        self.top_window = None  # To store reference to top-level window for charts

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        self.command_menu = tk.Menu(self.menubar)
        self.command_menu.add_command(label="設定", command=self.menu_setting_click)
        self.command_menu.add_command(label="離開", command=self.destroy)
        self.menubar.add_cascade(label="選項", menu=self.command_menu)

        self.topFrame = ttk.Labelframe(self)
        self.topFrame.pack(side=tk.TOP)

        self.bottomFrame = ttk.LabelFrame(self)
        self.bottomFrame.pack()

        logo_path = './Images/pic_1.jpg'
        if os.path.exists(logo_path):
            logoImage = Image.open(logo_path)
            resizeImage = logoImage.resize((460, 250), Image.LANCZOS)
            self.logoTkimage = ImageTk.PhotoImage(resizeImage)
            self.canvas = tk.Canvas(self.topFrame, width=500, height=250)
            self.canvas.pack()
            self.canvas.create_image(20, 30, image=self.logoTkimage, anchor='nw')
        else:
            self.canvas = tk.Canvas(self.topFrame, width=500, height=250, bg='white')
            self.canvas.pack()
            self.canvas.create_text(250, 125, text="Image not found", font=("Helvetica", 20))

        self.combobox_frame = ttk.Frame(self.topFrame)
        self.combobox_frame.pack(pady=10)

        self.combobox_label = ttk.Label(self.combobox_frame, text="Select Country:")
        self.combobox_label.grid(row=0, column=0, padx=(10, 0))

        self.combobox = ttk.Combobox(self.combobox_frame, state="readonly")
        self.combobox.grid(row=0, column=1, padx=10)

        self.chart_type_label = ttk.Label(self.combobox_frame, text="Select Chart Type:")
        self.chart_type_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        self.chart_type_combobox = ttk.Combobox(self.combobox_frame, values=["折線圖", "散佈圖"], state="readonly")
        self.chart_type_combobox.grid(row=1, column=1, padx=10, pady=(10, 0))
        self.chart_type_combobox.current(0)

        self.selectdata = datasource.getInfo()

        country_list = self.selectdata['country'].unique().tolist()
        country_list = sorted(country_list)
        country_list.insert(0, '請選擇一個國家vvv')
        self.combobox_values = tuple(country_list)
        self.combobox['values'] = self.combobox_values
        self.combobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.update_treeview)

        columns = ('#1', '#2', '#3', '#4', '#5', '#6')
        self.tree = ttk.Treeview(self.bottomFrame, columns=columns, show='headings')
        self.tree.heading('#1', text='year', anchor='center')
        self.tree.column("#1", minwidth=0, width=80)
        self.tree.heading('#2', text='co2', anchor='center')
        self.tree.column("#2", minwidth=0, width=80)
        self.tree.heading('#3', text='co2_per_capita', anchor='center')
        self.tree.column("#3", minwidth=0, width=100)
        self.tree.heading('#4', text='energy_per_capita', anchor='center')
        self.tree.column("#4", minwidth=0, width=110)
        self.tree.heading('#5', text='ghg_per_capita', anchor='center')
        self.tree.column("#5", minwidth=0, width=100)
        self.tree.heading('#6', text='population')
        self.tree.column("#6", minwidth=0, width=100)
        self.tree.pack(side=tk.LEFT)

        for i in range(self.selectdata['country'].size):
            self.tree.insert('', tk.END, values=[self.selectdata.iloc[i, 1], self.selectdata.iloc[i, 2], self.selectdata.iloc[i, 3],self.selectdata.iloc[i, 4], self.selectdata.iloc[i, 5], self.selectdata.iloc[i, 6]], tags=self.selectdata.index[i])

        scrollbar = ttk.Scrollbar(self.bottomFrame, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def menu_setting_click(self):
        pass

    def update_treeview(self, event):
        combobox = event.widget
        selected_index = combobox.current()
        selected_country = self.combobox_values[selected_index]

        if selected_country != '請選擇國家別vvv':

            filtered_data = self.selectdata[self.selectdata['country'] == selected_country]
            self.tree.delete(*self.tree.get_children())
            for i in range(filtered_data.shape[0]):
                self.tree.insert('', tk.END, values=[filtered_data.iloc[i, 1], filtered_data.iloc[i, 2], filtered_data.iloc[i, 3], filtered_data.iloc[i, 4], filtered_data.iloc[i, 5], filtered_data.iloc[i, 6]], tags=filtered_data.index[i])

    def show_line_chart(self):
        selected_country = self.combobox.get()
        if selected_country == '請選擇一個國家vvv':
            messagebox.showwarning("未選擇國家", "請先選擇一個國家!")
            return

        # Close any existing plot window
        self.close_plot()

        filtered_data = self.selectdata[self.selectdata['country'] == selected_country]
        years = filtered_data['year']
        energy_consumption = filtered_data['energy_per_capita']
        co2_emissions = filtered_data['co2_per_capita']

        top_window = tk.Toplevel(self)
        top_window.title(f'Charts for {selected_country}')
        self.top_window = top_window

        if self.chart_type_combobox.get() == "折線圖":
            self.fig1 = plt.figure(figsize=(6, 4))
            plt.plot(years, energy_consumption, marker='o', linestyle='-', color='b')
            plt.xlabel('Year')
            plt.ylabel('Energy Consumption')
            plt.title(f'Energy Consumption in {selected_country}')
            plt.grid(True)
            plt.tight_layout()

            self.canvas1 = FigureCanvasTkAgg(self.fig1, master=top_window)
            self.canvas1.draw()
            self.canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.fig2 = plt.figure(figsize=(6, 4))
            plt.plot(years, co2_emissions, marker='s', linestyle='-', color='g')
            plt.xlabel('Year')
            plt.ylabel('CO2 Emissions')
            plt.title(f'CO2 Emissions in {selected_country}')
            plt.grid(True)
            plt.tight_layout()

            self.canvas2 = FigureCanvasTkAgg(self.fig2, master=top_window)
            self.canvas2.draw()
            self.canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            self.close_button = ttk.Button(top_window, text="Close Plot", command=self.close_plot)
            self.close_button.pack(side='bottom', padx=10, pady=5)

        elif self.chart_type_combobox.get() == "散佈圖":
            self.fig2 = plt.figure(figsize=(6, 4))
            plt.scatter(filtered_data['energy_per_capita'], filtered_data['co2_per_capita'], color='g')
            plt.xlabel('Energy per Capita')
            plt.ylabel('CO2 per Capita')
            plt.title(f'Scatter Plot of Energy vs CO2 Emissions in {selected_country}')
            plt.grid(True)
            plt.tight_layout()

            slope, intercept, r_value, p_value, std_err = stats.linregress(filtered_data['energy_per_capita'], filtered_data['co2_per_capita'])
            line = slope * filtered_data['energy_per_capita'] + intercept
            plt.plot(filtered_data['energy_per_capita'], line, color='red', label='Trend Line')

            equation_text = f'y = {slope:.4f}x + {intercept:.4f}'
            r_squared_text = f'R^2 = {r_value**2:.4f}'
            plt.text(0.1, 0.9, equation_text, fontsize=10, transform=plt.gca().transAxes)
            plt.text(0.1, 0.85, r_squared_text, fontsize=10, transform=plt.gca().transAxes)

            self.canvas2 = FigureCanvasTkAgg(self.fig2, master=top_window)
            self.canvas2.draw()
            self.canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.close_button = ttk.Button(top_window, text="Close Plot", command=self.close_plot)
            self.close_button.pack(side='bottom', padx=10, pady=5)

    def close_plot(self):
        if self.top_window:
            self.top_window.destroy()
            self.top_window = None

        if self.canvas1:
            self.canvas1.get_tk_widget().pack_forget()
            self.canvas1.get_tk_widget().destroy()
            self.canvas1 = None

        if self.fig1:
            plt.close(self.fig1)
            self.fig1 = None

        if self.canvas2:
            self.canvas2.get_tk_widget().pack_forget()
            self.canvas2.get_tk_widget().destroy()
            self.canvas2 = None

        if self.fig2:
            plt.close(self.fig2)
            self.fig2 = None

        if hasattr(self, 'close_button') and self.close_button:
            self.close_button.pack_forget()
            self.close_button.destroy()
            self.close_button = None

    def create_widgets(self):
        self.plot_button = ttk.Button(self.combobox_frame, text="查看線圖", command=self.show_line_chart)
        self.plot_button.grid(row=1, column=2, padx=10, pady=(10, 0))

    def on_closing(self):
        self.destroy()

    def run(self):
        self.title("GHG Data")
        self.geometry("700x600")
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

if __name__ == '__main__':
    window = MyWindow()
    window.run()
