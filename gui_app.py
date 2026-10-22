"""
Interfaz Gráfica del Simulador de Granja
Reemplaza la interfaz de consola con una aplicación GUI moderna
"""

from tkinter import *
from tkinter import ttk, messagebox
from collections import defaultdict

from granja import Granja
from personaje import Personaje
from tienda import Tienda
from encargado import SistemaAutomatizacion, Encargado
from guardado import SistemaGuardado, restaurar_desde_datos
import constants as cfg


class SimuladorGranjaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏭 Simulador de Granja - Gestión de Recursos")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        self.colors = {
            'primary': '#FF6B6B',
            'secondary': '#4ECDC4',
            'accent': '#45B7D1',
            'warning': '#FFBE0B',
            'success': '#96CEB4',
            'info': '#FECA57',
            'dark': '#2C3E50',
            'light': '#ECF0F1',
            'error': '#E74C3C',
            'text_secondary': '#7F8C8D',
        }

        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass

        self.selected_character = None
        self.selected_order = None
        self.selected_worker = None
        self.selected_interaction_char = None

        self.inicializar_juego()
        self.create_widgets()
        self.refresh_all()

    # ── Inicialización del juego ──────────────────────────────────────────

    def inicializar_juego(self):
        self.sistema_guardado = SistemaGuardado()
        self.resultado_carga = None
        self.mostrar_dialogo_carga()
        if self.resultado_carga is None or self.resultado_carga[0] != 'cargar':
            self.crear_nueva_partida()

    def mostrar_dialogo_carga(self):
        dialogo = Toplevel(self.root)
        dialogo.title("Cargar Partida")
        dialogo.geometry("400x200")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()
        dialogo.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))

        Label(dialogo, text="¿Quieres cargar una partida guardada?", font=('Arial', 12)).pack(pady=20)

        button_frame = Frame(dialogo)
        button_frame.pack(pady=10)

        Button(button_frame, text="Cargar Partida",
               command=lambda: self.cargar_partida_dialogo(dialogo),
               bg=self.colors['secondary'], fg='white',
               font=('Arial', 10, 'bold'), padx=20).pack(side=LEFT, padx=10)

        Button(button_frame, text="Nueva Partida",
               command=lambda: self.nueva_partida_dialogo(dialogo),
               bg=self.colors['primary'], fg='white',
               font=('Arial', 10, 'bold'), padx=20).pack(side=LEFT, padx=10)

        self.root.wait_window(dialogo)

    def cargar_partida_dialogo(self, dialogo):
        partidas = self.sistema_guardado.listar_partidas()
        if not partidas:
            messagebox.showinfo("Info", "No hay partidas guardadas")
            return

        select_dialog = Toplevel(dialogo)
        select_dialog.title("Seleccionar Partida")
        select_dialog.geometry("300x400")
        select_dialog.transient(dialogo)
        select_dialog.grab_set()

        Label(select_dialog, text="Selecciona una partida:", font=('Arial', 10)).pack(pady=10)

        listbox = Listbox(select_dialog, font=('Arial', 9))
        listbox.pack(fill=BOTH, expand=True, padx=20, pady=10)

        for partida in partidas:
            listbox.insert(END, partida)

        def cargar_seleccionada():
            seleccion = listbox.curselection()
            if seleccion:
                nombre_partida = listbox.get(seleccion[0])
                dialogo.destroy()
                select_dialog.destroy()
                self.cargar_partida(nombre_partida)

        Button(select_dialog, text="Cargar", command=cargar_seleccionada,
               bg=self.colors['success'], fg='white',
               font=('Arial', 10, 'bold')).pack(pady=10)

        self.root.wait_window(select_dialog)

    def cargar_partida(self, nombre_partida):
        datos, mensaje = self.sistema_guardado.cargar_partida(nombre_partida)
        if datos:
            self.granja, self.tienda, self.sistema_auto = restaurar_desde_datos(datos)
            self.resultado_carga = ('cargar', nombre_partida)
            messagebox.showinfo("Éxito", "✅ Partida cargada correctamente")
        else:
            messagebox.showerror("Error", mensaje)
            self.crear_nueva_partida()

    def nueva_partida_dialogo(self, dialogo):
        dialogo.destroy()
        self.crear_nueva_partida()

    def crear_nueva_partida(self):
        self.granja = Granja()
        personajes_iniciales = [
            Personaje("Amber", "Outrider", 18),
            Personaje("Barbara", "Diaconisa", 16),
            Personaje("Fischl", "Investigadora", 16),
        ]
        for p in personajes_iniciales:
            self.granja.agregar_personaje(p)
        self.tienda = Tienda(self.granja)
        self.sistema_auto = SistemaAutomatizacion(self.granja)
        self.resultado_carga = ('nueva', None)

    # ── Construcción de la interfaz ───────────────────────────────────────

    def create_widgets(self):
        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=BOTH, expand=True)

        self.create_character_tab()
        self.create_storage_tab()
        self.create_store_tab()
        self.create_automation_tab()
        self.create_interactions_tab()
        self.create_controls_tab()
        self.create_status_bar()

    def create_status_bar(self):
        self.status_bar = Frame(self.root, relief=SUNKEN, bd=1)
        self.status_bar.pack(fill=X, side=BOTTOM)
        self.status_label = Label(self.status_bar, text="Listo", anchor=W)
        self.status_label.pack(side=LEFT, padx=5)
        self.status_time_label = Label(self.status_bar, text="", anchor=E)
        self.status_time_label.pack(side=RIGHT, padx=5)

    # ── Pestaña: Personajes ───────────────────────────────────────────────

    def create_character_tab(self):
        char_frame = Frame(self.notebook)
        self.notebook.add(char_frame, text="👥 Personajes")

        left_panel = Frame(char_frame)
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 5), pady=5)

        Label(left_panel, text="Personajes", font=('Arial', 12, 'bold')).pack(pady=(0, 10))

        self.character_listbox = Listbox(left_panel, width=20, height=15, font=('Arial', 10))
        self.character_listbox.pack(fill=Y, expand=True)
        self.character_listbox.bind('<<ListboxSelect>>', self.on_character_select)

        char_buttons = Frame(left_panel)
        char_buttons.pack(fill=X, pady=10)
        Button(char_buttons, text="Actualizar Lista", command=self.refresh_character_list,
               bg=self.colors['info'], fg='white', font=('Arial', 9)).pack(fill=X, pady=2)

        right_panel = Frame(char_frame)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0), pady=5)

        self.char_details_notebook = ttk.Notebook(right_panel)
        self.char_details_notebook.pack(fill=BOTH, expand=True)

        self.create_character_status_tab()
        self.create_character_resources_tab()
        self.create_character_actions_tab()

    def create_character_status_tab(self):
        status_frame = Frame(self.char_details_notebook)
        self.char_details_notebook.add(status_frame, text="📊 Estado")

        stats_frame = LabelFrame(status_frame, text="Estadísticas", padx=10, pady=10)
        stats_frame.pack(fill=X, pady=10)

        for i, (label_text, var_attr, bar_attr, lbl_attr) in enumerate([
            ("Hambre:", "hunger_var", "hunger_bar", "hunger_label"),
            ("Sed:", "thirst_var", "thirst_bar", "thirst_label"),
            ("Higiene:", "hygiene_var", "hygiene_bar", "hygiene_label"),
            ("Energía:", "energy_var", "energy_bar", "energy_label"),
        ]):
            Label(stats_frame, text=label_text).grid(row=i, column=0, sticky=W, pady=2)
            setattr(self, var_attr, DoubleVar())
            setattr(self, bar_attr, ttk.Progressbar(stats_frame, variable=getattr(self, var_attr), maximum=100, length=200))
            getattr(self, bar_attr).grid(row=i, column=1, padx=5, pady=2)
            setattr(self, lbl_attr, Label(stats_frame, text="0%"))
            getattr(self, lbl_attr).grid(row=i, column=2, padx=5, pady=2)

        info_frame = LabelFrame(status_frame, text="Información Detallada", padx=10, pady=10)
        info_frame.pack(fill=BOTH, expand=True, pady=10)
        self.char_info_text = Text(info_frame, height=8, width=40, font=('Courier', 9))
        self.char_info_text.pack(fill=BOTH, expand=True)
        self.char_info_text.config(state=DISABLED)

    def create_character_resources_tab(self):
        resources_frame = Frame(self.char_details_notebook)
        self.char_details_notebook.add(resources_frame, text="📦 Recursos")

        Label(resources_frame, text="Recursos Disponibles para Recolectar:",
              font=('Arial', 10, 'bold')).pack(anchor=W, pady=(0, 5))

        self.char_resources_text = Text(resources_frame, height=15, width=40, font=('Courier', 9))
        self.char_resources_text.pack(fill=BOTH, expand=True, padx=10, pady=5)
        self.char_resources_text.config(state=DISABLED)

        Button(resources_frame, text="Recolectar Todos los Recursos",
               command=self.collect_character_resources,
               bg=self.colors['success'], fg='white',
               font=('Arial', 10, 'bold')).pack(pady=10)

    def create_character_actions_tab(self):
        actions_frame = Frame(self.char_details_notebook)
        self.char_details_notebook.add(actions_frame, text="⚡ Acciones")

        basic_actions = LabelFrame(actions_frame, text="Acciones Básicas", padx=10, pady=10)
        basic_actions.pack(fill=X, pady=5)

        Button(basic_actions, text="Alimentar", command=self.feed_character,
               bg=self.colors['warning'], fg='white', font=('Arial', 9)).pack(fill=X, pady=2)
        Button(basic_actions, text="Dar Agua", command=self.give_water_character,
               bg=self.colors['accent'], fg='white', font=('Arial', 9)).pack(fill=X, pady=2)
        Button(basic_actions, text="Limpiar", command=self.clean_character,
               bg=self.colors['info'], fg='white', font=('Arial', 9)).pack(fill=X, pady=2)

        self.special_actions_frame = LabelFrame(actions_frame, text="Interacciones Especiales",
                                                padx=10, pady=10)
        self.special_actions_frame.pack(fill=BOTH, expand=True, pady=5)

    # ── Pestaña: Almacén ──────────────────────────────────────────────────

    def create_storage_tab(self):
        storage_frame = Frame(self.notebook)
        self.notebook.add(storage_frame, text="📦 Almacén")

        control_frame = Frame(storage_frame)
        control_frame.pack(fill=X, pady=5)

        Button(control_frame, text="Actualizar Almacén", command=self.refresh_storage_display,
               bg=self.colors['info'], fg='white', font=('Arial', 9)).pack(side=LEFT, padx=5)
        Button(control_frame, text="Vista Detallada", command=self.show_detailed_storage,
               bg=self.colors['secondary'], fg='white', font=('Arial', 9)).pack(side=LEFT, padx=5)

        storage_container = Frame(storage_frame)
        storage_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        storage_scroll = Scrollbar(storage_container)
        storage_scroll.pack(side=RIGHT, fill=Y)

        self.storage_text = Text(storage_container, yscrollcommand=storage_scroll.set,
                                 font=('Courier', 10), wrap=WORD)
        self.storage_text.pack(fill=BOTH, expand=True)
        storage_scroll.config(command=self.storage_text.yview)

    # ── Pestaña: Tienda ───────────────────────────────────────────────────

    def create_store_tab(self):
        store_frame = Frame(self.notebook)
        self.notebook.add(store_frame, text="🏪 Tienda")

        info_frame = Frame(store_frame)
        info_frame.pack(fill=X, pady=5)

        Label(info_frame, text="Dinero:", font=('Arial', 10, 'bold')).pack(side=LEFT)
        self.store_money_label = Label(info_frame, text="$0", font=('Arial', 10, 'bold'),
                                       fg=self.colors['warning'])
        self.store_money_label.pack(side=LEFT, padx=10)

        Label(info_frame, text="Completados:", font=('Arial', 10, 'bold')).pack(side=LEFT, padx=(20, 0))
        self.store_completed_label = Label(info_frame, text="0", font=('Arial', 10, 'bold'),
                                           fg=self.colors['success'])
        self.store_completed_label.pack(side=LEFT, padx=5)

        orders_frame = LabelFrame(store_frame, text="Encargos Disponibles", padx=10, pady=10)
        orders_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        orders_container = Frame(orders_frame)
        orders_container.pack(fill=BOTH, expand=True)

        orders_scroll = Scrollbar(orders_container)
        orders_scroll.pack(side=RIGHT, fill=Y)

        self.orders_listbox = Listbox(orders_container, yscrollcommand=orders_scroll.set,
                                      font=('Courier', 9), selectmode=SINGLE)
        self.orders_listbox.pack(fill=BOTH, expand=True)
        orders_scroll.config(command=self.orders_listbox.yview)
        self.orders_listbox.bind('<<ListboxSelect>>', self.on_order_select)

        order_buttons = Frame(orders_frame)
        order_buttons.pack(fill=X, pady=5)

        Button(order_buttons, text="Actualizar Encargos", command=self.refresh_store_display,
               bg=self.colors['info'], fg='white', font=('Arial', 9)).pack(side=LEFT, padx=5)

        self.complete_order_button = Button(order_buttons, text="Completar Encargo Seleccionado",
                                            command=self.complete_selected_order,
                                            bg=self.colors['success'], fg='white',
                                            font=('Arial', 9, 'bold'))
        self.complete_order_button.pack(side=LEFT, padx=5)
        self.complete_order_button.config(state=DISABLED)

        order_info_frame = LabelFrame(store_frame, text="Información del Encargo", padx=10, pady=10)
        order_info_frame.pack(fill=X, padx=10, pady=5)

        self.order_info_text = Text(order_info_frame, height=6, width=60, font=('Courier', 9))
        self.order_info_text.pack(fill=X)
        self.order_info_text.config(state=DISABLED)

    # ── Pestaña: Automatización ───────────────────────────────────────────

    def create_automation_tab(self):
        auto_frame = Frame(self.notebook)
        self.notebook.add(auto_frame, text="🤖 Automatización")

        top_frame = Frame(auto_frame)
        top_frame.pack(fill=X, pady=5)

        Label(top_frame, text="Encargados/Máquinas:", font=('Arial', 10, 'bold')).pack(side=LEFT)

        Button(top_frame, text="Crear Nuevo Encargado", command=self.create_new_worker_dialog,
               bg=self.colors['primary'], fg='white', font=('Arial', 9, 'bold')).pack(side=LEFT, padx=10)
        Button(top_frame, text="Actualizar Lista", command=self.refresh_worker_list,
               bg=self.colors['info'], fg='white', font=('Arial', 9)).pack(side=LEFT, padx=5)

        workers_frame = LabelFrame(auto_frame, text="Encargados Activos", padx=10, pady=10)
        workers_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        workers_container = Frame(workers_frame)
        workers_container.pack(fill=BOTH, expand=True)

        workers_scroll = Scrollbar(workers_container)
        workers_scroll.pack(side=RIGHT, fill=Y)

        self.workers_listbox = Listbox(workers_container, yscrollcommand=workers_scroll.set,
                                       font=('Courier', 9), selectmode=SINGLE)
        self.workers_listbox.pack(fill=BOTH, expand=True)
        workers_scroll.config(command=self.workers_listbox.yview)
        self.workers_listbox.bind('<<ListboxSelect>>', self.on_worker_select)

        worker_details_frame = LabelFrame(auto_frame, text="Detalles del Encargado", padx=10, pady=10)
        worker_details_frame.pack(fill=X, padx=10, pady=5)

        self.worker_info_text = Text(worker_details_frame, height=6, width=60, font=('Courier', 9))
        self.worker_info_text.pack(fill=BOTH, expand=True)
        self.worker_info_text.config(state=DISABLED)

        worker_action_buttons = Frame(auto_frame)
        worker_action_buttons.pack(fill=X, padx=10, pady=5)
        self.toggle_worker_btn = Button(worker_action_buttons, text="Activar/Desactivar",
                                        command=self.toggle_worker, state=DISABLED,
                                        bg=self.colors['info'], fg='white', font=('Arial', 9))
        self.toggle_worker_btn.pack(side=LEFT, padx=5)
        self.clear_tasks_btn = Button(worker_action_buttons, text="Limpiar Tareas",
                                      command=self.clear_all_tasks, state=DISABLED,
                                      bg=self.colors['warning'], fg='white', font=('Arial', 9))
        self.clear_tasks_btn.pack(side=LEFT, padx=5)

        task_frame = LabelFrame(auto_frame, text="Programar Tarea", padx=10, pady=10)
        task_frame.pack(fill=X, padx=10, pady=5)

        Label(task_frame, text="Personaje:").grid(row=0, column=0, sticky=W, pady=2)
        self.task_character_var = StringVar()
        self.task_character_combo = ttk.Combobox(task_frame, textvariable=self.task_character_var,
                                                 state="readonly", width=15)
        self.task_character_combo.grid(row=0, column=1, padx=5, pady=2, sticky=W)

        Label(task_frame, text="Acción:").grid(row=0, column=2, sticky=W, padx=(10, 0), pady=2)
        self.task_action_var = StringVar()
        self.task_action_combo = ttk.Combobox(task_frame, textvariable=self.task_action_var,
                                              values=["recolectar", "alimentar", "dar_agua", "limpiar"],
                                              state="readonly", width=12)
        self.task_action_combo.grid(row=0, column=3, padx=5, pady=2, sticky=W)

        Label(task_frame, text="Cantidad (g/ml):").grid(row=1, column=0, sticky=W, pady=2)
        self.task_cantidad_entry = Entry(task_frame, width=10)
        self.task_cantidad_entry.grid(row=1, column=1, padx=5, pady=2, sticky=W)
        self.task_cantidad_entry.insert(0, "400")

        Button(task_frame, text="Programar Tarea", command=self.schedule_task,
               bg=self.colors['warning'], fg='white', font=('Arial', 9, 'bold')).grid(
               row=2, column=0, columnspan=4, pady=10)

        scheduled_frame = LabelFrame(auto_frame, text="Tareas Programadas", padx=10, pady=10)
        scheduled_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        scheduled_container = Frame(scheduled_frame)
        scheduled_container.pack(fill=BOTH, expand=True)

        scheduled_scroll = Scrollbar(scheduled_container)
        scheduled_scroll.pack(side=RIGHT, fill=Y)

        self.scheduled_tasks_text = Text(scheduled_container, yscrollcommand=scheduled_scroll.set,
                                         font=('Courier', 9), height=8)
        self.scheduled_tasks_text.pack(fill=BOTH, expand=True)
        scheduled_scroll.config(command=self.scheduled_tasks_text.yview)

        task_buttons = Frame(auto_frame)
        task_buttons.pack(fill=X, pady=5)

        Button(task_buttons, text="Ejecutar Automatización Ahora", command=self.execute_automation_now,
               bg=self.colors['primary'], fg='white', font=('Arial', 9, 'bold')).pack(side=LEFT, padx=5)

    # ── Pestaña: Interacciones ────────────────────────────────────────────

    def create_interactions_tab(self):
        interactions_frame = Frame(self.notebook)
        self.notebook.add(interactions_frame, text="🔞 Interacciones")

        Label(interactions_frame,
              text="Interacciones especiales que generan recursos adicionales\npero reducen la higiene del personaje",
              font=('Arial', 10, 'italic'), fg=self.colors['dark']).pack(pady=10)

        char_select_frame = LabelFrame(interactions_frame, text="Seleccionar Personaje", padx=10, pady=10)
        char_select_frame.pack(fill=X, padx=10, pady=5)

        Label(char_select_frame, text="Personaje:").pack(side=LEFT)
        self.interaction_char_var = StringVar()
        self.interaction_char_combo = ttk.Combobox(char_select_frame,
                                                   textvariable=self.interaction_char_var,
                                                   state="readonly", width=20)
        self.interaction_char_combo.pack(side=LEFT, padx=5)
        self.interaction_char_combo.bind('<<ComboboxSelected>>', self.on_interaction_char_select)

        interactions_buttons = Frame(interactions_frame)
        interactions_buttons.pack(fill=X, padx=10, pady=10)

        for text, cmd in [
            ("Lamer", self.interaction_lamer),
            ("Tocar/Acariciar", self.interaction_tocar),
            ("Penetrar", self.interaction_penetrar),
            ("Insertar Objeto", self.interaction_insertar_objeto),
            ("Poner Boca en", self.interaction_boca),
        ]:
            Button(interactions_buttons, text=text, command=cmd,
                   bg=self.colors['warning'], fg='white', font=('Arial', 9)).pack(side=LEFT, padx=5)

        results_frame = LabelFrame(interactions_frame, text="Resultados de Interacciones", padx=10, pady=10)
        results_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        self.interaction_results_text = Text(results_frame, height=10, width=60, font=('Courier', 9))
        self.interaction_results_text.pack(fill=BOTH, expand=True)
        self.interaction_results_text.config(state=DISABLED)

    # ── Pestaña: Controles ────────────────────────────────────────────────

    def create_controls_tab(self):
        controls_frame = Frame(self.notebook)
        self.notebook.add(controls_frame, text="🎮 Controles")

        game_info_frame = LabelFrame(controls_frame, text="Información del Juego", padx=10, pady=10)
        game_info_frame.pack(fill=X, padx=10, pady=5)

        self.game_time_label = Label(game_info_frame, text="Hora: 08:00 AM", font=('Arial', 10, 'bold'))
        self.game_time_label.pack(anchor=W)

        time_controls = LabelFrame(controls_frame, text="Controles de Tiempo", padx=10, pady=10)
        time_controls.pack(fill=X, padx=10, pady=5)

        Button(time_controls, text="Avanzar 1 Hora", command=self.advance_one_hour,
               bg=self.colors['accent'], fg='white', font=('Arial', 9, 'bold')).pack(side=LEFT, padx=5)
        Button(time_controls, text="Avanzar 3 Horas", command=self.advance_three_hours,
               bg=self.colors['accent'], fg='white', font=('Arial', 9, 'bold')).pack(side=LEFT, padx=5)
        Button(time_controls, text="Avanzar 6 Horas", command=self.advance_six_hours,
               bg=self.colors['accent'], fg='white', font=('Arial', 9, 'bold')).pack(side=LEFT, padx=5)

        save_frame = LabelFrame(controls_frame, text="Guardado y Carga", padx=10, pady=10)
        save_frame.pack(fill=X, padx=10, pady=5)

        Button(save_frame, text="Guardar Partida", command=self.save_game_dialog,
               bg=self.colors['success'], fg='white', font=('Arial', 9, 'bold')).pack(side=LEFT, padx=5)
        Button(save_frame, text="Cargar Partida", command=self.load_game_dialog,
               bg=self.colors['primary'], fg='white', font=('Arial', 9, 'bold')).pack(side=LEFT, padx=5)
        Button(save_frame, text="Ver Partidas Guardadas", command=self.list_saved_games,
               bg=self.colors['info'], fg='white', font=('Arial', 9)).pack(side=LEFT, padx=5)

    # ── Actualización general ─────────────────────────────────────────────

    def refresh_all(self):
        self.refresh_character_list()
        self.refresh_storage_display()
        self.refresh_store_display()
        self.refresh_worker_list()
        self.update_time_display()
        self.populate_character_combos()

    def populate_character_combos(self):
        nombres = [p.nombre for p in self.granja.personajes]
        self.task_character_combo['values'] = nombres
        self.interaction_char_combo['values'] = nombres

    # ── Eventos: Personajes ───────────────────────────────────────────────

    def refresh_character_list(self):
        self.character_listbox.delete(0, END)
        for personaje in self.granja.personajes:
            self.character_listbox.insert(END, personaje.nombre)

    def on_character_select(self, event):
        selection = self.character_listbox.curselection()
        if selection:
            nombre = self.character_listbox.get(selection[0])
            self.selected_character = self.granja.buscar_personaje(nombre)
            self.update_character_display()

    def update_character_display(self):
        if not self.selected_character:
            return
        p = self.selected_character

        self.hunger_var.set(p.hambre)
        self.hunger_label.config(text=f"{p.hambre:.1f}%")
        self.thirst_var.set(p.sed)
        self.thirst_label.config(text=f"{p.sed:.1f}%")
        self.hygiene_var.set(p.higiene)
        self.hygiene_label.config(text=f"{p.higiene:.1f}%")
        self.energy_var.set(p.energia)
        self.energy_label.config(text=f"{p.energia:.1f}%")

        self.char_info_text.config(state=NORMAL)
        self.char_info_text.delete(1.0, END)
        self.char_info_text.insert(END, f"Nombre: {p.nombre}\n")
        self.char_info_text.insert(END, f"Tipo: {p.tipo}\n")
        self.char_info_text.insert(END, f"Edad: {p.edad} años\n")
        self.char_info_text.insert(END, f"Comida consumida: {p.comida_consumida}g\n")
        self.char_info_text.insert(END, f"Agua consumida: {p.agua_consumida}ml\n")
        self.char_info_text.config(state=DISABLED)

        self.char_resources_text.config(state=NORMAL)
        self.char_resources_text.delete(1.0, END)
        total = 0
        for recurso, cantidad in p.recursos_disponibles.items():
            if cantidad > 0:
                unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
                self.char_resources_text.insert(END, f"{recurso.replace('_', ' ').title()}: {cantidad:.1f}{unidad}\n")
                total += cantidad
        self.char_resources_text.insert(END, f"\nTotal: {total:.1f} unidades")
        self.char_resources_text.config(state=DISABLED)

    def feed_character(self):
        if not self.selected_character:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return

        dialogo = Toplevel(self.root)
        dialogo.title("Alimentar Personaje")
        dialogo.geometry("300x150")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text=f"Alimentar a {self.selected_character.nombre}").pack(pady=10)
        Label(dialogo, text="Cantidad de comida (g):").pack()
        cantidad_entry = Entry(dialogo, width=10)
        cantidad_entry.pack(pady=5)
        cantidad_entry.insert(0, "400")

        def confirmar():
            try:
                cantidad = int(cantidad_entry.get())
                if cantidad <= 0:
                    raise ValueError
                resultado = self.granja.alimentar_personaje(self.selected_character.nombre, cantidad)
                messagebox.showinfo("Resultado", resultado)
                self.update_character_display()
                dialogo.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingresa una cantidad válida")

        Button(dialogo, text="Alimentar", command=confirmar,
               bg=self.colors['success'], fg='white').pack(pady=10)
        self.root.wait_window(dialogo)

    def give_water_character(self):
        if not self.selected_character:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return

        dialogo = Toplevel(self.root)
        dialogo.title("Dar Agua a Personaje")
        dialogo.geometry("300x150")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text=f"Dar agua a {self.selected_character.nombre}").pack(pady=10)
        Label(dialogo, text="Cantidad de agua (ml):").pack()
        cantidad_entry = Entry(dialogo, width=10)
        cantidad_entry.pack(pady=5)
        cantidad_entry.insert(0, "300")

        def confirmar():
            try:
                cantidad = int(cantidad_entry.get())
                if cantidad <= 0:
                    raise ValueError
                resultado = self.granja.dar_agua_personaje(self.selected_character.nombre, cantidad)
                messagebox.showinfo("Resultado", resultado)
                self.update_character_display()
                dialogo.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingresa una cantidad válida")

        Button(dialogo, text="Dar Agua", command=confirmar,
               bg=self.colors['success'], fg='white').pack(pady=10)
        self.root.wait_window(dialogo)

    def clean_character(self):
        if not self.selected_character:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return
        resultado = self.granja.limpiar_personaje(self.selected_character.nombre)
        messagebox.showinfo("Resultado", resultado)
        self.update_character_display()

    def collect_character_resources(self):
        if not self.selected_character:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return
        resultado = self.granja.recolectar_recursos_personaje(self.selected_character.nombre)
        messagebox.showinfo("Resultado", resultado)
        self.update_character_display()
        self.refresh_storage_display()

    # ── Eventos: Almacén ──────────────────────────────────────────────────

    def refresh_storage_display(self):
        self.storage_text.config(state=NORMAL)
        self.storage_text.delete(1.0, END)

        if not self.granja.almacen:
            self.storage_text.insert(END, "El almacén está vacío\n")
        else:
            recursos_por_tipo = defaultdict(list)
            for (recurso, propietario), cantidad in self.granja.almacen.items():
                if cantidad > 0:
                    recursos_por_tipo[recurso].append((propietario, cantidad))

            for recurso in sorted(recursos_por_tipo.keys()):
                unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
                self.storage_text.insert(END, f"\n{recurso.replace('_', ' ').title()}:\n")
                total = 0
                for propietario, cantidad in recursos_por_tipo[recurso]:
                    self.storage_text.insert(END, f"  • De {propietario}: {cantidad:.1f}{unidad}\n")
                    total += cantidad
                self.storage_text.insert(END, f"  ➡️ Total: {total:.1f}{unidad}\n")

        self.storage_text.config(state=DISABLED)

    def show_detailed_storage(self):
        dialogo = Toplevel(self.root)
        dialogo.title("Almacén Detallado")
        dialogo.geometry("600x400")
        dialogo.transient(self.root)

        main_frame = Frame(dialogo)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tree_frame = Frame(main_frame)
        tree_frame.pack(fill=BOTH, expand=True)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        detailed_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
        detailed_tree.pack(fill=BOTH, expand=True)
        tree_scroll.config(command=detailed_tree.yview)

        detailed_tree["columns"] = ("propietario", "recurso", "cantidad", "unidad")
        detailed_tree.column("#0", width=0, stretch=NO)
        detailed_tree.column("propietario", width=150)
        detailed_tree.column("recurso", width=150)
        detailed_tree.column("cantidad", width=100)
        detailed_tree.column("unidad", width=80)

        detailed_tree.heading("propietario", text="Propietario")
        detailed_tree.heading("recurso", text="Recurso")
        detailed_tree.heading("cantidad", text="Cantidad")
        detailed_tree.heading("unidad", text="Unidad")

        for (recurso, propietario), cantidad in self.granja.almacen.items():
            if cantidad > 0:
                unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
                detailed_tree.insert("", "end", values=(propietario, recurso.replace('_', ' ').title(), f"{cantidad:.1f}", unidad))

        Button(main_frame, text="Cerrar", command=dialogo.destroy,
               bg=self.colors['warning'], fg='white').pack(pady=10)

    # ── Eventos: Tienda ───────────────────────────────────────────────────

    def refresh_store_display(self):
        self.orders_listbox.delete(0, END)
        for encargo in self.tienda.encargos_disponibles:
            recursos_str = []
            for (recurso, propietario), cantidad in encargo.recursos_necesarios.items():
                prop_str = f" de {propietario}" if propietario else ""
                unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
                recursos_str.append(f"{cantidad}{unidad} {recurso.replace('_', ' ')}{prop_str}")
            texto = f"#{encargo.id} | {' | '.join(recursos_str)} | ${encargo.pago} | {encargo.cliente}"
            self.orders_listbox.insert(END, texto)

        self.store_money_label.config(text=f"${self.tienda.dinero}")
        self.store_completed_label.config(text=str(self.tienda.encargos_completados))

    def on_order_select(self, event):
        selection = self.orders_listbox.curselection()
        if selection:
            texto = self.orders_listbox.get(selection[0])
            try:
                encargo_id = int(texto.split("|")[0].replace("#", "").strip())
            except ValueError:
                return
            self.selected_order = self.tienda.buscar_encargo_por_id(encargo_id)
            self.update_order_details()

    def update_order_details(self):
        if not self.selected_order:
            return
        encargo = self.selected_order

        self.order_info_text.config(state=NORMAL)
        self.order_info_text.delete(1.0, END)
        self.order_info_text.insert(END, f"ID: {encargo.id}\n")
        self.order_info_text.insert(END, f"Cliente: {encargo.cliente}\n")
        self.order_info_text.insert(END, f"Pago: ${encargo.pago}\n")
        self.order_info_text.insert(END, "Recursos necesarios:\n")
        for (recurso, propietario), cantidad in encargo.recursos_necesarios.items():
            prop_str = f" (de {propietario})" if propietario else ""
            unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
            self.order_info_text.insert(END, f"  • {cantidad}{unidad} {recurso.replace('_', ' ')}{prop_str}\n")
        self.order_info_text.config(state=DISABLED)

        self.check_order_completion()

    def check_order_completion(self):
        if not self.selected_order:
            self.complete_order_button.config(state=DISABLED)
            return
        encargo = self.selected_order
        puede = True
        for (recurso, propietario), cantidad_necesaria in encargo.recursos_necesarios.items():
            disponible = self.granja.obtener_cantidad_total_recurso(recurso, propietario)
            if disponible < cantidad_necesaria:
                puede = False
                break
        self.complete_order_button.config(state=NORMAL if puede else DISABLED)

    def complete_selected_order(self):
        if not self.selected_order:
            messagebox.showwarning("Advertencia", "Selecciona un encargo primero")
            return
        if not messagebox.askyesno("Confirmar", "¿Completar este encargo?"):
            return
        resultado = self.tienda.completar_encargo(self.selected_order.id, silent=True)
        messagebox.showinfo("Resultado", resultado)
        self.selected_order = None
        self.order_info_text.config(state=NORMAL)
        self.order_info_text.delete(1.0, END)
        self.order_info_text.config(state=DISABLED)
        self.complete_order_button.config(state=DISABLED)
        self.refresh_store_display()
        self.refresh_storage_display()

    # ── Eventos: Automatización ───────────────────────────────────────────

    def refresh_worker_list(self):
        self.workers_listbox.delete(0, END)
        for encargado in self.sistema_auto.encargados:
            estado = "🟢 Activo" if encargado.activo else "🔴 Inactivo"
            self.workers_listbox.insert(END, f"{encargado.nombre} ({encargado.tipo}) - {estado}")

    def on_worker_select(self, event):
        selection = self.workers_listbox.curselection()
        if selection:
            nombre = self.workers_listbox.get(selection[0]).split(" (")[0]
            self.selected_worker = self.sistema_auto.buscar_encargado(nombre)
            self.update_worker_display()

    def update_worker_display(self):
        if not self.selected_worker:
            return
        encargado = self.selected_worker

        self.worker_info_text.config(state=NORMAL)
        self.worker_info_text.delete(1.0, END)
        estado = "Activo" if encargado.activo else "Inactivo"
        self.worker_info_text.insert(END, f"Nombre: {encargado.nombre}\n")
        self.worker_info_text.insert(END, f"Tipo: {encargado.tipo}\n")
        self.worker_info_text.insert(END, f"Estado: {estado}\n")
        self.worker_info_text.insert(END, f"Tareas: {len(encargado.tareas_programadas)}\n")
        for i, tarea in enumerate(encargado.tareas_programadas, 1):
            self.worker_info_text.insert(END, f"  {i}. {tarea['accion']} → {tarea['personaje']}\n")
        self.worker_info_text.config(state=DISABLED)

        self.toggle_worker_btn.config(state=NORMAL)
        self.clear_tasks_btn.config(state=NORMAL)

    def create_new_worker_dialog(self):
        dialogo = Toplevel(self.root)
        dialogo.title("Crear Nuevo Encargado")
        dialogo.geometry("350x250")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text="Crear Nuevo Encargado", font=('Arial', 12, 'bold')).pack(pady=10)

        Label(dialogo, text="Nombre:").pack(anchor=W, padx=20)
        nombre_entry = Entry(dialogo, width=25)
        nombre_entry.pack(padx=20, pady=2)
        nombre_entry.insert(0, "Encargado")

        Label(dialogo, text="Tipo:").pack(anchor=W, padx=20)
        tipo_var = StringVar(value="humano")
        tipo_frame = Frame(dialogo)
        tipo_frame.pack(anchor=W, padx=20, pady=2)
        Radiobutton(tipo_frame, text="Humano", variable=tipo_var, value="humano").pack(side=LEFT)
        Radiobutton(tipo_frame, text="Robot", variable=tipo_var, value="robot").pack(side=LEFT, padx=(10, 0))

        def confirmar():
            nombre = nombre_entry.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            encargado = Encargado(nombre, tipo_var.get())
            self.sistema_auto.encargados.append(encargado)
            messagebox.showinfo("Éxito", f"Encargado {nombre} creado correctamente")
            self.refresh_worker_list()
            dialogo.destroy()

        Button(dialogo, text="Crear Encargado", command=confirmar,
               bg=self.colors['primary'], fg='white', font=('Arial', 10, 'bold')).pack(pady=15)
        self.root.wait_window(dialogo)

    def schedule_task(self):
        if not self.selected_worker:
            messagebox.showwarning("Advertencia", "Selecciona un encargado primero")
            return

        personaje_nombre = self.task_character_var.get()
        accion = self.task_action_var.get()
        if not personaje_nombre or not accion:
            messagebox.showwarning("Advertencia", "Selecciona un personaje y una acción")
            return

        parametros = {}
        if accion in ("alimentar", "dar_agua"):
            try:
                cantidad = int(self.task_cantidad_entry.get())
                if cantidad <= 0:
                    raise ValueError
                parametros['cantidad'] = cantidad
            except ValueError:
                messagebox.showerror("Error", "Ingresa una cantidad válida")
                return

        resultado = self.selected_worker.programar_tarea(personaje_nombre, accion, parametros)
        messagebox.showinfo("Éxito", resultado)
        self.update_worker_display()

    def execute_automation_now(self):
        self.sistema_auto.ejecutar_todos()
        messagebox.showinfo("Ejecución Completa", "Automatización ejecutada correctamente")
        self.refresh_storage_display()
        self.refresh_worker_list()
        if self.selected_worker:
            self.update_worker_display()

    def toggle_worker(self):
        if not self.selected_worker:
            return
        resultado = self.selected_worker.toggle_estado()
        messagebox.showinfo("Resultado", resultado)
        self.refresh_worker_list()
        self.update_worker_display()

    def clear_all_tasks(self):
        if not self.selected_worker:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar todas las tareas de este encargado?"):
            resultado = self.selected_worker.limpiar_tareas()
            messagebox.showinfo("Éxito", resultado)
            self.update_worker_display()

    # ── Eventos: Interacciones ────────────────────────────────────────────

    def on_interaction_char_select(self, event):
        nombre = self.interaction_char_var.get()
        self.selected_interaction_char = self.granja.buscar_personaje(nombre)
        if self.selected_interaction_char:
            self.append_interaction_result(f"Seleccionado: {nombre}")

    def append_interaction_result(self, texto):
        self.interaction_results_text.config(state=NORMAL)
        self.interaction_results_text.insert(END, texto + "\n")
        self.interaction_results_text.see(END)
        self.interaction_results_text.config(state=DISABLED)

    def interaction_lamer(self):
        if not self.selected_interaction_char:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return

        dialogo = Toplevel(self.root)
        dialogo.title("Lamer a Personaje")
        dialogo.geometry("300x150")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text=f"Lamer a {self.selected_interaction_char.nombre}").pack(pady=10)
        Label(dialogo, text="Zona:").pack()
        zona_var = StringVar(value="cara")
        ttk.Combobox(dialogo, textvariable=zona_var,
                     values=["cara", "pecho", "genitales", "pies", "espalda", "axilas"],
                     state="readonly").pack(pady=5)

        def confirmar():
            resultado = self.selected_interaction_char.interactuar_lamer(zona_var.get())
            self.append_interaction_result(resultado)
            messagebox.showinfo("Resultado", resultado)
            dialogo.destroy()

        Button(dialogo, text="Lamer", command=confirmar,
               bg=self.colors['success'], fg='white').pack(pady=10)
        self.root.wait_window(dialogo)

    def interaction_tocar(self):
        if not self.selected_interaction_char:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return

        dialogo = Toplevel(self.root)
        dialogo.title("Tocar/Acariciar a Personaje")
        dialogo.geometry("350x200")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text=f"Tocar a {self.selected_interaction_char.nombre}").pack(pady=10)
        Label(dialogo, text="Zona:").pack()
        zona_var = StringVar(value="cara")
        ttk.Combobox(dialogo, textvariable=zona_var,
                     values=["cara", "pecho", "genitales", "muslos", "espalda", "cabello"],
                     state="readonly").pack(pady=5)

        Label(dialogo, text="Intensidad:").pack(pady=(10, 0))
        intensidad_var = StringVar(value="normal")
        for texto, valor in [("Suave", "suave"), ("Normal", "normal"), ("Intenso", "intenso")]:
            Radiobutton(dialogo, text=texto, variable=intensidad_var, value=valor).pack(anchor=W)

        def confirmar():
            resultado = self.selected_interaction_char.interactuar_tocar(zona_var.get(), intensidad_var.get())
            self.append_interaction_result(resultado)
            messagebox.showinfo("Resultado", resultado)
            dialogo.destroy()

        Button(dialogo, text="Tocar/Acariciar", command=confirmar,
               bg=self.colors['success'], fg='white').pack(pady=10)
        self.root.wait_window(dialogo)

    def interaction_penetrar(self):
        if not self.selected_interaction_char:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return

        dialogo = Toplevel(self.root)
        dialogo.title("Penetrar a Personaje")
        dialogo.geometry("350x250")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text=f"Penetrar a {self.selected_interaction_char.nombre}").pack(pady=10)
        Label(dialogo, text="Agujero:").pack()
        agujero_var = StringVar(value="vaginal")
        ttk.Combobox(dialogo, textvariable=agujero_var,
                     values=["vaginal", "anal", "oral"], state="readonly").pack(pady=5)

        Label(dialogo, text="Objeto:").pack(pady=(10, 0))
        objeto_var = StringVar(value="ninguno")
        for texto, valor in [("Ninguno", "ninguno"), ("Dedo", "dedo"),
                             ("Juguete Pequeño", "juguete_pequeño"),
                             ("Juguete Grande", "juguete_grande")]:
            Radiobutton(dialogo, text=texto, variable=objeto_var, value=valor).pack(anchor=W)

        def confirmar():
            objeto = objeto_var.get() if objeto_var.get() != "ninguno" else None
            resultado = self.selected_interaction_char.interactuar_penetrar(agujero_var.get(), objeto)
            self.append_interaction_result(resultado)
            messagebox.showinfo("Resultado", resultado)
            dialogo.destroy()

        Button(dialogo, text="Penetrar", command=confirmar,
               bg=self.colors['success'], fg='white').pack(pady=10)
        self.root.wait_window(dialogo)

    def interaction_insertar_objeto(self):
        if not self.selected_interaction_char:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return

        dialogo = Toplevel(self.root)
        dialogo.title("Insertar Objeto en Personaje")
        dialogo.geometry("350x200")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text=f"Insertar objeto en {self.selected_interaction_char.nombre}").pack(pady=10)

        Label(dialogo, text="Agujero:").pack()
        agujero_var = StringVar(value="vaginal")
        ttk.Combobox(dialogo, textvariable=agujero_var,
                     values=["vaginal", "anal", "oral"], state="readonly").pack(pady=5)

        Label(dialogo, text="Objeto:").pack(pady=(10, 0))
        objeto_entry = Entry(dialogo, width=20)
        objeto_entry.pack(pady=5)
        objeto_entry.insert(0, "objeto")

        Label(dialogo, text="Tamaño:").pack(pady=(10, 0))
        tamano_var = StringVar(value="mediano")
        ttk.Combobox(dialogo, textvariable=tamano_var,
                     values=["pequeño", "mediano", "grande"], state="readonly").pack(pady=5)

        def confirmar():
            resultado = self.selected_interaction_char.insertar_objeto(
                agujero_var.get(), objeto_entry.get(), tamano_var.get())
            self.append_interaction_result(resultado)
            messagebox.showinfo("Resultado", resultado)
            dialogo.destroy()

        Button(dialogo, text="Insertar Objeto", command=confirmar,
               bg=self.colors['success'], fg='white').pack(pady=10)
        self.root.wait_window(dialogo)

    def interaction_boca(self):
        if not self.selected_interaction_char:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return

        dialogo = Toplevel(self.root)
        dialogo.title("Poner Boca en Personaje")
        dialogo.geometry("300x150")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text=f"Poner boca en {self.selected_interaction_char.nombre}").pack(pady=10)
        Label(dialogo, text="Zona:").pack()
        zona_var = StringVar(value="genitales")
        ttk.Combobox(dialogo, textvariable=zona_var,
                     values=["genitales", "ano", "boca", "axilas"], state="readonly").pack(pady=5)

        def confirmar():
            resultado = self.selected_interaction_char.interactuar_directo(
                self.selected_interaction_char, zona_var.get())
            self.append_interaction_result(resultado)
            messagebox.showinfo("Resultado", resultado)
            dialogo.destroy()

        Button(dialogo, text="Poner Boca en", command=confirmar,
               bg=self.colors['success'], fg='white').pack(pady=10)
        self.root.wait_window(dialogo)

    # ── Eventos: Controles / Tiempo / Guardado ────────────────────────────

    def advance_one_hour(self):
        self.granja.avanzar_tiempo()
        self.after_time_advance()

    def advance_three_hours(self):
        for _ in range(3):
            self.granja.avanzar_tiempo()
        self.after_time_advance()

    def advance_six_hours(self):
        for _ in range(6):
            self.granja.avanzar_tiempo()
        self.after_time_advance()

    def after_time_advance(self):
        self.update_time_display()
        if self.selected_character:
            self.update_character_display()
        self.refresh_storage_display()
        self.refresh_store_display()

    def update_time_display(self):
        hora = self.granja.hora_actual
        periodo = "AM" if hora < 12 else "PM"
        hora_12 = hora % 12
        if hora_12 == 0:
            hora_12 = 12
        self.game_time_label.config(text=f"Hora: {hora_12:02d}:00 {periodo}")
        self.status_time_label.config(text=f"Hora: {hora_12:02d}:00 {periodo}")

    def save_game_dialog(self):
        dialogo = Toplevel(self.root)
        dialogo.title("Guardar Partida")
        dialogo.geometry("350x150")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text="Nombre de la partida:").pack(pady=10)
        nombre_entry = Entry(dialogo, width=30)
        nombre_entry.pack(pady=5)
        nombre_entry.insert(0, "")

        def guardar():
            nombre = nombre_entry.get().strip()
            exito, mensaje = self.sistema_guardado.guardar_partida(
                self.granja, self.tienda, self.sistema_auto, nombre if nombre else None)
            messagebox.showinfo("Guardar", mensaje)
            dialogo.destroy()

        Button(dialogo, text="Guardar", command=guardar,
               bg=self.colors['success'], fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
        self.root.wait_window(dialogo)

    def load_game_dialog(self):
        partidas = self.sistema_guardado.listar_partidas()
        if not partidas:
            messagebox.showinfo("Info", "No hay partidas guardadas")
            return

        dialogo = Toplevel(self.root)
        dialogo.title("Cargar Partida")
        dialogo.geometry("350x300")
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
        dialogo.grab_set()

        Label(dialogo, text="Selecciona una partida:", font=('Arial', 10)).pack(pady=10)

        listbox = Listbox(dialogo, font=('Arial', 9))
        listbox.pack(fill=BOTH, expand=True, padx=20, pady=10)
        for p in partidas:
            listbox.insert(END, p)

        def cargar():
            sel = listbox.curselection()
            if sel:
                nombre = listbox.get(sel[0])
                datos, mensaje = self.sistema_guardado.cargar_partida(nombre)
                if datos:
                    self.granja, self.tienda, self.sistema_auto = restaurar_desde_datos(datos)
                    messagebox.showinfo("Éxito", "Partida cargada correctamente")
                    self.selected_character = None
                    self.selected_order = None
                    self.selected_worker = None
                    self.refresh_all()
                    dialogo.destroy()
                else:
                    messagebox.showerror("Error", mensaje)

        Button(dialogo, text="Cargar", command=cargar,
               bg=self.colors['success'], fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
        self.root.wait_window(dialogo)

    def list_saved_games(self):
        partidas = self.sistema_guardado.listar_partidas()
        if not partidas:
            messagebox.showinfo("Partidas Guardadas", "No hay partidas guardadas")
            return
        texto = "Partidas guardadas:\n\n"
        for i, p in enumerate(partidas, 1):
            texto += f"  {i}. {p}\n"
        messagebox.showinfo("Partidas Guardadas", texto)


if __name__ == "__main__":
    root = Tk()
    app = SimuladorGranjaGUI(root)
    root.mainloop()
