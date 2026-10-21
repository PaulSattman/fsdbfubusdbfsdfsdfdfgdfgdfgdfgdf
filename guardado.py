"""
Sistema de Guardado y Carga
guardado.py
"""

import json
import os
from datetime import datetime
from constants import *

class SistemaGuardado:
    def __init__(self, carpeta_guardados="guardados"):
        self.carpeta_guardados = carpeta_guardados
        # Crear carpeta si no existe
        if not os.path.exists(carpeta_guardados):
            os.makedirs(carpeta_guardados)
    
    def guardar_partida(self, granja, tienda, sistema_auto, nombre_partida=None):
        """Guarda el estado completo del juego"""
        if not nombre_partida:
            # Generar nombre automático con fecha y hora
            nombre_partida = f"partida_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Preparar datos para guardar
        datos = {
            'fecha_guardado': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'granja': self._serializar_granja(granja),
            'tienda': self._serializar_tienda(tienda),
            'automatizacion': self._serializar_automatizacion(sistema_auto)
        }
        
        # Guardar en archivo JSON
        ruta_archivo = os.path.join(self.carpeta_guardados, f"{nombre_partida}.json")
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True, f"✅ Partida guardada como: {nombre_partida}"
        except Exception as e:
            return False, f"❌ Error al guardar: {str(e)}"
    
    def cargar_partida(self, nombre_partida):
        """Carga una partida guardada"""
        ruta_archivo = os.path.join(self.carpeta_guardados, f"{nombre_partida}.json")
        
        if not os.path.exists(ruta_archivo):
            return None, f"❌ No se encontró la partida: {nombre_partida}"
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            return datos, f"✅ Partida cargada: {nombre_partida}"
        except Exception as e:
            return None, f"❌ Error al cargar: {str(e)}"
    
    def listar_partidas(self):
        """Lista todas las partidas guardadas"""
        archivos = [f[:-5] for f in os.listdir(self.carpeta_guardados) if f.endswith('.json')]
        return sorted(archivos, reverse=True)  # Más recientes primero
    
    def eliminar_partida(self, nombre_partida):
        """Elimina una partida guardada"""
        ruta_archivo = os.path.join(self.carpeta_guardados, f"{nombre_partida}.json")
        
        if not os.path.exists(ruta_archivo):
            return False, f"❌ No se encontró la partida: {nombre_partida}"
        
        try:
            os.remove(ruta_archivo)
            return True, f"✅ Partida eliminada: {nombre_partida}"
        except Exception as e:
            return False, f"❌ Error al eliminar: {str(e)}"
    
    def _serializar_granja(self, granja):
        """Convierte la granja a formato JSON"""
        return {
            'hora_actual': granja.hora_actual,
            'personajes': [self._serializar_personaje(p) for p in granja.personajes],
            'almacen': {f"{k[0]}|{k[1]}": v for k, v in granja.almacen.items()}
        }
    
    def _serializar_personaje(self, personaje):
        """Convierte un personaje a formato JSON"""
        return {
            'nombre': personaje.nombre,
            'tipo': personaje.tipo,
            'edad': personaje.edad,
            'hambre': personaje.hambre,
            'sed': personaje.sed,
            'higiene': personaje.higiene,
            'energia': personaje.energia,
            'recursos_disponibles': personaje.recursos_disponibles,
            'comida_consumida': personaje.comida_consumida,
            'agua_consumida': personaje.agua_consumida
        }
    
    def _serializar_tienda(self, tienda):
        """Convierte la tienda a formato JSON"""
        return {
            'dinero': tienda.dinero,
            'encargos_completados': tienda.encargos_completados,
            'contador_encargos': tienda.contador_encargos,
            'encargos_disponibles': [self._serializar_encargo(e) for e in tienda.encargos_disponibles]
        }
    
    def _serializar_encargo(self, encargo):
        """Convierte un encargo a formato JSON"""
        return {
            'id': encargo.id,
            'descripcion': encargo.descripcion,
            'recursos_necesarios': {f"{k[0]}|{k[1] if k[1] else 'None'}": v for k, v in encargo.recursos_necesarios.items()},
            'pago': encargo.pago,
            'cliente': encargo.cliente
        }
    
    def _serializar_automatizacion(self, sistema_auto):
        """Convierte el sistema de automatización a formato JSON"""
        return {
            'contador_encargados': sistema_auto.contador_encargados,
            'encargados': [self._serializar_encargado(e) for e in sistema_auto.encargados]
        }
    
    def _serializar_encargado(self, encargado):
        """Convierte un encargado a formato JSON"""
        return {
            'nombre': encargado.nombre,
            'tipo': encargado.tipo,
            'activo': encargado.activo,
            'tareas_programadas': encargado.tareas_programadas
        }
    
    def menu_guardado(self, granja, tienda, sistema_auto):
        """Menú para gestionar guardado/carga"""
        while True:
            print("\n" + "="*60)
            print("💾 GESTIÓN DE PARTIDAS")
            print("="*60)
            print("1. Guardar partida actual")
            print("2. Cargar partida")
            print("3. Ver partidas guardadas")
            print("4. Eliminar partida")
            print("5. Volver")
            print("="*60)
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == "1":
                nombre = input("\nNombre de la partida (Enter para auto): ").strip()
                exito, mensaje = self.guardar_partida(granja, tienda, sistema_auto, nombre if nombre else None)
                print(mensaje)
                
            elif opcion == "2":
                partidas = self.listar_partidas()
                if not partidas:
                    print("\n❌ No hay partidas guardadas")
                else:
                    print("\n📁 Partidas disponibles:")
                    for i, partida in enumerate(partidas, 1):
                        print(f"   {i}. {partida}")
                    
                    seleccion = input("\nNombre de la partida a cargar: ").strip()
                    if seleccion:
                        return 'cargar', seleccion
                
            elif opcion == "3":
                partidas = self.listar_partidas()
                if not partidas:
                    print("\n❌ No hay partidas guardadas")
                else:
                    print("\n📁 Partidas guardadas:")
                    for i, partida in enumerate(partidas, 1):
                        ruta = os.path.join(self.carpeta_guardados, f"{partida}.json")
                        tamaño = os.path.getsize(ruta) / 1024  # KB
                        print(f"   {i}. {partida} ({tamaño:.1f} KB)")
                
            elif opcion == "4":
                partidas = self.listar_partidas()
                if not partidas:
                    print("\n❌ No hay partidas guardadas")
                else:
                    print("\n📁 Partidas disponibles:")
                    for i, partida in enumerate(partidas, 1):
                        print(f"   {i}. {partida}")
                    
                    nombre = input("\nNombre de la partida a eliminar: ").strip()
                    if nombre:
                        confirmacion = input(f"⚠️ ¿Seguro que quieres eliminar '{nombre}'? (s/n): ").strip().lower()
                        if confirmacion == 's':
                            exito, mensaje = self.eliminar_partida(nombre)
                            print(mensaje)
                
            elif opcion == "5":
                return None, None
            
            else:
                print("❌ Opción no válida")
            
            input("\nPresiona Enter para continuar...")


