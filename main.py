"""
Simulador de Granja - Gestión de Recursos
Archivo principal del juego
main.py
"""

from granja import Granja
from personaje import Personaje
from tienda import Tienda
from encargado import SistemaAutomatizacion
from guardado import SistemaGuardado, restaurar_desde_datos
import time

def mostrar_menu_principal():
    print("\n" + "="*60)
    print("🏭 SIMULADOR DE GRANJA - GESTIÓN DE RECURSOS 🏭")
    print("="*60)
    print("1. Gestionar Granja")
    print("2. Ir a la Tienda")
    print("3. Sistema de Automatización")
    print("4. Ver Estadísticas Generales")
    print("5. Avanzar Tiempo (1 hora)")
    print("6. Guardar/Cargar Partida")
    print("7. Salir")
    print("="*60)

def mostrar_menu_granja(granja):
    print("\n" + "="*60)
    print("🐄 GESTIÓN DE GRANJA 🐄")
    print("="*60)
    print("1. Ver todos los personajes")
    print("2. Alimentar personaje")
    print("3. Dar agua a personaje")
    print("4. Limpiar personaje")
    print("5. Recolectar recursos de personaje")
    print("6. Interacciones especiales con personaje")
    print("7. Ver almacén")
    print("8. Volver al menú principal")
    print("="*60)

def crear_nueva_partida():
    """Crea una nueva partida desde cero"""
    # Crear la granja
    granja = Granja()
    
    # Crear personajes iniciales con sus edades correctas
    personajes_iniciales = [

        Personaje("Amber", "Outrider", 18),
        #Personaje("Lisa", "Bibliotecaria", 32),
        Personaje("Barbara", "Diaconisa", 16),
        #Personaje("Xiangling", "Chef", 14),
        #Personaje("Beidou", "Capitana", 27),
        #Personaje("Ningguang", "Tianquan", 25),
        Personaje("Fischl", "Investigadora", 16),
        Personaje("Noelle", "Camarera", 15),
        #Personaje("Sacarosa", "Alquimista", 18),
        #Personaje("Jean", "Gran Maestra", 21),
        Personaje("Qiqi", "Herborista", 8),
        Personaje("Mona", "Astróloga", 19),
        Personaje("Keching", "Yuheng", 17),
        Personaje("Klee", "Caballera", 8),
        Personaje("Diona", "Camarera", 12),
        #Personaje("Xinyan", "Músico", 17),
        Personaje("Ganyu", "Secretaria", 18),
        Personaje("Hu Tao", "Directora", 19),
        #Personaje("Rosaria", "Monja", 24),
        Personaje("Yanfei", "Abogada", 20),
        Personaje("Eula", "Capitana", 25),
        Personaje("Ayaka", "Shirasagi", 19),
        #Personaje("Sayu", "Ninja", 14),
        Personaje("Yoimiya", "Pirotécnica", 19),
        #Personaje("Sara", "General", 25),
        Personaje("Raiden", "Shogun", 29),
        Personaje("Kokomi", "Líder", 17),
        Personaje("Yun Jin", "Actriz", 19),
        #Personaje("Shenhe", "Exorcista", 35),
        Personaje("Yae Miko", "Guuji", 26),
        Personaje("Yelan", "Agente", 30),
        #Personaje("Kuki", "Subjefa", 20),
        Personaje("Collei", "Guardabosques", 14),
        #Personaje("Dori", "Mercader", 15),
        Personaje("Candace", "Guardiana", 24),
        Personaje("Nilou", "Bailarina", 17),
        Personaje("Nahida", "Arconte", 12),
        Personaje("Laila", "Astróloga", 20),
        Personaje("Faruzan", "Profesora", 18),
        Personaje("Yaoyao", "Asistente", 10),
        #Personaje("Dehya", "Mercenaria", 24),
        Personaje("Kirara", "Repartidora", 19),
        Personaje("Lynette", "Asistente", 15),
        Personaje("Charlotte", "Periodista", 18),
        Personaje("Furina", "Actriz", 18),
        Personaje("Navia", "Presidenta", 22),
        #Personaje("Chevreuse", "Oficial", 18),
        Personaje("Xianyun", "Inventora", 30),
        Personaje("Chiori", "Modista", 19),
        #Personaje("Clorinde", "Duelista", 22),
        Personaje("Sigewinne", "Enfermera", 10),
        #Personaje("Emilie", "Perfumista", 26),
        Personaje("Kachina", "Guía", 14),
        Personaje("Mualani", "Guía", 17),
        #Personaje("Xilonen", "Forjadora", 30),
        #Personaje("Chasca", "Pacificadora", 27),
        Personaje("Citlali", "Chamán", 20),
        #Personaje("Mavuika", "Arconte", 38),
        Personaje("Lanyan", "Artista", 18),
        Personaje("Mizuki", "Investigadora", 19),
        #Personaje("Iansan", "Guerrera", 18),
        Personaje("Varesa", "Granjera", 20),
        Personaje("Escoffier", "Chef", 21),
        Personaje("Skirk", "Aventurera", 29),
        Personaje("Ineffa", "Músico", 17),
        Personaje("Aino", "Inventora", 12),
        Personaje("Lauma", "Druida", 36),
        Personaje("Neffer", "Diplomático", 27),
        Personaje("Columbina", "Diosa Lunar", 19),
        Personaje("Linnea", "Profesora", 18)
    ]
    
    for p in personajes_iniciales:
        granja.agregar_personaje(p)
    
    # Crear tienda
    tienda = Tienda(granja)
    
    # Crear sistema de automatización
    sistema_auto = SistemaAutomatizacion(granja)
    
    print("\n¡Bienvenido al Simulador de Granja!")
    print(f"✅ Se han añadido {len(personajes_iniciales)} personajes iniciales")
    
    return granja, tienda, sistema_auto

