"""
Constantes de Configuración - Simulador de Granja
Este archivo contiene todos los valores configurables para facilitar el balanceamiento del juego.
"""

# === ESTADOS INICIALES ===
HAMBRE_INICIAL = 50           # Valor inicial de hambre
SED_INICIAL = 50              # Valor inicial de sed
HIGIENE_INICIAL = 100         # Valor inicial de higiene
ENERGIA_INICIAL = 100         # Valor inicial de energía

# === FACTORES DE CONVERSIÓN ===
HAMBRE_POR_COMIDA = 10        # Cantidad de comida necesaria para reducir hambre en 1 punto
SED_POR_AGUA = 10             # Cantidad de agua necesaria para reducir sed en 1 punto
LIMPIEZA_SUDOR_RETENCION = 0.3 # Fracción de sudor retenida después de limpiar (0.3 = 30%)

# === ESTADOS DE PERSONAJE ===
HAMBRE_AUMENTO_POR_HORA = (3, 7)      # Incremento mínimo y máximo de hambre por hora
SED_AUMENTO_POR_HORA = (4, 8)         # Incremento mínimo y máximo de sed por hora
HIGIENE_DISMINUCION_POR_HORA = (2, 5) # Disminución mínima y máxima de higiene por hora

# LÍMITES DE ESTADOS (0-100)
ESTADO_MINIMO = 0
ESTADO_MAXIMO = 100

# UMBRALES DE ESTADOS
HAMBRE_BUENO_UMBRAL = 40      # Por debajo de este valor: bien alimentado (verde)
HAMBRE_URGENTE_UMBRAL = 70    # Por encima de este valor: hambre urgente (rojo)
SED_BUENO_UMBRAL = 40         # Por debajo de este valor: bien hidratado (verde)
SED_URGENTE_UMBRAL = 70       # Por encima de este valor: sed urgente (rojo)
HIGIENE_BUENA_UMBRAL = 60     # Por encima de este valor: limpio (verde)
HIGIENE_BAJA_UMBRAL = 30      # Por debajo de este valor: suciedad baja (rojo)

# === GENERACIÓN DE RECURSOS ===
# Orina (basada en agua consumida)
ORINA_FACTOR_CONVERSION = (0.3, 0.5)      # Porcentaje de agua que se convierte en orina
ORINA_PERDIDA_AGUA_FACTOR = 1.0          # Cuánta agua se pierde por unidad de orina producida

# Excrementos (basados en comida consumida)
EXCREMENTOS_FACTOR_CONVERSION = (0.15, 0.25) # Porcentaje de comida que se convierte en excrementos
EXCREMENTOS_PERDIDA_COMIDA_FACTOR = 0.5   # Cuánta comida se pierde por unidad de excrementos producida

# Producción constante
SALIVA_PRODUCCION_HOURLY = (5, 15)        # ml de saliva producidos por hora
SUDOR_BASE_HOURLY = (3, 8)                # ml base de sudor por hora
SUDOR_HIGIENE_UMBRAL = 50                 # Higiene por debajo de este valor aumenta sudor
SUDOR_MULTIPLICADOR_SUCIO = 1.5           # Multiplicador de sudor cuando higiene < SUDOR_HIGIENE_UMBRAL
FLUIDO_VAGINAL_PRODUCCION_HOURLY = (2, 8) # ml de fluido vaginal por hora

# Producción condicional
LECHE_HAMBRE_UMBRAL = 40                  # Hambre por debajo de este valor produce leche
LECHE_PRODUCCION_HOURLY = (50, 150)       # ml de leche producidos por hora cuando condition se cumple

# Producción de pelos (probabilística)
PELO_CABEZA_PROBABILIDAD = 0.3            # 30% de probabilidad por hora
PELO_CABEZA_CANTIDAD = (0.1, 0.5)         # g de pelo de cabeza
PELO_CUERPO_PROBABILIDAD = 0.2            # 20% de probabilidad por hora
PELO_CUERPO_CANTIDAD = (0.05, 0.3)        # g de pelo de cuerpo
PELO_PUBICO_PROBABILIDAD = 0.15           # 15% de probabilidad por hora
PELO_PUBICO_CANTIDAD = (0.05, 0.2)        # g de pelo púbico

# Vómito (condicional)
VOMITO_HAMBRE_UMBRAL = 80                 # Hambre por encima de este valor puede causar vómito
VOMITO_HIGIENE_UMBRAL = 20                # Higiene por debajo de este valor puede causar vómito
VOMITO_PROBABILIDAD = 0.1                 # 10% de probabilidad cuando se cumplen condiciones
VOMITO_CANTIDAD = (50, 200)               # ml de vómito producido

