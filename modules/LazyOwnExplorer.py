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
    def __init__(self, get_suggestions_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_suggestions = get_suggestions_func  # Función que devuelve sugerencias
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
            words = self.get_suggestions(self.var.get())  # Llama a la función dinámica
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

    def comparison(self, pattern):
        # Método auxiliar para filtrar
        return [w for w in self.get_suggestions(pattern) if w.lower().startswith(pattern.lower())]
class LazyOwnGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LazyOwn - Análisis de Binarios")
        self.geometry("1366x768")  # Establecer la resolución de la ventana
        
        self.parquet_files = [
            "../parquets/binarios.parquet",           # GTFOBins - lista básica
            "../parquets/detalles.parquet",          # GTFOBins - detalles
            "../parquets/lolbas_index.parquet",      # LOLBAS - índice (puede no tener ejemplo)
            "../parquets/lolbas_details.parquet"     # LOLBAS - detalles con ejemplos
        ]
        self.dataframe = self.load_parquet_files()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Término de búsqueda:")
        self.label.pack(pady=10)

        # Función que devuelve sugerencias basadas en el término actual
        def get_suggestions(term):
            if not term:
                return []
            binaries = self.dataframe['Binary'].dropna().astype(str).unique()
            return [b for b in binaries if b != 'None' and term.lower() in b.lower()]

        self.search_term_entry = AutocompleteEntry(get_suggestions, self)
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
        dataframes = []
        for file in self.parquet_files:
            if not os.path.exists(file):
                print(f"[!] Archivo no encontrado: {file}")
                continue
            try:
                df = pd.read_parquet(file)
                df = df.replace({np.nan: None})  # Limpiar NaN

                # Mapeo unificado de columnas
                if 'Function URL' in df.columns and 'Description' not in df.columns:
                    # Es GTFOBins binarios (binarios.parquet)
                    df = df.rename(columns={'Function Name': 'Function Name'})
                    df['Description'] = ""
                    df['Example'] = ""

                elif 'Function Name' in df.columns and 'Example' in df.columns:
                    # Es GTFOBins detalles (detalles.parquet) o LOLBAS bien formateado
                    pass  # Ya tiene las columnas clave

                elif 'General Description' in df.columns:
                    # Es LOLBAS details
                    df['Description'] = df['General Description'].fillna("") + "\n" + \
                                    df['Description'].astype(str).replace('None', '')
                    df['Binary'] = df['Binary'].str.replace(r'\.exe$', '', case=False, regex=True)

                elif 'URL' in df.columns and 'Functions' in df.columns:
                    # Es lolbas_index.parquet (sin detalles)
                    continue  # Ya está cubierto por lolbas_details

                # Asegurarnos de tener las columnas clave
                required_cols = ['Binary', 'Function Name', 'Description', 'Example']
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = ""

                df = df[required_cols]
                dataframes.append(df)

            except Exception as e:
                print(f"[!] Error leyendo {file}: {e}")

        if not dataframes:
            messagebox.showerror("Error", "No se pudo cargar ningún archivo Parquet.")
            return pd.DataFrame()

        # Concatenar todo
        df = pd.concat(dataframes, ignore_index=True)

        # Limpiar: quitar filas sin 'Example' útil
        df = df.dropna(subset=['Example']).reset_index(drop=True)
        df = df[df['Example'].astype(str).str.strip() != ""].reset_index(drop=True)

        # Unificar nombres de binarios (sin .exe)
        df['Binary'] = df['Binary'].astype(str).str.replace(r'\.exe$', '', case=False, regex=True)

        return df

    def get_unique_values(self):
        if self.dataframe.empty:
            return []
        # Solo tomar los binarios únicos
        binaries = self.dataframe['Binary'].dropna().unique()
        return [b for b in binaries if b and b != 'None']

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
