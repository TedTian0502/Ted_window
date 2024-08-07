import tkinter as tk
from tkinter import messagebox
from collections import deque

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("圓圈叉叉遊戲")
        self.current_player = "Red"  # 初始玩家
        self.moves = {"Red": 0, "Blue": 0}  # 跟踪每個玩家的步數
        self.game_active = True  # 確保遊戲在開始時是活動的
        self.button_history = deque()  # 保存按鈕歷史 (button, symbol)
        self.symbol_count = {"O": 0, "X": 0}  # 跟踪每個符號的顯示次數
        self.create_widgets()

    def create_widgets(self):
        # 創建主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 創建左側框架
        game_frame = tk.Frame(main_frame)
        game_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # 創建右側框架
        control_frame = tk.Frame(main_frame)
        control_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # 創建9個按鈕
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c] = tk.Button(game_frame, text="Click", width=5, height=2,
                                               command=lambda r=r, c=c: self.on_button_click(r, c))
                self.buttons[r][c].grid(row=r, column=c, padx=5, pady=5)
        
        # 創建角色選擇按鈕
        self.red_button = tk.Button(control_frame, text="Red", command=self.set_red)
        self.red_button.pack(pady=5)
        
        self.blue_button = tk.Button(control_frame, text="Blue", command=self.set_blue)
        self.blue_button.pack(pady=5)
        
        # 創建顯示當前玩家的標籤
        self.status_label = tk.Label(control_frame, text=f"當前玩家: {self.current_player}")
        self.status_label.pack(pady=10)
        
        self.last_player = None  # 跟踪上一次執行操作的玩家

    def set_red(self):
        if not self.game_active:
            return
        self.current_player = "Red"
        self.status_label.config(text="當前玩家: Red")
        self.last_player = None  # 重置上一個玩家

    def set_blue(self):
        if not self.game_active:
            return
        self.current_player = "Blue"
        self.status_label.config(text="當前玩家: Blue")
        self.last_player = None  # 重置上一個玩家
        
    def on_button_click(self, r, c):
        if not self.game_active:
            return

        button = self.buttons[r][c]
        if button["text"] != "Click":
            messagebox.showwarning("警告", "這個位置已經被佔用！")
            return

        if self.last_player == self.current_player:
            messagebox.showwarning("警告", "請勿連續動作！")
            return

        # 確定當前玩家的符號
        symbol = "O" if self.current_player == "Red" else "X"
        self.update_button_history(button, symbol)
        
        self.moves[self.current_player] += 1
        self.last_player = self.current_player

        # 檢查是否有勝利
        if self.check_winner():
            messagebox.showinfo("遊戲結束", f"{self.current_player} 勝利！")
            self.game_active = False
            self.root.after(2000, self.root.quit)  # 2秒後關閉窗口

    def update_button_history(self, button, symbol):
        # 移除超過 3 次的最早按鈕
        while self.symbol_count[symbol] >= 3:
            old_button, old_symbol = self.button_history.popleft()
            if old_symbol == symbol:
                old_button["text"] = "Click"
                self.symbol_count[symbol] -= 1

        # 更新按鈕內容
        button["text"] = symbol
        self.button_history.append((button, symbol))
        self.symbol_count[symbol] += 1

    def check_winner(self):
        # 獲取當前玩家的符號
        symbol = "O" if self.current_player == "Red" else "X"
        # 檢查行、列和對角線
        for i in range(3):
            if all(self.buttons[i][j]["text"] == symbol for j in range(3)) or \
               all(self.buttons[j][i]["text"] == symbol for j in range(3)):
                return True

        if all(self.buttons[i][i]["text"] == symbol for i in range(3)) or \
           all(self.buttons[i][2 - i]["text"] == symbol for i in range(3)):
            return True

        return False

# 創建主窗口
root = tk.Tk()
app = TicTacToeApp(root)
root.mainloop()
