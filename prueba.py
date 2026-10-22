"""
Demo Automática del Simulador de Granja
Este script ejecuta una demostración completa del juego
"""

from granja import Granja
from personaje import Personaje
from tienda import Tienda
from encargado import SistemaAutomatizacion
import time

def separador(titulo):
    print("\n" + "="*80)
    print(f"  {titulo}")
    print("="*80)

def pausa(segundos=2):
    """Pausa para visualizar mejor la demo"""
    time.sleep(segundos)

def demo_completa():
    print("\n🎮 DEMO AUTOMÁTICA - SIMULADOR DE GRANJA")
    print("="*80)
    
    # ========== PASO 1: CREAR GRANJA Y PERSONAJES ==========
    separador("PASO 1: INICIALIZACIÓN DE LA GRANJA")
    granja = Granja()
    
    # Crear 3 personajes
    personajes = [
        Personaje("Amber", "Outrider", 18),
        Personaje("Barbara", "Diaconisa", 16),
        Personaje("Fischl", "Investigadora", 16)
    ]
    
    for p in personajes:
        granja.agregar_personaje(p)
        pausa(0.5)
    
    print(f"\n✅ Granja inicializada con {len(granja.personajes)} personajes")
    pausa(2)
    
    # ========== PASO 2: MOSTRAR ESTADO INICIAL ==========
    separador("PASO 2: ESTADO INICIAL DE LOS PERSONAJES")
    granja.mostrar_personajes()
    pausa(3)
    
    # ========== PASO 3: ALIMENTAR A TODOS ==========
    separador("PASO 3: ALIMENTACIÓN Y HIDRATACIÓN")
    
    for p in granja.personajes:
        print(f"\n🍖 Alimentando a {p.nombre}...")
        granja.alimentar_personaje(p.nombre, 400)
        pausa(1)
        
        print(f"\n💧 Dando agua a {p.nombre}...")
        granja.dar_agua_personaje(p.nombre, 350)
        pausa(1)
    
    pausa(2)
    
    # ========== PASO 4: AVANZAR TIEMPO ==========
    separador("PASO 4: AVANCE DEL TIEMPO (3 HORAS)")
    
    for i in range(3):
        granja.avanzar_tiempo()
        print(f"⏰ Hora actual: {granja.hora_actual}:00 - Los personajes están produciendo recursos...")
        pausa(1)
    
    print("\n✅ Han pasado 3 horas. Los personajes han generado recursos.")
    pausa(2)
    
    # ========== PASO 5: MOSTRAR ESTADOS ACTUALIZADOS ==========
    separador("PASO 5: ESTADO DESPUÉS DE 3 HORAS")
    granja.mostrar_personajes()
    pausa(3)
    
    # Mostrar estado detallado de cada personaje
    for p in granja.personajes:
        p.mostrar_estado()
        pausa(2)
    
    # ========== PASO 6: RECOLECTAR RECURSOS ==========
    separador("PASO 6: RECOLECCIÓN DE RECURSOS")
    
    for p in granja.personajes:
        print(f"\n📦 Recolectando recursos de {p.nombre}...")
        granja.recolectar_recursos_personaje(p.nombre)
        pausa(2)
    
    # Mostrar almacén
    granja.mostrar_almacen()
    pausa(3)
    
    # ========== PASO 7: CREAR TIENDA Y VER ENCARGOS ==========
    separador("PASO 7: TIENDA - ENCARGOS DISPONIBLES")
    tienda = Tienda(granja)
    
    print(f"💰 Dinero inicial: ${tienda.dinero}")
    tienda.mostrar_encargos()
    pausa(4)
    
    # ========== PASO 8: INTENTAR COMPLETAR ENCARGOS ==========
    separador("PASO 8: COMPLETANDO ENCARGOS")
    
    # Intentar completar los primeros 2 encargos
    encargos_a_completar = min(2, len(tienda.encargos_disponibles))
    
    for i in range(encargos_a_completar):
        if tienda.encargos_disponibles:
            encargo = tienda.encargos_disponibles[0]
            print(f"\n🎯 Intentando completar encargo #{encargo.id}...")
            pausa(1)
            tienda.completar_encargo(encargo.id)
            pausa(3)
    
    # ========== PASO 9: AVANZAR MÁS TIEMPO ==========
    separador("PASO 9: INTERACCIONES ESPECIALES")
    
    print("\n🔞 Probando interacciones especiales con Amber...")
    pausa(1)
    
    amber = granja.buscar_personaje("Amber")
    
    print("\n1️⃣ Interacción: Lamer genitales")
    resultado = amber.interactuar_lamer("genitales")
    print(resultado)
    pausa(2)
    
    print("\n2️⃣ Interacción: Tocar pecho (intenso)")
    resultado = amber.interactuar_tocar("pecho", "intenso")
    print(resultado)
    pausa(2)
    
    print("\n3️⃣ Interacción: Penetración vaginal")
    resultado = amber.interactuar_penetrar("vaginal", "juguete_pequeño")
    print(resultado)
    pausa(3)
    
    print("\n📊 Estado de Amber después de las interacciones:")
    amber.mostrar_estado()
    pausa(3)
    
    # ========== PASO 10: SISTEMA DE AUTOMATIZACIÓN ==========
    separador("PASO 10: CONFIGURANDO AUTOMATIZACIÓN")
    
    sistema_auto = SistemaAutomatizacion(granja)
    
    print("\n🤖 Creando encargado automático...")
    encargado = sistema_auto.crear_encargado("Robot-01", "maquina_recoleccion")
    print(f"✅ {encargado.nombre} creado")
    pausa(1)
    
    print("\n📋 Programando tareas automáticas...")
    encargado.programar_tarea("Amber", "recolectar", {"recursos": ["orina", "leche"]})
    encargado.programar_tarea("Barbara", "recolectar")
    encargado.programar_tarea("Fischl", "alimentar", {"cantidad": 350})
    pausa(2)
    
    encargado.mostrar_info()
    pausa(3)
    
    # ========== PASO 11: SEGUNDO CICLO ==========
    separador("PASO 11: SEGUNDO CICLO CON AUTOMATIZACIÓN")
    
    # Limpiar a un personaje
    print("\n🧼 Limpiando a Amber...")
    granja.limpiar_personaje("Amber")
    pausa(2)
    
    # Alimentar de nuevo
    print("\n🍖 Alimentando nuevamente a todos...")
    for p in granja.personajes:
        granja.alimentar_personaje(p.nombre, 300)
        granja.dar_agua_personaje(p.nombre, 250)
        pausa(1)
    
    # Avanzar tiempo
    print("\n⏰ Avanzando 2 horas más...")
    for i in range(2):
        granja.avanzar_tiempo()
        print(f"⏰ Hora actual: {granja.hora_actual}:00")
        pausa(1)
    
    # ========== PASO 12: EJECUTAR AUTOMATIZACIÓN ==========
    separador("PASO 12: EJECUTANDO AUTOMATIZACIÓN")
    
    sistema_auto.ejecutar_todos()
    pausa(3)
    
    granja.mostrar_almacen()
    pausa(3)
    
    # Intentar completar más encargos
    print("\n🎯 Intentando completar más encargos...")
    pausa(1)
    
    if tienda.encargos_disponibles:
        encargo = tienda.encargos_disponibles[0]
        tienda.completar_encargo(encargo.id)
        pausa(3)
    
    # ========== PASO 13: ESTADÍSTICAS FINALES ==========
    separador("PASO 13: ESTADÍSTICAS FINALES")
    
    print(f"\n⏰ Hora actual del juego: {granja.hora_actual}:00")
    print(f"💰 Dinero total: ${tienda.dinero}")
    print(f"✅ Encargos completados: {tienda.encargos_completados}")
    print(f"📦 Encargos disponibles: {len(tienda.encargos_disponibles)}")
    print(f"🤖 Encargados/Máquinas: {len(sistema_auto.encargados)}")
    
    print("\n👥 Estado final de los personajes:")
    granja.mostrar_personajes()
    pausa(2)
    
    print("\n📦 Almacén final:")
    granja.mostrar_almacen()
    pausa(3)
    
    # ========== CONCLUSIÓN ==========
    separador("🎉 FIN DE LA DEMOSTRACIÓN")
    
    print("""
✅ Demostración completada exitosamente!

Has visto:
1. Inicialización de la granja con 3 personajes
2. Estados básicos (hambre, sed, higiene)
3. Alimentación e hidratación
4. Sistema de tiempo y producción automática de recursos
5. Recolección de recursos (orina, leche, saliva, sudor, etc.)
6. Almacenamiento por tipo y propietario
7. Sistema de encargos de la tienda
8. Completación de encargos y ganancias económicas
9. 🆕 Interacciones especiales (lamer, tocar, penetrar)
10. 🆕 Sistema de automatización con encargados/máquinas
11. 🆕 Programación de tareas automáticas
12. Ciclo completo de gestión

🎮 ¡Ahora puedes ejecutar main.py para jugar manualmente!
    """)

if __name__ == "__main__":
    demo_completa()
