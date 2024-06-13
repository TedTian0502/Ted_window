import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import YouBike_data  # 導入您的 YouBike_data 模塊

class Window(ThemedTk):
    def __init__(self, theme:str|None = None, **kwargs):
        super().__init__(theme=theme, **kwargs)

        self.title('YouBike2.0 臺北市公共自行車即時資訊')
        self.geometry('820x200')  # 調整視窗寬度

        columns = ('sna', 'sarea', 'mday', 'ar', 'act', 'updateTime', 'total', 'available_rent_bikes', 'latitude', 'longitude', 'available_return_bikes')
        tree = ttk.Treeview(self, columns=columns, show='headings')

        # 將所有標題和文字置中對齊，並設定寬度大小
        for col in columns:
            tree.heading(col, text=col, anchor=tk.CENTER)
            tree.column(col, anchor=tk.CENTER, minwidth=100, width=150)
            
        tree.heading('sna', text='Station Name') 
        tree.heading('sarea', text='Station Area')
        tree.heading('mday', text='Data Update Time')
        tree.heading('ar', text='Address')
        tree.heading('act', text='Active')
        tree.heading('updateTime', text='UpdateTime')
        tree.heading('total', text='Total')
        tree.heading('available_rent_bikes', text='Available Rent Bikes')
        tree.heading('latitude', text='Latitude')
        tree.heading('longitude', text='Longitude')
        tree.heading('available_return_bikes', text='Available Return Bikes')

        try:
            ubike = YouBike_data.load_data()
        except Exception:
            messagebox.showwarning("出現錯誤","資料未能成功下載")
        else:
            for station in ubike:
                tree.insert('', tk.END, values=tuple(station.values()))

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                messagebox.showinfo(title='Information', message=','.join(map(str, record)))

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')

        # 橫向卷軸
        x_scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=tree.xview)
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        tree.configure(xscrollcommand=x_scrollbar.set)

        # 縱向卷軸
        y_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=y_scrollbar.set)

        # 設置列和行的伸展
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

def main():   
    window = Window(theme='arc')
    window.mainloop()

if __name__ == '__main__':
    main()