def main():
    # Sistema de guardado
    sistema_guardado = SistemaGuardado()
    
    # Preguntar si quiere cargar partida
    print("\n" + "="*60)
    print("💾 ¿Quieres cargar una partida guardada? (s/n)")
    print("="*60)
    cargar = input("> ").strip().lower()
    
    if cargar == 's':
        partidas = sistema_guardado.listar_partidas()
        if partidas:
            print("\n📁 Partidas disponibles:")
            for i, partida in enumerate(partidas, 1):
                print(f"   {i}. {partida}")
            
            nombre_partida = input("\nNombre de la partida: ").strip()
            datos, mensaje = sistema_guardado.cargar_partida(nombre_partida)
            
            if datos:
                print(mensaje)
                granja, tienda, sistema_auto = restaurar_desde_datos(datos)
                print(f"✅ Partida cargada exitosamente!")
                print(f"   👥 Personajes: {len(granja.personajes)}")
                print(f"   💰 Dinero: ${tienda.dinero}")
                print(f"   ⏰ Hora: {granja.hora_actual}:00")
            else:
                print(mensaje)
                print("Iniciando nueva partida...")
                granja, tienda, sistema_auto = crear_nueva_partida()
        else:
            print("❌ No hay partidas guardadas. Iniciando nueva partida...")
            granja, tienda, sistema_auto = crear_nueva_partida()
    else:
        granja, tienda, sistema_auto = crear_nueva_partida()
    
    # Bucle principal del juego
    while True:
        mostrar_menu_principal()
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            # Menú de granja
            while True:
                mostrar_menu_granja(granja)
                sub_opcion = input("\nSelecciona una opción: ").strip()
                
                if sub_opcion == "1":
                    granja.mostrar_personajes()
                    
                elif sub_opcion == "2":
                    granja.mostrar_personajes()
                    nombre = input("\n¿A quién quieres alimentar? ").strip()
                    personaje = granja.buscar_personaje(nombre)
                    if personaje:
                        cantidad = input("¿Cuánta comida? (gramos, recomendado 300-500): ").strip()
                        try:
                            granja.alimentar_personaje(nombre, int(cantidad))
                        except ValueError:
                            print("❌ Cantidad inválida")
                    else:
                        print(f"❌ No se encontró a {nombre}")
                        
                elif sub_opcion == "3":
                    granja.mostrar_personajes()
                    nombre = input("\n¿A quién quieres dar agua? ").strip()
                    personaje = granja.buscar_personaje(nombre)
                    if personaje:
                        cantidad = input("¿Cuánta agua? (ml, recomendado 200-500): ").strip()
                        try:
                            granja.dar_agua_personaje(nombre, int(cantidad))
                        except ValueError:
                            print("❌ Cantidad inválida")
                    else:
                        print(f"❌ No se encontró a {nombre}")
                        
                elif sub_opcion == "4":
                    granja.mostrar_personajes()
                    nombre = input("\n¿A quién quieres limpiar? ").strip()
                    granja.limpiar_personaje(nombre)
                    
                elif sub_opcion == "5":
                    granja.mostrar_personajes()
                    nombre = input("\n¿De quién quieres recolectar recursos? ").strip()
                    granja.recolectar_recursos_personaje(nombre)
                    
                elif sub_opcion == "6":
                    granja.mostrar_personajes()
                    nombre = input("\n¿Con quién quieres interactuar? ").strip()
                    granja.interactuar_con_personaje(nombre)
                    
                elif sub_opcion == "7":
                    granja.mostrar_almacen()
                    
                elif sub_opcion == "8":
                    break
                    
                else:
                    print("❌ Opción no válida")
                    
                if sub_opcion != "6":  # Las interacciones ya tienen su propio input
                    input("\nPresiona Enter para continuar...")
                
        elif opcion == "2":
            # Menú de tienda
            tienda.mostrar_menu()
            
        elif opcion == "3":
            # Sistema de automatización
            sistema_auto.menu_automatizacion()
            
        elif opcion == "4":
            # Estadísticas generales
            print("\n" + "="*60)
            print("📊 ESTADÍSTICAS GENERALES 📊")
            print("="*60)
            print(f"⏰ Hora actual: {granja.hora_actual}:00")
            print(f"👥 Personajes en la granja: {len(granja.personajes)}")
            print(f"💰 Dinero: ${tienda.dinero}")
            print(f"📦 Encargos completados: {tienda.encargos_completados}")
            print(f"🤖 Encargados/Máquinas: {len(sistema_auto.encargados)}")
            granja.mostrar_almacen()
            
        elif opcion == "5":
            # Avanzar tiempo
            granja.avanzar_tiempo()
            print(f"\n⏰ Tiempo avanzado. Hora actual: {granja.hora_actual}:00")
            
            # Ejecutar automatización si hay encargados activos
            if sistema_auto.encargados:
                ejecutar_auto = input("\n¿Ejecutar automatización? (s/n): ").strip().lower()
                if ejecutar_auto == 's':
                    sistema_auto.ejecutar_todos()
            
        elif opcion == "6":
            # Sistema de guardado
            accion, nombre = sistema_guardado.menu_guardado(granja, tienda, sistema_auto)
            if accion == 'cargar':
                datos, mensaje = sistema_guardado.cargar_partida(nombre)
                if datos:
                    print(mensaje)
                    confirmacion = input("⚠️ Se perderá el progreso actual. ¿Continuar? (s/n): ").strip().lower()
                    if confirmacion == 's':
                        granja, tienda, sistema_auto = restaurar_desde_datos(datos)
                        print("✅ Partida cargada exitosamente!")
                else:
                    print(mensaje)
            
        elif opcion == "7":
            # Salir
            guardar = input("\n💾 ¿Quieres guardar antes de salir? (s/n): ").strip().lower()
            if guardar == 's':
                nombre = input("Nombre de la partida (Enter para auto): ").strip()
                exito, mensaje = sistema_guardado.guardar_partida(granja, tienda, sistema_auto, nombre if nombre else None)
                print(mensaje)
            print("\n¡Gracias por jugar! 👋")
            break
            
        else:
            print("❌ Opción no válida")
            
        if opcion not in ["1", "2", "3", "6"]:
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()