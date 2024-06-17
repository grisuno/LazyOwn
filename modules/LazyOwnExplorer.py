#!/usr/bin/env python3 
#_*_ coding: utf8 _*_
"""
main.py

Autor: Gris Iscomeback 
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: 09/06/2024
Licencia: GPL v3

Descripción: Gui to search in gtfobins db 

██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝

"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Text
import pandas as pd
import os
import numpy as np
import subprocess

class AutocompleteEntry(tk.Entry):
    def __init__(self, lista, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lista = [item for item in lista if item is not None]
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()

        self.var.trace_add('write', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)

        self.lb_up = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = tk.Listbox(width=self["width"])
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, tk.END)
                for w in words:
                    self.lb.insert(tk.END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):
        if self.lb_up:
            self.var.set(self.lb.get(tk.ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)

    def move_up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def move_down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != tk.END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = self.var.get()
        return [w for w in self.lista if w.lower().startswith(pattern.lower())]

class LazyOwnGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LazyOwn - Análisis de Binarios")
        self.geometry("1366x768")  # Establecer la resolución de la ventana
        
        self.parquet_files = ["parquets/binarios.parquet", "parquets/detalles.parquet"]
        self.dataframe = self.load_parquet_files()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Término de búsqueda:")
        self.label.pack(pady=10)

        # Crear AutocompleteEntry
        unique_values = self.get_unique_values()
        self.search_term_entry = AutocompleteEntry(unique_values, self)
        self.search_term_entry.pack(pady=10)
        self.search_term_entry.bind("<Return>", lambda event: self.search())  # Búsqueda al presionar Enter

        self.search_button = tk.Button(self, text="Buscar", command=self.search)
        self.search_button.pack(pady=10)
        
        # Botón para agregar nuevo vector de ataque
        self.new_attack_button = tk.Button(self, text="Nuevo Vector de Ataque", command=self.add_new_attack_vector)
        self.new_attack_button.pack(pady=10)

        # Botón para buscar binarios en el sistema
        self.scan_button = tk.Button(self, text="Buscar Binarios en el Sistema", command=self.scan_system_for_binaries)
        self.scan_button.pack(pady=10)

        # Botón para exportar a CSV
        self.export_button = tk.Button(self, text="Exportar a CSV", command=self.export_to_csv)
        self.export_button.pack(pady=10)

        # Crear el marco para Treeview y Scrollbars
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Crear Treeview
        self.result_tree = ttk.Treeview(self.result_frame, columns=("Binary", "Function Name", "Description", "Example"), show='headings')
        self.result_tree.heading("Binary", text="Binary")
        self.result_tree.heading("Function Name", text="Function Name")
        self.result_tree.heading("Description", text="Description")
        self.result_tree.heading("Example", text="Example")
        
        self.result_tree.column("Binary", width=100, anchor=tk.W)
        self.result_tree.column("Function Name", width=150, anchor=tk.W)
        self.result_tree.column("Description", width=500, anchor=tk.W)
        self.result_tree.column("Example", width=500, anchor=tk.W)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        self.scrollbar_y = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_tree.config(yscrollcommand=self.scrollbar_y.set)
        
        self.scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.result_tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_tree.config(xscrollcommand=self.scrollbar_x.set)

        # Bind double-click event on rows
        self.result_tree.bind("<Double-1>", self.on_row_double_click)

    def load_parquet_files(self):
        dataframes = [pd.read_parquet(file) for file in self.parquet_files if os.path.exists(file)]
        if not dataframes:
            messagebox.showerror("Error", "No se encontraron archivos Parquet.")
            return pd.DataFrame()

        df = pd.concat(dataframes, ignore_index=True)
        df = df.replace({np.nan: None})  # Reemplazar NaN por None para manejar mejor los datos
        return df

    def get_unique_values(self):
        if self.dataframe.empty:
            return []
        unique_values = pd.concat([self.dataframe[col] for col in self.dataframe.columns]).unique()
        return unique_values.tolist()

    def search(self):
        search_term = self.search_term_entry.get()
        if not search_term:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un término de búsqueda.")
            return
        
        # Realizar la búsqueda en el DataFrame
        result = self.search_in_parquet(search_term)
        
        # Limpiar Treeview
        for i in self.result_tree.get_children():
            self.result_tree.delete(i)
        
        # Insertar resultados en el Treeview
        for idx, row in result.iterrows():
            self.result_tree.insert("", "end", values=(row["Binary"], row["Function Name"], row["Description"], row["Example"]))
    
    def search_in_parquet(self, term):
        if self.dataframe.empty:
            return pd.DataFrame()

        result = self.dataframe[self.dataframe.apply(lambda row: row.astype(str).str.contains(term, case=False).any(), axis=1)]
        result = result.dropna(subset=["Example"])  # Filtrar las filas donde 'Example' es NaN
        
        return result

    def on_row_double_click(self, event):
        selected_item = self.result_tree.selection()[0]
        selected_row = self.result_tree.item(selected_item, "values")
        self.show_row_details(selected_row)

    def show_row_details(self, row):
        detail_window = tk.Toplevel(self)
        detail_window.title("Detalles de la fila")

        tk.Label(detail_window, text="Binary:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(detail_window, text=row[0]).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        tk.Label(detail_window, text="Function Name:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(detail_window, text=row[1]).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        tk.Label(detail_window, text="Description:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        description_text = Text(detail_window, wrap=tk.WORD, height=10, width=50)
        description_text.grid(row=2, column=1, padx=10, pady=5)
        description_text.insert(tk.END, row[2])
        description_text.config(state=tk.DISABLED)

        tk.Label(detail_window, text="Example:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        example_text = Text(detail_window, wrap=tk.WORD, height=10, width=50)
        example_text.grid(row=3, column=1, padx=10, pady=5)
        example_text.insert(tk.END, row[3])
        example_text.config(state=tk.DISABLED)

    def add_new_attack_vector(self):
        new_vector_window = tk.Toplevel(self)
        new_vector_window.title("Agregar Nuevo Vector de Ataque")

        tk.Label(new_vector_window, text="Binary:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        binary_entry = tk.Entry(new_vector_window)
        binary_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(new_vector_window, text="Function Name:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        function_name_entry = tk.Entry(new_vector_window)
        function_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(new_vector_window, text="Description:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        description_entry = Text(new_vector_window, wrap=tk.WORD, height=10, width=50)
        description_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(new_vector_window, text="Example:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        example_entry = Text(new_vector_window, wrap=tk.WORD, height=10, width=50)
        example_entry.grid(row=3, column=1, padx=10, pady=5)

        def save_new_vector():
            binary = binary_entry.get()
            function_name = function_name_entry.get()
            description = description_entry.get("1.0", tk.END).strip()
            example = example_entry.get("1.0", tk.END).strip()

            if not binary or not function_name or not description or not example:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            
            new_data = pd.DataFrame({
                "Binary": [binary],
                "Function Name": [function_name],
                "Description": [description],
                "Example": [example]
            })

            self.dataframe = pd.concat([self.dataframe, new_data], ignore_index=True)

            # Guardar los datos actualizados en los archivos Parquet
            for file in self.parquet_files:
                self.dataframe.to_parquet(file)

            messagebox.showinfo("Éxito", "Nuevo vector de ataque agregado con éxito.")
            new_vector_window.destroy()

        tk.Button(new_vector_window, text="Guardar", command=save_new_vector).grid(row=4, column=1, padx=10, pady=10, sticky=tk.E)

    def scan_system_for_binaries(self):
        def is_binary(file_path):
            try:
                result = subprocess.run(['file', '--mime', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return b'application/x-executable' in result.stdout
            except Exception as e:
                return False

        binaries = []
        for root, dirs, files in os.walk('/'):
            for file in files:
                file_path = os.path.join(root, file)
                if is_binary(file_path):
                    binaries.append(file_path)
        
        self.show_scan_results(binaries)

    def show_scan_results(self, binaries):
        result_window = tk.Toplevel(self)
        result_window.title("Resultados de la Búsqueda de Binarios")

        tk.Label(result_window, text="Binarios encontrados:").pack(pady=10)
        listbox = tk.Listbox(result_window, width=100, height=20)
        listbox.pack(pady=10)
        
        for binary in binaries:
            listbox.insert(tk.END, binary)

    def export_to_csv(self):
        if self.dataframe.empty:
            messagebox.showerror("Error", "No hay datos para exportar.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.dataframe.to_csv(file_path, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados con éxito a {file_path}")

if __name__ == "__main__":
    app = LazyOwnGUI()
    app.mainloop()
