"""
Clase Encargado y Máquina - Automatización de tareas
encargado.py
"""

from constants import *

class Encargado:
    def __init__(self, nombre, tipo):
        """
        tipo puede ser: 'humano', 'maquina_recoleccion', 'maquina_alimentacion', 'maquina_limpieza'
        """
        self.nombre = nombre
        self.tipo = tipo
        self.activo = True
        self.tareas_programadas = []  # Lista de tareas: [(personaje, accion, parametros)]
        
    def programar_tarea(self, personaje_nombre, accion, parametros=None):
        """
        Programa una tarea para ejecutar automáticamente
        accion: 'recolectar', 'alimentar', 'dar_agua', 'limpiar'
        parametros: dict con detalles adicionales
        """
        tarea = {
            'personaje': personaje_nombre,
            'accion': accion,
            'parametros': parametros or {}
        }
        self.tareas_programadas.append(tarea)
        return f"✅ Tarea programada: {accion} para {personaje_nombre}"
        
    def ejecutar_tareas(self, granja):
        """Ejecuta todas las tareas programadas"""
        if not self.activo:
            return "❌ Encargado desactivado"
            
        resultados = []
        for tarea in self.tareas_programadas:
            personaje = granja.buscar_personaje(tarea['personaje'])
            if not personaje:
                resultados.append(f"❌ No se encontró a {tarea['personaje']}")
                continue
                
            accion = tarea['accion']
            parametros = tarea['parametros']
            
            if accion == 'recolectar':
                # Recolectar recursos específicos o todos
                recursos_objetivo = parametros.get('recursos', [])
                if recursos_objetivo:
                    # Recolectar solo recursos específicos
                    recursos_recolectados = {}
                    for recurso in recursos_objetivo:
                        if recurso in personaje.recursos_disponibles:
                            cantidad = personaje.recursos_disponibles[recurso]
                            if cantidad > 0:
                                recursos_recolectados[recurso] = cantidad
                                personaje.recursos_disponibles[recurso] = 0
                                clave = (recurso, personaje.nombre)
                                granja.almacen[clave] += cantidad
                    
                    if recursos_recolectados:
                        recursos_texto = ", ".join([f"{r}: {c:.1f}" for r, c in recursos_recolectados.items()])
                        resultados.append(f"✅ Recolectado de {personaje.nombre}: {recursos_texto}")
                    else:
                        resultados.append(f"⚠️ {personaje.nombre} no tiene los recursos especificados")
                else:
                    # Recolectar todos los recursos
                    granja.recolectar_recursos_personaje(personaje.nombre)
                    resultados.append(f"✅ Todos los recursos recolectados de {personaje.nombre}")
                    
            elif accion == 'alimentar':
                cantidad = parametros.get('cantidad', AUTO_ALIMENTAR_CANTIDAD_DEFECTO)
                granja.alimentar_personaje(personaje.nombre, cantidad)
                resultados.append(f"✅ {personaje.nombre} alimentado con {cantidad}g")

            elif accion == 'dar_agua':
                cantidad = parametros.get('cantidad', AUTO_DAR_AGUA_CANTIDAD_DEFECTO)
                granja.dar_agua_personaje(personaje.nombre, cantidad)
                resultados.append(f"✅ {personaje.nombre} hidratado con {cantidad}ml")
                
            elif accion == 'limpiar':
                granja.limpiar_personaje(personaje.nombre)
                resultados.append(f"✅ {personaje.nombre} limpiado")
                
        return resultados
        
    def mostrar_info(self):
        """Muestra la información del encargado"""
        estado = "🟢 Activo" if self.activo else "🔴 Desactivado"
        print(f"\n{'='*60}")
        print(f"👷 {self.nombre} ({self.tipo})")
        print(f"Estado: {estado}")
        print(f"Tareas programadas: {len(self.tareas_programadas)}")
        
        if self.tareas_programadas:
            print("\n📋 Lista de tareas:")
            for i, tarea in enumerate(self.tareas_programadas, 1):
                print(f"   {i}. {tarea['accion']} → {tarea['personaje']}")
                if tarea['parametros']:
                    for k, v in tarea['parametros'].items():
                        print(f"      • {k}: {v}")
        print(f"{'='*60}")
        
    def limpiar_tareas(self):
        """Elimina todas las tareas programadas"""
        self.tareas_programadas = []
        return "✅ Todas las tareas han sido eliminadas"
        
    def toggle_estado(self):
        """Activa/desactiva el encargado"""
        self.activo = not self.activo
        estado = "activado" if self.activo else "desactivado"
        return f"✅ Encargado {estado}"


