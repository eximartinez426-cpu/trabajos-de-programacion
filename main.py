# main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config

# Esto es opcional, pero ayuda a que Kivy no se inicie en modo pantalla completa 
# y puedas ver mejor la ventana de prueba en tu Chromebook.
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '300')


# 1. Definir el Widget Raíz (la interfaz)
class ContenedorPrincipal(BoxLayout):
    # Aquí puedes añadir código Python si lo necesitas, pero por ahora se carga el diseño de holamundo.kv
    pass

# 2. Definir la Aplicación
class HolaMundoApp(App):
    # Kivy buscará el archivo holamundo.kv
    def build(self):
        return ContenedorPrincipal()

if __name__ == '__main__':
    HolaMundoApp().run()