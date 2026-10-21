"""
Clase Tienda - Gestión de encargos y ventas
tienda.py
"""

import random
from constants import *

class Encargo:
    def __init__(self, id_encargo, descripcion, recursos_necesarios, pago, cliente):
        self.id = id_encargo
        self.descripcion = descripcion
        self.recursos_necesarios = recursos_necesarios  # {(recurso, propietario): cantidad}
        self.pago = pago
        self.cliente = cliente
        
    def mostrar(self):
        """Muestra los detalles del encargo"""
        print(f"\n📋 Encargo #{self.id} - Cliente: {self.cliente}")
        print(f"📝 {self.descripcion}")
        print(f"💰 Pago: ${self.pago}")
        print(f"📦 Recursos necesarios:")
        for (recurso, propietario), cantidad in self.recursos_necesarios.items():
            unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
            prop_texto = f"de {propietario}" if propietario else "de cualquiera"
            print(f"   • {cantidad}{unidad} de {recurso.replace('_', ' ')} {prop_texto}")
        print("-" * 60)

class Tienda:
    def __init__(self, granja):
        self.granja = granja
        self.encargos_disponibles = []
        self.dinero = DINERO_INICIAL  # Dinero inicial
        self.encargos_completados = 0
        self.contador_encargos = 1

        # Generar encargos iniciales
        self._generar_encargos_aleatorios(3)
        
    def _generar_encargos_aleatorios(self, cantidad):
        """Genera encargos aleatorios"""
        tipos_recursos = ["orina", "saliva", "leche", "excrementos", "sudor", "fluido_vaginal", "vomito"]
        clientes = ["Restaurante El Gourmet", "Laboratorio Científico", "Spa Premium",
                   "Coleccionista Privado", "Empresa Farmacéutica", "Chef Experimental"]

        for _ in range(cantidad):
            # Decidir tipo de encargo
            tipo = random.choice(["simple", "mezcla", "especifico"])

            recursos_necesarios = {}

            if tipo == "simple":
                # Un solo recurso de cualquier personaje
                recurso = random.choice(tipos_recursos)
                cantidad_recurso = random.randint(RECURSO_ENCARGO_MINIMO_SIMPLE, RECURSO_ENCARGO_MAXIMO_SIMPLE)
                recursos_necesarios[(recurso, None)] = cantidad_recurso
                descripcion = f"Necesito {cantidad_recurso}ml de {recurso.replace('_', ' ')}"

            elif tipo == "mezcla":
                # Mezcla de 2 recursos
                recurso1, recurso2 = random.sample(tipos_recursos, 2)
                cant1 = random.randint(RECURSO_ENCARGO_MINIMO_MEZCLA, RECURSO_ENCARGO_MAXIMO_MEZCLA)
                cant2 = random.randint(RECURSO_ENCARGO_MINIMO_MEZCLA, RECURSO_ENCARGO_MAXIMO_MEZCLA)
                recursos_necesarios[(recurso1, None)] = cant1
                recursos_necesarios[(recurso2, None)] = cant2
                descripcion = f"Necesito una mezcla de {cant1}ml de {recurso1.replace('_', ' ')} y {cant2}ml de {recurso2.replace('_', ' ')}"

            else:  # especifico
                # Recurso de un personaje específico
                if self.granja.personajes:
                    personaje = random.choice(self.granja.personajes)
                    recurso = random.choice(tipos_recursos)
                    cantidad_recurso = random.randint(RECURSO_ENCARGO_MINIMO_ESPECIFICO, RECURSO_ENCARGO_MAXIMO_ESPECIFICO)
                    recursos_necesarios[(recurso, personaje.nombre)] = cantidad_recurso
                    descripcion = f"Necesito {cantidad_recurso}ml de {recurso.replace('_', ' ')} específicamente de {personaje.nombre}"
                else:
                    # Si no hay personajes, hacer encargo simple
                    recurso = random.choice(tipos_recursos)
                    cantidad_recurso = random.randint(RECURSO_ENCARGO_MINIMO_SIMPLE, RECURSO_ENCARGO_MAXIMO_SIMPLE)
                    recursos_necesarios[(recurso, None)] = cantidad_recurso
                    descripcion = f"Necesito {cantidad_recurso}ml de {recurso.replace('_', ' ')}"

            # Calcular pago basado en cantidad y complejidad
            pago_base = sum(recursos_necesarios.values())
            multiplicador = ENCARGO_PAGO_BASE_MULTIPLICADOR[tipo]
            pago = int(pago_base * multiplicador * random.uniform(ENCARGO_PAGO_VARIACION[0], ENCARGO_PAGO_VARIACION[1]))

            cliente = random.choice(clientes)

            encargo = Encargo(self.contador_encargos, descripcion, recursos_necesarios, pago, cliente)
            self.encargos_disponibles.append(encargo)
            self.contador_encargos += 1
            
    def mostrar_encargos(self):
        """Muestra todos los encargos disponibles"""
        print("\n" + "="*80)
        print("🏪 ENCARGOS DISPONIBLES EN LA TIENDA")
        print("="*80)
        
        if not self.encargos_disponibles:
            print("No hay encargos disponibles en este momento")
            print("\n¡Se generarán nuevos encargos pronto!")
            self._generar_encargos_aleatorios(2)
        else:
            for encargo in self.encargos_disponibles:
                encargo.mostrar()
                
        print("="*80)
        
    def completar_encargo(self, id_encargo):
        """Intenta completar un encargo"""
        encargo = None
        for e in self.encargos_disponibles:
            if e.id == id_encargo:
                encargo = e
                break
                
        if not encargo:
            print(f"❌ No se encontró el encargo #{id_encargo}")
            return False
            
        # Verificar si tenemos todos los recursos
        print(f"\n🔍 Verificando recursos para el encargo #{id_encargo}...")
        recursos_suficientes = True
        faltantes = []
        
        for (recurso, propietario), cantidad_necesaria in encargo.recursos_necesarios.items():
            disponible = self.granja.obtener_cantidad_total_recurso(recurso, propietario)
            if disponible < cantidad_necesaria:
                recursos_suficientes = False
                faltante = cantidad_necesaria - disponible
                unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
                prop_texto = f"de {propietario}" if propietario else ""
                faltantes.append(f"{faltante:.1f}{unidad} de {recurso.replace('_', ' ')} {prop_texto}")
                
        if not recursos_suficientes:
            print(f"\n❌ No tienes suficientes recursos para completar este encargo")
            print(f"Te faltan:")
            for faltante in faltantes:
                print(f"   • {faltante}")
            return False
            
        # Extraer recursos del almacén
        print(f"\n📦 Extrayendo recursos del almacén...")
        for (recurso, propietario), cantidad_necesaria in encargo.recursos_necesarios.items():
            extraido = self.granja.obtener_recurso_almacen(recurso, cantidad_necesaria, propietario)
            unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
            print(f"   ✅ {extraido:.1f}{unidad} de {recurso.replace('_', ' ')}")
            
        # Completar encargo
        self.dinero += encargo.pago
        self.encargos_completados += 1
        self.encargos_disponibles.remove(encargo)
        
        print(f"\n✨ ¡Encargo #{id_encargo} completado!")
        print(f"💰 Has ganado ${encargo.pago}")
        print(f"💰 Dinero total: ${self.dinero}")
        
        # Generar nuevo encargo
        if len(self.encargos_disponibles) < 3:
            self._generar_encargos_aleatorios(1)
            print(f"📋 ¡Nuevo encargo disponible!")
            
        return True
        
    def mostrar_menu(self):
        """Muestra el menú de la tienda"""
        while True:
            print("\n" + "="*80)
            print("🏪 TIENDA DE RECURSOS")
            print("="*80)
            print(f"💰 Dinero disponible: ${self.dinero}")
            print(f"✅ Encargos completados: {self.encargos_completados}")
            print("="*80)
            print("\n1. Ver encargos disponibles")
            print("2. Completar un encargo")
            print("3. Ver almacén de la granja")
            print("4. Volver al menú principal")
            print("="*80)
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == "1":
                self.mostrar_encargos()
                
            elif opcion == "2":
                self.mostrar_encargos()
                if self.encargos_disponibles:
                    try:
                        id_encargo = int(input("\n¿Qué encargo quieres completar? (número): ").strip())
                        self.completar_encargo(id_encargo)
                    except ValueError:
                        print("❌ ID de encargo inválido")
                        
            elif opcion == "3":
                self.granja.mostrar_almacen()
                
            elif opcion == "4":
                break
                
            else:
                print("❌ Opción no válida")
                
            input("\nPresiona Enter para continuar...")