import tkinter as tk
from fractions import Fraction
from tkinter import ttk

import numpy as np
import pyperclip

from operations import findbasis


class Page:
    def __init__(self, root):
        self.root = root

        label = ttk.Label(root, text="Import your vectors in this table\n\nEach vector should be a row!", font=("Arial", 12))
        label.grid(row=0, column=0, padx=10, pady=10)

        # Use Fractions checkbox
        self.use_fraction = tk.BooleanVar(value=False)
        self.use_fraction_checkbox = ttk.Checkbutton(root, text="Use Fractions", variable=self.use_fraction)
        self.use_fraction_checkbox.grid(row=10, column=0, padx=(0,0), pady=5)

        # Step by step LaTeX checkbox
        self.detailed_documentation = tk.BooleanVar(value=False)
        self.detailed_documentation_checkbox = ttk.Checkbutton(root, text="Step by step LaTeX",
                                                               variable=self.detailed_documentation)
        self.detailed_documentation_checkbox.grid(row=10, column=1, padx=(0,50), pady=5)

        # Matrix dimensions
        self.matrix1_rows = tk.IntVar(value=2)
        self.matrix1_cols = tk.IntVar(value=2)

        # Frame to hold the input matrices and buttons for Matrix 1
        self.matrix_frame1 = ttk.LabelFrame(root, text="Vector Matrix")
        self.matrix_frame1.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.matrix1_entries_frame = ttk.Frame(self.matrix_frame1)
        self.matrix1_entries_frame.grid(row=0, column=0, padx=5, pady=5)
        self.matrix1_bottom_buttons_frame = ttk.Frame(self.matrix_frame1)
        self.matrix1_bottom_buttons_frame.grid(row=1, column=0, padx=5, pady=5)
        self.matrix1_side_buttons_frame = ttk.Frame(self.matrix_frame1)
        self.matrix1_side_buttons_frame.grid(row=0, column=1, padx=5, pady=5)

        # Entry fields for matrix elements of Matrix 1
        self.matrix1_entries = self.create_matrix_entries(self.matrix1_entries_frame, self.matrix1_rows,
                                                          self.matrix1_cols)

        # Buttons to change matrix dimensions for Matrix 1
        ttk.Button(self.matrix1_bottom_buttons_frame, text="+", command=self.increase_matrix_width1,
                   width=2).grid(
            row=0,
            column=1,
            padx=2,
            pady=2)
        ttk.Button(self.matrix1_bottom_buttons_frame, text="-", command=self.decrease_matrix_width1,
                   width=2).grid(
            row=0,
            column=0,
            padx=2,
            pady=2)
        ttk.Button(self.matrix1_side_buttons_frame, text="+", command=self.increase_matrix_height1,
                   width=2).grid(
            row=1,
            column=0,
            padx=5,
            pady=5)
        ttk.Button(self.matrix1_side_buttons_frame, text="-", command=self.decrease_matrix_height1,
                   width=2).grid(
            row=0,
            column=0,
            padx=5,
            pady=5)

        self.one_matrix_operations_frame = ttk.LabelFrame(root, text="Operations")
        self.one_matrix_operations_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.one_matrix_operations = {
            "Find basis": findbasis.find_basis
        }

        # Buttons for matrix operations
        for i, (op_name, op_func) in enumerate(self.one_matrix_operations.items()):
            button = ttk.Button(self.one_matrix_operations_frame, text=op_name,
                                command=lambda func=op_func: self.perform_one_matrix_operation(func))
            button.grid(row=0, column=i , padx=5, pady=5)

        # Text widget to display result
        self.result = None
        self.result_text = tk.Text(root, width=0, height=10, wrap=tk.NONE, font=("Courier", 12))
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        copy_button = ttk.Button(root, text="Copy LaTeX",
                                 command=lambda: self.copy_latex_code())
        copy_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configure column and row weights to center the operation frame
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

    def create_matrix_entries(self, parent, num_rows, num_cols):
        entries = []
        for i in range(num_rows.get()):
            row_entries = []
            for j in range(num_cols.get()):
                # Use Rational type if the checkbox is checked, otherwise use float
                if self.use_fraction.get():
                    entry = ttk.Entry(parent, width=5)
                else:
                    entry = ttk.Entry(parent, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            entries.append(row_entries)
        return entries

    def get_matrices(self):
        matrix1 = self.retrieve_matrix_values(self.matrix1_entries_frame, self.matrix1_rows.get(),
                                              self.matrix1_cols.get())
        return matrix1

    def retrieve_matrix_values(self, frame, num_rows, num_cols):
        matrix = []
        for i in range(num_rows):
            row_entries = []
            for j in range(num_cols):
                entry = frame.grid_slaves(row=i, column=j)[0]
                # Convert entry value to Rational if checkbox is checked, otherwise convert to float
                value = entry.get()
                if self.use_fraction.get():
                    try:
                        value = Fraction(value)
                    except:
                        value = 0
                else:
                    try:
                        value = float(value)
                    except:
                        value = 0
                row_entries.append(value)
            matrix.append(row_entries)
        return np.array(matrix)

    def display_result(self, result):
        self.result_text.delete(1.0, tk.END)  # Clear previous content
        self.result_text.insert(tk.END, str(result))

    def perform_one_matrix_operation(self, operation):
        try:
            matrix1 = self.get_matrices()
            print(matrix1)
            result = operation(matrix1)
            self.result = result
            self.display_result(result)
        except Exception as e:
            self.display_result(f"Error: {str(e)}")


    def increase_matrix_width1(self):
        self.matrix1_cols.set(self.matrix1_cols.get() + 1)
        self.update_matrix_size(self.matrix1_entries_frame, self.matrix1_rows, self.matrix1_cols)

    def decrease_matrix_width1(self):
        if self.matrix1_cols.get() > 1:
            self.matrix1_cols.set(self.matrix1_cols.get() - 1)
            self.update_matrix_size(self.matrix1_entries_frame, self.matrix1_rows, self.matrix1_cols)

    def increase_matrix_height1(self):
        self.matrix1_rows.set(self.matrix1_rows.get() + 1)
        self.update_matrix_size(self.matrix1_entries_frame, self.matrix1_rows, self.matrix1_cols)

    def decrease_matrix_height1(self):
        if self.matrix1_rows.get() > 1:
            self.matrix1_rows.set(self.matrix1_rows.get() - 1)
            self.update_matrix_size(self.matrix1_entries_frame, self.matrix1_rows,
                                    self.matrix1_cols)

    def update_matrix_size(self, frame, num_rows, num_cols):
        # Clear the existing entries
        for widget in frame.winfo_children():
            widget.destroy()

        # Create new entry fields with updated dimensions
        self.create_matrix_entries(frame, num_rows, num_cols)

    def generate_latex_code(self):
        try:
            latex_code = "\\begin{pmatrix}\n"
            for row in self.result:
                latex_code += "    " + " & ".join(map(str, row)) + " \\\\\n"
            latex_code += "\\end{pmatrix}"
            latex_code = latex_code.replace('.0', '')
            return latex_code
        except Exception as e:
            return f"Error: {e}"

    def copy_latex_code(self):
        latex_code = self.generate_latex_code()
        pyperclip.copy(latex_code)

    def update_matrix_entries(self):
        # When the checkbox state changes, update the matrix entries
        self.update_matrix_size(self.matrix1_entries_frame, self.matrix1_rows, self.matrix1_cols)
