import tkinter as tk
import random
import heapq
import time

class Puzzle8:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Game")
        
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.board = self.goal_state[:]
        self.buttons = []
        self.move_count = 0
        self.start_time = time.time()
        
        self.create_widgets()
        self.shuffle_board()
    
    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0)
        
        for i in range(9):
            btn = tk.Button(self.frame, text='', font=('Arial', 24), width=4, height=2,
                            command=lambda i=i: self.move_tile(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)
        
        self.reset_btn = tk.Button(self.root, text="Reiniciar", command=self.shuffle_board)
        self.reset_btn.grid(row=1, column=0, pady=10)
        
        self.solve_btn = tk.Button(self.root, text="Resolver", command=self.solve_puzzle)
        self.solve_btn.grid(row=2, column=0, pady=10)
    
    def shuffle_board(self):
        random.shuffle(self.board)
        while not self.is_solvable():
            random.shuffle(self.board)
        self.move_count = 0
        self.start_time = time.time()
        self.update_board()
    
    def update_board(self):
        for i in range(9):
            value = self.board[i]
            self.buttons[i].config(text=str(value) if value != 0 else '', state=tk.NORMAL if value != 0 else tk.DISABLED)
        if self.board == self.goal_state:
            self.show_victory_screen()
    
    def move_tile(self, index):
        zero_index = self.board.index(0)
        if index in self.get_adjacent_indices(zero_index):
            self.board[zero_index], self.board[index] = self.board[index], self.board[zero_index]
            self.move_count += 1
            self.update_board()
    
    def get_adjacent_indices(self, index):
        row, col = index // 3, index % 3
        moves = []
        if row > 0: moves.append(index - 3)
        if row < 2: moves.append(index + 3)
        if col > 0: moves.append(index - 1)
        if col < 2: moves.append(index + 1)
        return moves
    
    def is_solvable(self):
        inversions = sum(
            1
            for i in range(len(self.board))
            for j in range(i + 1, len(self.board))
            if self.board[i] and self.board[j] and self.board[i] > self.board[j]
        )
        return inversions % 2 == 0
    
    def manhattan_distance(self, board):
        distance = 0
        for i, value in enumerate(board):
            if value == 0:
                continue
            goal_index = self.goal_state.index(value)
            current_x, current_y = i % 3, i // 3
            goal_x, goal_y = goal_index % 3, goal_index // 3
            distance += abs(current_x - goal_x) + abs(current_y - goal_y)
        return distance
    
    def solve_puzzle(self):
        def reconstruct_path(came_from, current):
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        
        start = tuple(self.board)
        open_set = [(self.manhattan_distance(start), start)]
        heapq.heapify(open_set)
        came_from = {}
        g_score = {start: 0}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            if list(current) == self.goal_state:
                path = reconstruct_path(came_from, current)
                for step in path:
                    self.board = list(step)
                    self.update_board()
                    self.root.update()
                    self.root.after(200)
                    self.move_count += 1
                return
            
            zero_index = current.index(0)
            for move in self.get_adjacent_indices(zero_index):
                new_board = list(current)
                new_board[zero_index], new_board[move] = new_board[move], new_board[zero_index]
                new_state = tuple(new_board)
                
                temp_g_score = g_score[current] + 1
                if new_state not in g_score or temp_g_score < g_score[new_state]:
                    g_score[new_state] = temp_g_score
                    f_score = temp_g_score + self.manhattan_distance(new_state)
                    heapq.heappush(open_set, (f_score, new_state))
                    came_from[new_state] = current

    def show_victory_screen(self):
        end_time = time.time()
        elapsed_time = round(end_time - self.start_time, 2)
        
        victory_window = tk.Toplevel(self.root)
        victory_window.title("¡Victoria!")
        
        tk.Label(victory_window, text=f"¡Felicidades! Has resuelto el puzzle.", font=("Arial", 16)).pack(pady=10)
        tk.Label(victory_window, text=f"Movimientos: {self.move_count}", font=("Arial", 14)).pack(pady=5)
        tk.Label(victory_window, text=f"Tiempo: {elapsed_time} segundos", font=("Arial", 14)).pack(pady=5)
        
        tk.Button(victory_window, text="Cerrar", command=victory_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    game = Puzzle8(root)
    root.mainloop()