# === INTERACCIONES ESPECIALES ===
# Lamer
LAMER_SALIVA_ADICIONAL = (10, 30)         # ml de saliva adicional por lamer
LAMER_GENITALES_FLUIDO_VAGINAL = (5, 15)  # ml extra de fluido vaginal al lamer genitales
LAMER_ZONAS_SUDOR = ["axilas", "pies"]    # Zonas que generan sudor extra al lamer
LAMER_SUDOR_ADICIONAL = (3, 10)           # ml extra de sudor al lamer axilas/pies

# Tocar/Acariciar
Tocar_INTENSIDADES = {
    "suave": 0.5,
    "normal": 1.0,
    "intenso": 1.5
}
Tocar_SUDOR_BASE = (2, 8)                 # ml base de sudor por tocar
Tocar_GENITALES_FLUIDO_VAGINAL = (8, 20)  # ml extra de fluido vaginal al tocar genitales
Tocar_Pecho_INTENSO_LECHE = (10, 40)      # ml extra de leche al tocar pecho intensamente
Tocar_CABELLO_PELO = (0.1, 0.8)           # g de pelo que cae al acariciar cabello

# Penetrar
Penetrar_INTENSIDAD_FACTOR = {
    None: 1.0,                            # Sin objeto
    "dedo": 0.8,
    "juguete_pequeño": 1.2,
    "juguete_grande": 1.8,
    "otro": 1.5
}
Penetrar_VAGINAL_FLUIDO_VAGINAL = (15, 50) # ml de fluido vaginal
Penetrar_VAGINAL_SUDOR = (5, 15)          # ml de sudor
Penetrar_ANAL_SUDOR = (8, 20)             # ml de sudor
Penetrar_ANAL_EXCREMENTOS_PROBABILIDAD = 0.3 # 30% probabilidad de estimular evacuación
Penetrar_ANAL_EXCREMENTOS_CANTIDAD = (20, 100) # g de excrementos estimulados
Penetrar_ORAL_SALIVA = (20, 60)           # ml de saliva
Penetrar_ORAL_VOMITO_INTENSIDAD_UMBRAL = 1.5 # Factor de intensidad desde el cual puede causar vómito
Penetrar_ORAL_VOMITO_PROBABILIDAD = 0.2   # 20% probabilidad de vómito cuando es intenso
Penetrar_ORAL_VOMITO_CANTIDAD = (30, 150) # ml de vómito producido
Penetrar_HIGIENE_REDUCCION = (5, 15)      # Puntos de higiene perdidos por penetración

# Insertar objetos
InsertarObjeto_TAMANO_FACTOR = {
    "pequeño": 0.7,
    "mediano": 1.0,
    "grande": 1.5
}

# === SISTEMA DE AUTOMATIZACION ===
# Cantidades por defecto para tareas automatizadas
AUTO_ALIMENTAR_CANTIDAD_DEFECTO = 400     # gramos
AUTO_DAR_AGUA_CANTIDAD_DEFECTO = 300      # ml

# === SISTEMA DE ECONOMIA ===
DINERO_INICIAL = 1000                     # Dinero inicial del jugador
ENCARGO_PAGO_BASE_MULTIPLICADOR = {
    "simple": 1.0,
    "mezcla": 1.2,
    "especifico": 1.5
}
ENCARGO_PAGO_VARIACION = (0.8, 1.2)       # Variación aleatoria del pago (80%-120%)

# === TIEMPO ===
HORA_INICIO_JUEGO = 8                     # Hora de inicio del juego (8 AM)
HORAS_EN_DIA = 24                         # Horas en un día completo

# === SISTEMA DE ENCARGOS (TIENDA) ===
RECURSO_ENCARGO_MINIMO_SIMPLE = 100
RECURSO_ENCARGO_MAXIMO_SIMPLE = 500
RECURSO_ENCARGO_MINIMO_MEZCLA = 50
RECURSO_ENCARGO_MAXIMO_MEZCLA = 300
RECURSO_ENCARGO_MINIMO_ESPECIFICO = 100
RECURSO_ENCARGO_MAXIMO_ESPECIFICO = 400

# === SISTEMA DE PENETRACIÓN ===
Penetrar_HIGIENE_REDUCCION = (5, 15)  # Puntos de higiene perdidos por penetración

# === INTERFAZ (para futura GUI) ===
# Colores para barras de progreso (RGB)
COLOR_HAMBRE_BARRA = (255, 69, 0)         # Rojo anaranjado
COLOR_SED_BARRA = (30, 144, 255)          # Azul dodger
COLOR_HIGIENE_BARRA = (50, 205, 50)       # Verde lima
COLOR_ENERGIA_BARRA = (255, 215, 0)       # Oro

# Umbrales para colores de advertencia en barras
COLOR_UMBRAL_ADVERTENCIA = 70             # Por encima de este % cambia a color de alerta
COLOR_UMBRAL_PELIGRO = 85                 # Por encima de este % cambia a color de peligro