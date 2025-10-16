#importaciones necesarias de Kivy (framework)
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty, StringProperty
from kivy.metrics import dp # Para usar unidades de densidad de píxeles (mejor para el diseño)
from kivy.core.window import Window
from kivy.uix.popup import Popup

# clase tareaapp 

class TareaApp(App):
    # Lista observable que almacenará todas las tareas. Kivy la actualiza automáticamente.
    tareas = ListProperty([]) 

    def build(self):
        # Configuramos un administrador de pantallas
        sm = ScreenManager()
        
        # Pantalla Principal
        sm.add_widget(PrincipalScreen(name='principal'))
        
        # Pantalla para Agregar Tareas
        sm.add_widget(AgregarTareaScreen(name='agregar'))
        
        #Pantalla para Ver y Eliminar Tareas
        sm.add_widget(VerTareasScreen(name='ver'))
        
        return sm #sm es una instancia del administrador de pantillas creadas

# Pantalla Principal (PrincipalScreen) es la pantalla de inicio

class PrincipalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(
            orientation='vertical', padding=dp(40), spacing=dp(20)
        )
        
        # Título
        layout.add_widget(Label(
            text='[b]ADMINISTRADOR DE TAREAS[/b]', markup=True, font_size='30sp',size_hint_y=None, height=dp(60)
        ))

        # Botón: Agregar Tarea
        btn_agregar = Button(
            text='Agregar Tarea', font_size='20sp', background_color=(0.2, 0.6, 0.8, 1) # Azul claro
        )
        btn_agregar.bind(on_release=lambda x: self.cambiar_pantalla('agregar'))
        layout.add_widget(btn_agregar)

        # Botón: Ver Tareas
        btn_ver = Button(
            text='Ver Tareas', font_size='20sp', background_color=(0.8, 0.4, 0.2, 1) # Naranja
        )
        btn_ver.bind(on_release=lambda x: self.cambiar_pantalla('ver'))
        layout.add_widget(btn_ver)

        self.add_widget(layout)
    
    def cambiar_pantalla(self, nombre_pantalla):
        self.manager.current = nombre_pantalla

# 3. Pantalla para Agregar Tarea (AgregarTareaScreen) esta es la parte para escribir y guardar taras

class AgregarTareaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(
            orientation='vertical', padding=dp(30), spacing=dp(20)
        )
        
        layout.add_widget(Label(
            text='[b]AGREGAR NUEVA TAREA[/b]', markup=True, font_size='25sp', size_hint_y=None, height=dp(50)
        ))

        # Campo de Texto
        self.input_tarea = TextInput(
            hint_text='Escribe aquí la descripción de la tarea...',
            multiline=False, font_size='18sp', size_hint_y=None, height=dp(40)
        )
        layout.add_widget(self.input_tarea)
        
        # Botón "Agregar"
        btn_agregar = Button(
            text='AGREGAR', font_size='20sp', size_hint_y=None,
            height=dp(50), background_color=(0.4, 0.8, 0.4, 1) # Verde
        )
        btn_agregar.bind(on_release=self.agregar_tarea)
        layout.add_widget(btn_agregar)

        # Botón para Volver a la pantalla principal
        btn_volver = Button(
            text='Volver al Menú', font_size='15sp',
            size_hint_y=None, height=dp(40), background_color=(0.6, 0.6, 0.6, 1) # Gris
        )
        btn_volver.bind(on_release=lambda x: self.cambiar_pantalla('principal'))
        layout.add_widget(btn_volver)

        self.add_widget(layout)

    def agregar_tarea(self, instance):
        tarea = self.input_tarea.text.strip()
        
        if tarea:
            # Agrega la tarea a la lista de tareas de la aplicación
            App.get_running_app().tareas.append(tarea)
            self.mostrar_popup('Tarea Agregada', f'"{tarea}" se ha guardado con éxito.')
            self.input_tarea.text = '' # Limpia el campo
            self.cambiar_pantalla('principal') # Vuelve al menú principal
        else:
            self.mostrar_popup('Advertencia', 'Por favor, escribe una descripción para la tarea.')

    def cambiar_pantalla(self, nombre_pantalla):
        self.manager.current = nombre_pantalla

    def mostrar_popup(self, titulo, mensaje):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=mensaje, font_size='18sp'))
        btn_cerrar = Button(text='Cerrar', size_hint_y=None, height=dp(40))
        content.add_widget(btn_cerrar)
        
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        btn_cerrar.bind(on_release=popup.dismiss)
        popup.open()

# representa una tarea individual en la lista de tareas

class TareaItem(BoxLayout):
    # La tarea que se muestra en esta instancia
    tarea_texto = StringProperty('')
    
    def __init__(self, tarea, **kwargs):
        super().__init__(**kwargs)
        self.tarea_texto = tarea
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(5)
        self.spacing = dp(10)
        
        # Etiqueta de la Tarea
        self.label = Label(
            text=self.tarea_texto, font_size='16sp', size_hint_x=0.8, halign='left', valign='middle',
            # ELIMINADO: text_size=(self.width * 0.8, self.height)
        )
        self.add_widget(self.label)
        
        # Botón de Selección para Eliminar
        self.btn_select = Button(
            text='Seleccionar', size_hint_x=0.2, background_color=(0.9, 0.9, 0.9, 1)
        )
        self.btn_select.bind(on_release=self.seleccionar_para_eliminar)
        self.add_widget(self.btn_select)
        
        # AÑADIDO: Binding para asegurar que el texto se ajusta al tamaño
        self.bind(size=self.actualizar_text_size)

    def actualizar_text_size(self, instance, value):
        # La propiedad text_size debe ser establecida con el ancho real del widget
        # Usamos el 80% del ancho total del TareaItem (que es el size_hint_x del Label)
        ancho_label = self.width * 0.8 
        self.label.text_size = (ancho_label - dp(10), self.height) # Restamos un poco de padding

    def seleccionar_para_eliminar(self, instance):
        # Envía la tarea a la pantalla contenedora para marcarla
        self.parent.parent.parent.parent.marcar_tarea_seleccionada(self.tarea_texto, self.btn_select)