def restaurar_desde_datos(datos):
    """Restaura los objetos del juego desde datos guardados"""
    from granja import Granja
    from personaje import Personaje
    from tienda import Tienda, Encargo
    from encargado import SistemaAutomatizacion, Encargado
    from collections import defaultdict
    
    # Restaurar granja
    granja = Granja()
    granja.hora_actual = datos['granja']['hora_actual']
    
    # Restaurar personajes
    for p_data in datos['granja']['personajes']:
        personaje = Personaje(p_data['nombre'], p_data['tipo'], p_data['edad'])
        personaje.hambre = p_data['hambre']
        personaje.sed = p_data['sed']
        personaje.higiene = p_data['higiene']
        personaje.energia = p_data['energia']
        personaje.recursos_disponibles = p_data['recursos_disponibles']
        personaje.comida_consumida = p_data['comida_consumida']
        personaje.agua_consumida = p_data['agua_consumida']
        granja.personajes.append(personaje)
    
    # Restaurar almacén
    granja.almacen = defaultdict(float)
    for key, value in datos['granja']['almacen'].items():
        recurso, propietario = key.split('|')
        granja.almacen[(recurso, propietario)] = value
    
    # Restaurar tienda
    tienda = Tienda(granja)
    tienda.dinero = datos['tienda']['dinero']
    tienda.encargos_completados = datos['tienda']['encargos_completados']
    tienda.contador_encargos = datos['tienda']['contador_encargos']
    
    # Restaurar encargos
    tienda.encargos_disponibles = []
    for e_data in datos['tienda']['encargos_disponibles']:
        recursos_necesarios = {}
        for key, value in e_data['recursos_necesarios'].items():
            recurso, propietario = key.split('|')
            propietario = None if propietario == 'None' else propietario
            recursos_necesarios[(recurso, propietario)] = value
        
        encargo = Encargo(
            e_data['id'],
            e_data['descripcion'],
            recursos_necesarios,
            e_data['pago'],
            e_data['cliente']
        )
        tienda.encargos_disponibles.append(encargo)
    
    # Restaurar sistema de automatización
    sistema_auto = SistemaAutomatizacion(granja)
    sistema_auto.contador_encargados = datos['automatizacion']['contador_encargados']
    
    # Restaurar encargados
    sistema_auto.encargados = []
    for enc_data in datos['automatizacion']['encargados']:
        encargado = Encargado(enc_data['nombre'], enc_data['tipo'])
        encargado.activo = enc_data['activo']
        encargado.tareas_programadas = enc_data['tareas_programadas']
        sistema_auto.encargados.append(encargado)
    
    return granja, tienda, sistema_auto