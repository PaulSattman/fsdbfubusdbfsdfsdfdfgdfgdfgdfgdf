"""
Clase Granja - Gestión del escenario principal
granja.py
"""

from collections import defaultdict
from constants import *

class Granja:
    def __init__(self):
        self.personajes = []
        self.hora_actual = 8  # Empieza a las 8 AM
        
        # Almacén de recursos: {(tipo_recurso, propietario): cantidad}
        self.almacen = defaultdict(float)
        
    def agregar_personaje(self, personaje):
        """Agrega un personaje a la granja"""
        self.personajes.append(personaje)
        print(f"✅ {personaje.nombre} ({personaje.edad} años) ha sido agregado a la granja")
        
    def buscar_personaje(self, nombre):
        """Busca un personaje por nombre"""
        for p in self.personajes:
            if p.nombre.lower() == nombre.lower():
                return p
        return None
        
    def mostrar_personajes(self):
        """Muestra todos los personajes y sus estados básicos"""
        print("\n" + "="*80)
        print("👥 PERSONAJES EN LA GRANJA")
        print("="*80)
        
        if not self.personajes:
            print("No hay personajes en la granja")
            return
            
        for p in self.personajes:
            estado_hambre = "🟢" if p.hambre < HAMBRE_BUENO_UMBRAL else "🟡" if p.hambre < HAMBRE_URGENTE_UMBRAL else "🔴"
            estado_sed = "🟢" if p.sed < SED_BUENO_UMBRAL else "🟡" if p.sed < SED_URGENTE_UMBRAL else "🔴"
            estado_higiene = "🟢" if p.higiene > HIGIENE_BUENA_UMBRAL else "🟡" if p.higiene > HIGIENE_BAJA_UMBRAL else "🔴"
            
            print(f"\n👤 {p.nombre} ({p.tipo}) - {p.edad} años")
            print(f"   Hambre: {estado_hambre} {p.hambre:.0f}%  |  Sed: {estado_sed} {p.sed:.0f}%  |  Higiene: {estado_higiene} {p.higiene:.0f}%")
            
            recursos_totales = p.obtener_recursos_totales()
            print(f"   📦 Recursos disponibles: {recursos_totales:.1f} unidades")
            
        print("="*80)
        
    def alimentar_personaje(self, nombre, cantidad):
        """Alimenta a un personaje específico"""
        personaje = self.buscar_personaje(nombre)
        if personaje:
            mensaje = personaje.alimentar(cantidad)
            print(mensaje)
            personaje.mostrar_estado()
        else:
            print(f"❌ No se encontró al personaje {nombre}")
            
    def dar_agua_personaje(self, nombre, cantidad):
        """Da agua a un personaje específico"""
        personaje = self.buscar_personaje(nombre)
        if personaje:
            mensaje = personaje.dar_agua(cantidad)
            print(mensaje)
            personaje.mostrar_estado()
        else:
            print(f"❌ No se encontró al personaje {nombre}")
            
    def limpiar_personaje(self, nombre):
        """Limpia a un personaje específico"""
        personaje = self.buscar_personaje(nombre)
        if personaje:
            mensaje = personaje.limpiar()
            print(mensaje)
            personaje.mostrar_estado()
        else:
            print(f"❌ No se encontró al personaje {nombre}")
            
    def recolectar_recursos_personaje(self, nombre):
        """Recolecta los recursos de un personaje y los guarda en el almacén"""
        personaje = self.buscar_personaje(nombre)
        if personaje:
            recursos = personaje.recolectar_recursos()
            if recursos:
                print(f"\n✅ Recursos recolectados de {nombre}:")
                for recurso, cantidad in recursos.items():
                    clave = (recurso, nombre)
                    self.almacen[clave] += cantidad
                    unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
                    print(f"   • {recurso.replace('_', ' ').title()}: {cantidad:.1f}{unidad}")
                print(f"\n📦 Los recursos han sido almacenados")
            else:
                print(f"❌ {nombre} no tiene recursos disponibles para recolectar")
        else:
            print(f"❌ No se encontró al personaje {nombre}")
            
    def mostrar_almacen(self):
        """Muestra el contenido del almacén"""
        print("\n" + "="*80)
        print("📦 ALMACÉN DE RECURSOS")
        print("="*80)
        
        if not self.almacen:
            print("El almacén está vacío")
            print("="*80)
            return
            
        # Organizar por recurso
        recursos_por_tipo = defaultdict(list)
        for (recurso, propietario), cantidad in self.almacen.items():
            recursos_por_tipo[recurso].append((propietario, cantidad))
            
        for recurso in sorted(recursos_por_tipo.keys()):
            unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
            print(f"\n🧪 {recurso.replace('_', ' ').title()}:")
            total = 0
            for propietario, cantidad in recursos_por_tipo[recurso]:
                print(f"   • De {propietario}: {cantidad:.1f}{unidad}")
                total += cantidad
            print(f"   ➡️ Total: {total:.1f}{unidad}")
            
        print("="*80)
        
    def obtener_recurso_almacen(self, tipo_recurso, cantidad_necesaria, propietario=None):
        """
        Extrae recursos del almacén
        Si propietario es None, toma de cualquiera que tenga disponible
        Retorna la cantidad que pudo extraer
        """
        cantidad_extraida = 0
        
        if propietario:
            # Extraer de un propietario específico
            clave = (tipo_recurso, propietario)
            if clave in self.almacen:
                disponible = self.almacen[clave]
                extraer = min(disponible, cantidad_necesaria)
                self.almacen[clave] -= extraer
                if self.almacen[clave] <= 0:
                    del self.almacen[clave]
                cantidad_extraida = extraer
        else:
            # Extraer de cualquier propietario
            for clave in list(self.almacen.keys()):
                if clave[0] == tipo_recurso and cantidad_extraida < cantidad_necesaria:
                    disponible = self.almacen[clave]
                    necesaria = cantidad_necesaria - cantidad_extraida
                    extraer = min(disponible, necesaria)
                    self.almacen[clave] -= extraer
                    if self.almacen[clave] <= 0:
                        del self.almacen[clave]
                    cantidad_extraida += extraer
                    
        return cantidad_extraida
        
    def avanzar_tiempo(self):
        """Avanza el tiempo 1 hora y actualiza todos los personajes"""
        self.hora_actual = (self.hora_actual + 1) % 24
        
        # Actualizar estados de todos los personajes
        for personaje in self.personajes:
            personaje.actualizar_estados()
            
        # Eventos especiales según la hora
        if self.hora_actual == 8:
            print("\n🌅 ¡Es de mañana! Los personajes tienen más hambre")
        elif self.hora_actual == 12:
            print("\n☀️ ¡Es mediodía! Hora de almorzar")
        elif self.hora_actual == 20:
            print("\n🌙 ¡Es de noche! Los personajes se preparan para dormir")
            
    def obtener_cantidad_total_recurso(self, tipo_recurso, propietario=None):
        """Devuelve la cantidad total de un recurso en el almacén"""
        total = 0
        for (recurso, prop), cantidad in self.almacen.items():
            if recurso == tipo_recurso:
                if propietario is None or prop == propietario:
                    total += cantidad
        return total
    
    def interactuar_con_personaje(self, nombre):
        """Menú de interacciones con un personaje"""
        personaje = self.buscar_personaje(nombre)
        if not personaje:
            print(f"❌ No se encontró al personaje {nombre}")
            return
            
        while True:
            print("\n" + "="*80)
            print(f"🔞 INTERACCIONES CON {personaje.nombre}")
            print("="*80)
            print("1. Lamer")
            print("2. Tocar/Acariciar")
            print("3. Penetrar")
            print("4. Insertar objeto")
            print("5. Poner tu boca en")
            print("6. Ver estado del personaje")
            print("7. Volver")
            print("="*80)
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == "1":
                print("\nZonas disponibles: cara, pecho, genitales, pies, espalda, axilas")
                zona = input("¿Qué zona quieres lamer? ").strip().lower()
                resultado = personaje.interactuar_lamer(zona)
                print(f"\n{resultado}")
                
            elif opcion == "2":
                print("\nZonas disponibles: cara, pecho, genitales, muslos, espalda, cabello")
                zona = input("¿Qué zona quieres tocar? ").strip().lower()
                print("\nIntensidades: suave, normal, intenso")
                intensidad = input("¿Qué intensidad? (default: normal) ").strip().lower() or 'normal'
                resultado = personaje.interactuar_tocar(zona, intensidad)
                print(f"\n{resultado}")
                
            elif opcion == "3":
                print("\nAgujeros disponibles: vaginal, anal, oral")
                agujero = input("¿Qué agujero? ").strip().lower()
                print("\nObjetos: dedo, juguete_pequeño, juguete_grande, otro, o Enter para ninguno")
                objeto = input("¿Con qué objeto? ").strip().lower() or None
                resultado = personaje.interactuar_penetrar(agujero, objeto)
                print(f"\n{resultado}")
                
            elif opcion == "4":
                print("\nAgujeros disponibles: vaginal, anal, oral")
                agujero = input("¿En qué agujero? ").strip().lower()
                objeto = input("Describe el objeto: ").strip()
                print("\nTamaños: pequeño, mediano, grande")
                tamano = input("¿Qué tamaño? (default: mediano) ").strip().lower() or 'mediano'
                resultado = personaje.insertar_objeto(agujero, objeto, tamano)
                print(f"\n{resultado}")
            
            elif opcion == "5":
                print("\nOpciones disponibles: genitales, ano, boca, axilas")
                zona = input("¿Dónde quieres poner tu boca? ").strip().lower()
                if zona in ["genitales", "ano", "boca", "axilas"]:
                    resultado = personaje.interactuar_directo(personaje, zona)
                else:
                    resultado = "❌ Opción no válida. Inténtalo de nuevo."
                print(f"\n{resultado}")
                
            elif opcion == "6":
                personaje.mostrar_estado()
                
            elif opcion == "7":
                break
                
            else:
                print("❌ Opción no válida")
                
            input("\nPresiona Enter para continuar...")