# Pantalla para Ver/Eliminar Tareas (VerTareasScreen)

class VerTareasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        layout.add_widget(Label(
            text='[b]TAREAS PENDIENTES[/b]', markup=True, font_size='25sp', size_hint_y=None, height=dp(50)
        ))

        # Contenedor para la lista de tareas
        self.lista_tareas_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        self.lista_tareas_layout.bind(minimum_height=self.lista_tareas_layout.setter('height'))

        # ScrollView para la lista
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.lista_tareas_layout)
        layout.add_widget(scroll)

        # Botón "Eliminar Tarea"
        self.btn_eliminar = Button(
            text='Eliminar Tarea Seleccionada', font_size='20sp', size_hint_y=None, height=dp(50),
            background_color=(1, 0.3, 0.3, 1), # Rojo
            disabled=True # Deshabilitado por defecto
        )
        self.btn_eliminar.bind(on_release=self.eliminar_tarea)
        layout.add_widget(self.btn_eliminar)
        
        # Botón para Volver
        btn_volver = Button(
            text='Volver al Menú', font_size='15sp', size_hint_y=None,
            height=dp(40), background_color=(0.6, 0.6, 0.6, 1) # Gris
        )
        btn_volver.bind(on_release=lambda x: self.cambiar_pantalla('principal'))
        layout.add_widget(btn_volver)#btn para volver al menu principal juajus 
        
        self.add_widget(layout)
        
        # Variables de estado
        self.tarea_a_eliminar = None #nada o ningun valor 
        self.btn_seleccionado = None
        
        # Vinculamos la función actualizar_lista a los cambios en App.tareas
        App.get_running_app().bind(tareas=self.actualizar_lista_kivy)

    def on_enter(self):
        # Se llama cada vez que se entra a esta pantalla
        self.actualizar_lista_kivy(None, App.get_running_app().tareas)
        
    def actualizar_lista_kivy(self, instance, tareas_list):
        # Limpia la lista visual
        self.lista_tareas_layout.clear_widgets()
        self.tarea_a_eliminar = None
        self.btn_eliminar.disabled = True
        
        # Rellena la lista con los elementos TareaItem
        for tarea in tareas_list:
            item = TareaItem(tarea=tarea)
            self.lista_tareas_layout.add_widget(item)
            
        # Si no hay tareas, agregamos un mensaje
        if not tareas_list:
            self.lista_tareas_layout.add_widget(Label(text='No hay tareas pendientes.', size_hint_y=None, height=dp(50)))

    def marcar_tarea_seleccionada(self, tarea_texto, boton):
        if self.btn_seleccionado:
            # Desmarcar el botón previamente seleccionado
            self.btn_seleccionado.background_color = (0.9, 0.9, 0.9, 1)
            self.btn_seleccionado.text = 'Seleccionar'

        if self.tarea_a_eliminar == tarea_texto:
            # Si hace click en la misma tarea, deselecciona
            self.tarea_a_eliminar = None
            self.btn_eliminar.disabled = True
            self.btn_seleccionado = None
        else:
            # Selecciona la nueva tarea
            self.tarea_a_eliminar = tarea_texto
            self.btn_seleccionado = boton
            self.btn_eliminar.disabled = False
            self.btn_seleccionado.background_color = (0.2, 0.8, 0.2, 1) # Verde
            self.btn_seleccionado.text = 'Seleccionada'


    def eliminar_tarea(self, instance):
        if self.tarea_a_eliminar:
            app = App.get_running_app()
            
            # Buscamos y eliminamos la tarea de la lista observable
            app.tareas.remove(self.tarea_a_eliminar)
            
            # Limpiamos las variables de selección
            self.tarea_a_eliminar = None
            self.btn_seleccionado = None
            self.btn_eliminar.disabled = True
            
            self.mostrar_popup('Eliminado', f'Tarea eliminada con éxito.')
            
            # La función actualizar_lista_kivy se llama automáticamente gracias al bind
            # Pero la llamamos para forzar el estado visual
            self.actualizar_lista_kivy(None, app.tareas)
        else:
            self.mostrar_popup('Atención', 'Por favor, selecciona una tarea para eliminar.')

    def cambiar_pantalla(self, nombre_pantalla):
        self.manager.current = nombre_pantalla

    def mostrar_popup(self, titulo, mensaje):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=mensaje, font_size='18sp'))
        btn_cerrar = Button(text='Cerrar', size_hint_y=None, height=dp(40))
        content.add_widget(btn_cerrar)
        
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        btn_cerrar.bind(on_release=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    Window.size = (400, 600) 
    TareaApp().run()
