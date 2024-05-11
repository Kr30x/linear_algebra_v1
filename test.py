import tkinter as tk
from tkinter import ttk

class MatrixCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")

        # Sidebar with notebook widget
        self.sidebar = ttk.Frame(root)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.notebook = ttk.Notebook(self.sidebar)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Matrix Calculator page
        self.matrix_calculator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.matrix_calculator_frame, text="Matrix Calculator")
        self.create_matrix_calculator_page(self.matrix_calculator_frame)

        # Find Basis page
        self.find_basis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.find_basis_frame, text="Find Basis")
        self.create_find_basis_page(self.find_basis_frame)

    def create_matrix_calculator_page(self, frame):
        # Add Matrix Calculator widgets to the frame
        pass

    def create_find_basis_page(self, frame):
        # Add Find Basis widgets to the frame
        pass

def main():
    root = tk.Tk()
    app = MatrixCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