class SistemaAutomatizacion:
    def __init__(self, granja):
        self.granja = granja
        self.encargados = []
        self.contador_encargados = 1
        
    def crear_encargado(self, nombre, tipo):
        """Crea un nuevo encargado o máquina"""
        encargado = Encargado(nombre, tipo)
        self.encargados.append(encargado)
        return encargado
        
    def buscar_encargado(self, nombre):
        """Busca un encargado por nombre"""
        for enc in self.encargados:
            if enc.nombre.lower() == nombre.lower():
                return enc
        return None
        
    def ejecutar_todos(self):
        """Ejecuta las tareas de todos los encargados activos"""
        print("\n🤖 Ejecutando automatización...")
        resultados_totales = []
        
        for encargado in self.encargados:
            if encargado.activo and encargado.tareas_programadas:
                print(f"\n👷 {encargado.nombre} trabajando...")
                resultados = encargado.ejecutar_tareas(self.granja)
                resultados_totales.extend(resultados)
                
        if resultados_totales:
            print("\n📊 Resultados de la automatización:")
            for resultado in resultados_totales:
                print(f"   {resultado}")
        else:
            print("⚠️ No hay tareas programadas o encargados activos")
            
    def mostrar_todos(self):
        """Muestra todos los encargados"""
        print("\n" + "="*80)
        print("👷 SISTEMA DE AUTOMATIZACIÓN")
        print("="*80)
        
        if not self.encargados:
            print("No hay encargados ni máquinas configurados")
            return
            
        for enc in self.encargados:
            estado = "🟢" if enc.activo else "🔴"
            print(f"{estado} {enc.nombre} ({enc.tipo}) - {len(enc.tareas_programadas)} tareas")
            
        print("="*80)
        
    def menu_automatizacion(self):
        """Menú para gestionar la automatización"""
        while True:
            print("\n" + "="*80)
            print("🤖 GESTIÓN DE AUTOMATIZACIÓN")
            print("="*80)
            print("1. Ver encargados/máquinas")
            print("2. Crear nuevo encargado/máquina")
            print("3. Programar tareas")
            print("4. Ejecutar automatización ahora")
            print("5. Ver detalles de un encargado")
            print("6. Activar/Desactivar encargado")
            print("7. Eliminar tareas de un encargado")
            print("8. Volver")
            print("="*80)
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == "1":
                self.mostrar_todos()
                
            elif opcion == "2":
                print("\nTipos disponibles:")
                print("1. Humano (versátil)")
                print("2. Máquina de Recolección")
                print("3. Máquina de Alimentación")
                print("4. Máquina de Limpieza")
                
                tipo_opcion = input("Tipo: ").strip()
                tipos = {
                    "1": "humano",
                    "2": "maquina_recoleccion",
                    "3": "maquina_alimentacion",
                    "4": "maquina_limpieza"
                }
                
                if tipo_opcion in tipos:
                    nombre = input("Nombre del encargado/máquina: ").strip()
                    enc = self.crear_encargado(nombre, tipos[tipo_opcion])
                    print(f"✅ {nombre} creado exitosamente")
                else:
                    print("❌ Tipo inválido")
                    
            elif opcion == "3":
                self.mostrar_todos()
                if not self.encargados:
                    continue
                    
                nombre = input("\n¿A quién quieres programar? ").strip()
                enc = self.buscar_encargado(nombre)
                
                if enc:
                    self.granja.mostrar_personajes()
                    personaje_nombre = input("\n¿Para qué personaje? ").strip()
                    
                    print("\nAcciones disponibles:")
                    print("1. Recolectar recursos")
                    print("2. Alimentar")
                    print("3. Dar agua")
                    print("4. Limpiar")
                    
                    accion_opcion = input("Acción: ").strip()
                    
                    parametros = {}
                    accion = None
                    
                    if accion_opcion == "1":
                        accion = "recolectar"
                        especifico = input("¿Recursos específicos? (s/n): ").strip().lower()
                        if especifico == 's':
                            recursos_str = input("Recursos separados por coma (ej: orina,leche): ").strip()
                            recursos = [r.strip() for r in recursos_str.split(',')]
                            parametros['recursos'] = recursos
                            
                    elif accion_opcion == "2":
                        accion = "alimentar"
                        cantidad = input("Cantidad (g, default 400): ").strip()
                        if cantidad:
                            parametros['cantidad'] = int(cantidad)
                            
                    elif accion_opcion == "3":
                        accion = "dar_agua"
                        cantidad = input("Cantidad (ml, default 300): ").strip()
                        if cantidad:
                            parametros['cantidad'] = int(cantidad)
                            
                    elif accion_opcion == "4":
                        accion = "limpiar"
                        
                    if accion:
                        mensaje = enc.programar_tarea(personaje_nombre, accion, parametros)
                        print(mensaje)
                else:
                    print(f"❌ No se encontró a {nombre}")
                    
            elif opcion == "4":
                self.ejecutar_todos()
                
            elif opcion == "5":
                self.mostrar_todos()
                if self.encargados:
                    nombre = input("\n¿De quién quieres ver detalles? ").strip()
                    enc = self.buscar_encargado(nombre)
                    if enc:
                        enc.mostrar_info()
                    else:
                        print(f"❌ No se encontró a {nombre}")
                        
            elif opcion == "6":
                self.mostrar_todos()
                if self.encargados:
                    nombre = input("\n¿A quién quieres activar/desactivar? ").strip()
                    enc = self.buscar_encargado(nombre)
                    if enc:
                        print(enc.toggle_estado())
                    else:
                        print(f"❌ No se encontró a {nombre}")
                        
            elif opcion == "7":
                self.mostrar_todos()
                if self.encargados:
                    nombre = input("\n¿De quién quieres eliminar tareas? ").strip()
                    enc = self.buscar_encargado(nombre)
                    if enc:
                        print(enc.limpiar_tareas())
                    else:
                        print(f"❌ No se encontró a {nombre}")
                        
            elif opcion == "8":
                break
                
            else:
                print("❌ Opción no válida")
                
            input("\nPresiona Enter para continuar...")