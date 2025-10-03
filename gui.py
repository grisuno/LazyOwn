# terminal_tkinter_pty.py
import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import pty
import subprocess
import select

class TerminalEmulator:
    def __init__(self, root):
        self.root = root
        root.title("Terminal con cmd2 (PTY)")

        self.text = scrolledtext.ScrolledText(
            root,
            bg="black",
            fg="green",
            insertbackground="green",
            font=("DejaVu Sans Mono", 10),
            wrap=tk.CHAR
        )
        self.text.pack(expand=True, fill="both")
        self.text.bind("<Key>", self.on_key)
        self.text.configure(state="disabled")

        # Iniciar el proceso cmd2 en un PTY
        self.start_cmd2_process()

    def start_cmd2_process(self):
        # Crear un pseudo-terminal
        pid, fd = pty.fork()
        if pid == 0:
            # Proceso hijo: ejecutar tu app cmd2
            os.execv("/usr/bin/bash", ["bash", "run"])
        else:
            # Proceso padre: leer desde el PTY
            self.pty_fd = fd
            self.read_thread = threading.Thread(target=self.read_pty_output, daemon=True)
            self.read_thread.start()

    def read_pty_output(self):
        while True:
            try:
                if select.select([self.pty_fd], [], [], 0.1)[0]:
                    data = os.read(self.pty_fd, 1024)
                    if not data:
                        break
                    # Programación segura en Tkinter desde otro hilo
                    self.root.after(0, self.append_text, data.decode("utf-8", errors="replace"))
            except OSError:
                break

    def append_text(self, text):
        self.text.configure(state="normal")
        self.text.insert(tk.END, text)
        self.text.see(tk.END)
        self.text.configure(state="disabled")

    def on_key(self, event):
        if event.keysym in ("Control_L", "Control_R", "Alt_L", "Alt_R", "Shift_L", "Shift_R"):
            return

        if event.keysym == "Return":
            self.send_to_process("\n")
            return "break"
        elif event.keysym == "BackSpace":
            self.send_to_process("\x08")  # Backspace ASCII
            return "break"
        elif len(event.char) == 1:
            self.send_to_process(event.char)
            return "break"

        # Ignorar otras teclas (flechas, etc.) por ahora
        return "break"

    def send_to_process(self, data):
        try:
            os.write(self.pty_fd, data.encode("utf-8"))
        except OSError:
            pass  # El proceso ya terminó

if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalEmulator(root)
    root.mainloop()