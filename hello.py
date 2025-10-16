from kivy.app import App
from kivy.uix.label import Label
# Importamos la clase Color para usar colores RGB (opcional, pero útil)
from kivy.core.window import Window 

class MyApp(App):
    def build(self):
        # 1. Creamos una etiqueta de texto (Label)
        # 2. Establecemos el tamaño de la fuente.
        # 3. Establecemos el color del texto a blanco (R=1, G=1, B=1, A=1)
        return Label(
            text='¡Mi Primera App Kivy Funciona!', 
            font_size='50sp',
            color=(1, 1, 1, 1) # Blanco puro
        )

if __name__ == '__main__':
    MyApp().run()
