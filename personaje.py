"""
Clase Personaje - Gestión de personajes individuales
personaje.py
"""

import random
from constants import *

class Personaje:
    def __init__(self, nombre, tipo, edad):
        self.nombre = nombre
        self.tipo = tipo
        self.edad = edad
        
        # Estados básicos (0-100)
        self.hambre = HAMBRE_INICIAL  # A mayor valor, más hambre
        self.sed = SED_INICIAL
        self.higiene = HIGIENE_INICIAL  # A mayor valor, más limpio
        self.energia = ENERGIA_INICIAL
        
        # Producción de recursos (ml o gramos)
        self.recursos_disponibles = {
            "orina": 0,
            "vomito": 0,
            "saliva": 0,
            "excrementos": 0,
            "leche": 0,
            "sudor": 0,
            "fluido_vaginal": 0,
            "pelo_cabeza": 0,
            "pelo_cuerpo": 0,
            "pelo_pubico": 0
        }
        
        # Alimentación acumulada
        self.comida_consumida = 0
        self.agua_consumida = 0
        
    def actualizar_estados(self):
        """Actualiza los estados del personaje cada hora"""
        # Aumentar hambre y sed
        self.hambre = min(ESTADO_MAXIMO, self.hambre + random.randint(HAMBRE_AUMENTO_POR_HORA[0], HAMBRE_AUMENTO_POR_HORA[1]))
        self.sed = min(ESTADO_MAXIMO, self.sed + random.randint(SED_AUMENTO_POR_HORA[0], SED_AUMENTO_POR_HORA[1]))

        # Disminuir higiene
        self.higiene = max(ESTADO_MINIMO, self.higiene - random.randint(HIGIENE_DISMINUCION_POR_HORA[0], HIGIENE_DISMINUCION_POR_HORA[1]))
        
        # Producción de recursos basada en consumo
        self._generar_recursos()
        
    def _generar_recursos(self):
        """Genera recursos basados en el estado del personaje"""
        # Orina (basada en agua consumida)
        if self.agua_consumida > 0:
            orina = self.agua_consumida * random.uniform(ORINA_FACTOR_CONVERSION[0], ORINA_FACTOR_CONVERSION[1])
            self.recursos_disponibles["orina"] += orina
            self.agua_consumida = max(0, self.agua_consumida - orina * ORINA_PERDIDA_AGUA_FACTOR)
            
        # Excrementos (basados en comida consumida)
        if self.comida_consumida > 0:
            excrementos = self.comida_consumida * random.uniform(EXCREMENTOS_FACTOR_CONVERSION[0], EXCREMENTOS_FACTOR_CONVERSION[1])
            self.recursos_disponibles["excrementos"] += excrementos
            self.comida_consumida = max(0, self.comida_consumida - excrementos * EXCREMENTOS_PERDIDA_COMIDA_FACTOR)
            
        # Saliva (producción constante)
        self.recursos_disponibles["saliva"] += random.uniform(SALIVA_PRODUCCION_HOURLY[0], SALIVA_PRODUCCION_HOURLY[1])
        
        # Sudor (más si está sucio)
        sudor_base = random.uniform(SUDOR_BASE_HOURLY[0], SUDOR_BASE_HOURLY[1])
        if self.higiene < SUDOR_HIGIENE_UMBRAL:
            sudor_base *= SUDOR_MULTIPLICADOR_SUCIO
        self.recursos_disponibles["sudor"] += sudor_base
        
        # Leche (si está bien alimentado)
        if self.hambre < LECHE_HAMBRE_UMBRAL:
            self.recursos_disponibles["leche"] += random.uniform(LECHE_PRODUCCION_HOURLY[0], LECHE_PRODUCCION_HOURLY[1])
            
        # Fluido vaginal (producción constante pequeña)
        self.recursos_disponibles["fluido_vaginal"] += random.uniform(FLUIDO_VAGINAL_PRODUCCION_HOURLY[0], FLUIDO_VAGINAL_PRODUCCION_HOURLY[1])
        
        # Pelos (producción lenta)
        if random.random() < PELO_CABEZA_PROBABILIDAD:
            self.recursos_disponibles["pelo_cabeza"] += random.uniform(PELO_CABEZA_CANTIDAD[0], PELO_CABEZA_CANTIDAD[1])
        if random.random() < PELO_CUERPO_PROBABILIDAD:
            self.recursos_disponibles["pelo_cuerpo"] += random.uniform(PELO_CUERPO_CANTIDAD[0], PELO_CUERPO_CANTIDAD[1])
        if random.random() < PELO_PUBICO_PROBABILIDAD:
            self.recursos_disponibles["pelo_pubico"] += random.uniform(PELO_PUBICO_CANTIDAD[0], PELO_PUBICO_CANTIDAD[1])
            
        # Vómito (si come demasiado o está muy sucio)
        if self.hambre > VOMITO_HAMBRE_UMBRAL or self.higiene < VOMITO_HIGIENE_UMBRAL:
            if random.random() < VOMITO_PROBABILIDAD:  # 10% probabilidad
                vomito = random.uniform(VOMITO_CANTIDAD[0], VOMITO_CANTIDAD[1])
                self.recursos_disponibles["vomito"] += vomito
                
    def alimentar(self, cantidad):
        """Alimenta al personaje (cantidad en gramos)"""
        self.hambre = max(0, self.hambre - cantidad / HAMBRE_POR_COMIDA)
        self.comida_consumida += cantidad
        return f"✅ {self.nombre} ha comido {cantidad}g de comida"

    def dar_agua(self, cantidad):
        """Da agua al personaje (cantidad en ml)"""
        self.sed = max(0, self.sed - cantidad / SED_POR_AGUA)
        self.agua_consumida += cantidad
        return f"✅ {self.nombre} ha bebido {cantidad}ml de agua"
        
    def limpiar(self):
        """Limpia al personaje"""
        self.higiene = ESTADO_MAXIMO
        # Al limpiar se pierde algo de sudor disponible
        self.recursos_disponibles["sudor"] *= LIMPIEZA_SUDOR_RETENCION
        return f"✅ {self.nombre} ha sido limpiado"
        
    def recolectar_recursos(self):
        """Recolecta todos los recursos disponibles"""
        recursos_recolectados = {}
        for recurso, cantidad in self.recursos_disponibles.items():
            if cantidad > 0:
                recursos_recolectados[recurso] = cantidad
                self.recursos_disponibles[recurso] = 0
        return recursos_recolectados
        
    def mostrar_estado(self):
        """Muestra el estado actual del personaje"""
        print(f"\n{'='*50}")
        print(f"👤 {self.nombre} ({self.tipo}) - {self.edad} años")
        print(f"{'='*50}")
        print(f"🍖 Hambre: {self.hambre:.1f}% {'❗' if self.hambre > HAMBRE_URGENTE_UMBRAL else ''}")
        print(f"💧 Sed: {self.sed:.1f}% {'❗' if self.sed > SED_URGENTE_UMBRAL else ''}")
        print(f"🧼 Higiene: {self.higiene:.1f}% {'❗' if self.higiene < HIGIENE_BAJA_UMBRAL else ''}")
        print(f"⚡ Energía: {self.energia:.1f}%")
        print(f"\n📦 Recursos disponibles para recolectar:")
        
        for recurso, cantidad in self.recursos_disponibles.items():
            if cantidad > 1:
                unidad = "ml" if recurso in ["orina", "saliva", "leche", "fluido_vaginal", "vomito", "sudor"] else "g"
                print(f"   • {recurso.replace('_', ' ').title()}: {cantidad:.1f}{unidad}")
        print(f"{'='*50}")
        
    def obtener_recursos_totales(self):
        """Devuelve la suma total de recursos disponibles"""
        return sum(self.recursos_disponibles.values())
    
    def interactuar_lamer(self, zona):
        """
        Interacción: lamer al personaje
        zona: 'cara', 'pecho', 'genitales', 'pies', 'espalda', 'axilas'
        """
        zonas_validas = ['cara', 'pecho', 'genitales', 'pies', 'espalda', 'axilas']
        
        if zona not in zonas_validas:
            return f"❌ Zona no válida. Opciones: {', '.join(zonas_validas)}"
        
        # Generar saliva adicional por estimulación
        saliva_generada = random.uniform(LAMER_SALIVA_ADICIONAL[0], LAMER_SALIVA_ADICIONAL[1])
        self.recursos_disponibles["saliva"] += saliva_generada

        # Si se lame zona genital, genera fluido vaginal
        if zona == "genitales":
            fluido_generado = random.uniform(LAMER_GENITALES_FLUIDO_VAGINAL[0], LAMER_GENITALES_FLUIDO_VAGINAL[1])
            self.recursos_disponibles["fluido_vaginal"] += fluido_generado
            return f"👅 Has lamido los genitales de {self.nombre}. Generó {saliva_generada:.1f}ml de saliva y {fluido_generado:.1f}ml de fluido vaginal"

        # Si se lame axilas o pies, genera sudor
        if zona in LAMER_ZONAS_SUDOR:
            sudor_generado = random.uniform(LAMER_SUDOR_ADICIONAL[0], LAMER_SUDOR_ADICIONAL[1])
            self.recursos_disponibles["sudor"] += sudor_generado
            return f"👅 Has lamido las {zona} de {self.nombre}. Generó {saliva_generada:.1f}ml de saliva y {sudor_generado:.1f}ml de sudor"

        return f"👅 Has lamido {zona} de {self.nombre}. Generó {saliva_generada:.1f}ml de saliva"
    
    def interactuar_tocar(self, zona, intensidad='normal'):
        """
        Interacción: tocar/acariciar al personaje
        zona: 'cara', 'pecho', 'genitales', 'muslos', 'espalda', 'cabello'
        intensidad: 'suave', 'normal', 'intenso'
        """
        zonas_validas = ['cara', 'pecho', 'genitales', 'muslos', 'espalda', 'cabello']
        
        if zona not in zonas_validas:
            return f"❌ Zona no válida. Opciones: {', '.join(zonas_validas)}"
        
        multiplicador = Tocar_INTENSIDADES.get(intensidad, 1.0)

        # Tocar genera sudor
        sudor_generado = random.uniform(Tocar_SUDOR_BASE[0], Tocar_SUDOR_BASE[1]) * multiplicador
        self.recursos_disponibles["sudor"] += sudor_generado

        # Si tocas genitales, genera fluido vaginal
        if zona == "genitales":
            fluido_generado = random.uniform(Tocar_GENITALES_FLUIDO_VAGINAL[0], Tocar_GENITALES_FLUIDO_VAGINAL[1]) * multiplicador
            self.recursos_disponibles["fluido_vaginal"] += fluido_generado
            return f"🤚 Has tocado los genitales de {self.nombre} ({intensidad}). Generó {sudor_generado:.1f}ml de sudor y {fluido_generado:.1f}ml de fluido vaginal"

        # Si tocas pecho intensamente
        if zona == "pecho" and intensidad == 'intenso':
            leche_generada = random.uniform(Tocar_Pecho_INTENSO_LECHE[0], Tocar_Pecho_INTENSO_LECHE[1])
            self.recursos_disponibles["leche"] += leche_generada
            return f"🤚 Has tocado el pecho de {self.nombre} intensamente. Generó {sudor_generado:.1f}ml de sudor y {leche_generada:.1f}ml de leche"

        # Si tocas cabello, puede caerse pelo
        if zona == "cabello":
            pelo_caido = random.uniform(Tocar_CABELLO_PELO[0], Tocar_CABELLO_PELO[1])
            self.recursos_disponibles["pelo_cabeza"] += pelo_caido
            return f"🤚 Has acariciado el cabello de {self.nombre}. Generó {sudor_generado:.1f}ml de sudor y cayó {pelo_caido:.2f}g de pelo"

        return f"🤚 Has tocado {zona} de {self.nombre} ({intensidad}). Generó {sudor_generado:.1f}ml de sudor"
    
    def interactuar_penetrar(self, agujero, objeto=None):
        """
        Interacción: penetrar al personaje
        agujero: 'vaginal', 'anal', 'oral'
        objeto: None (sin objeto), 'dedo', 'juguete_pequeño', 'juguete_grande', 'otro'
        """
        agujeros_validos = ['vaginal', 'anal', 'oral']
        
        if agujero not in agujeros_validos:
            return f"❌ Agujero no válido. Opciones: {', '.join(agujeros_validos)}"
        
        objeto_texto = objeto if objeto else "natural"
        intensidad_factor = Penetrar_INTENSIDAD_FACTOR.get(objeto, 1.0)
        
        resultados = []
        
        if agujero == "vaginal":
            fluido_generado = random.uniform(Penetrar_VAGINAL_FLUIDO_VAGINAL[0], Penetrar_VAGINAL_FLUIDO_VAGINAL[1]) * intensidad_factor
            self.recursos_disponibles["fluido_vaginal"] += fluido_generado
            sudor_generado = random.uniform(Penetrar_VAGINAL_SUDOR[0], Penetrar_VAGINAL_SUDOR[1]) * intensidad_factor
            self.recursos_disponibles["sudor"] += sudor_generado
            resultados.append(f"🔞 Penetración vaginal de {self.nombre} ({objeto_texto})")
            resultados.append(f"   💧 Generó {fluido_generado:.1f}ml de fluido vaginal")
            resultados.append(f"   💦 Generó {sudor_generado:.1f}ml de sudor")
            
        elif agujero == "anal":
            sudor_generado = random.uniform(Penetrar_ANAL_SUDOR[0], Penetrar_ANAL_SUDOR[1]) * intensidad_factor
            self.recursos_disponibles["sudor"] += sudor_generado
            # Puede estimular evacuación
            if random.random() < Penetrar_ANAL_EXCREMENTOS_PROBABILIDAD:
                excremento_generado = random.uniform(Penetrar_ANAL_EXCREMENTOS_CANTIDAD[0], Penetrar_ANAL_EXCREMENTOS_CANTIDAD[1])
                self.recursos_disponibles["excrementos"] += excremento_generado
                resultados.append(f"🔞 Penetración anal de {self.nombre} ({objeto_texto})")
                resultados.append(f"   💦 Generó {sudor_generado:.1f}ml de sudor")
                resultados.append(f"   💩 Estimuló {excremento_generado:.1f}g de excrementos")
            else:
                resultados.append(f"🔞 Penetración anal de {self.nombre} ({objeto_texto})")
                resultados.append(f"   💦 Generó {sudor_generado:.1f}ml de sudor")
                
        elif agujero == "oral":
            saliva_generada = random.uniform(Penetrar_ORAL_SALIVA[0], Penetrar_ORAL_SALIVA[1]) * intensidad_factor
            self.recursos_disponibles["saliva"] += saliva_generada
            resultados.append(f"🔞 Penetración oral de {self.nombre} ({objeto_texto})")
            resultados.append(f"   💧 Generó {saliva_generada:.1f}ml de saliva")
            # Puede provocar vómito si es intenso
            if intensidad_factor > Penetrar_ORAL_VOMITO_INTENSIDAD_UMBRAL and random.random() < Penetrar_ORAL_VOMITO_PROBABILIDAD:
                vomito_generado = random.uniform(Penetrar_ORAL_VOMITO_CANTIDAD[0], Penetrar_ORAL_VOMITO_CANTIDAD[1])
                self.recursos_disponibles["vomito"] += vomito_generado
                resultados.append(f"   🤮 Provocó {vomito_generado:.1f}ml de vómito (muy intenso)")
        
        # Reduce un poco la higiene
        self.higiene = max(0, self.higiene - random.randint(Penetrar_HIGIENE_REDUCCION[0], Penetrar_HIGIENE_REDUCCION[1]))
        
        return "\n".join(resultados)
    
    def insertar_objeto(self, agujero, objeto_descripcion, tamano='mediano'):
        """
        Insertar objetos en el personaje
        agujero: 'vaginal', 'anal', 'oral'
        objeto_descripcion: descripción del objeto
        tamano: 'pequeño', 'mediano', 'grande'
        """
        agujeros_validos = ['vaginal', 'anal', 'oral']
        
        if agujero not in agujeros_validos:
            return f"❌ Agujero no válido. Opciones: {', '.join(agujeros_validos)}"
        
        factor_tamano = InsertarObjeto_TAMANO_FACTOR.get(tamano, 1.0)
        
        # Similar a penetrar pero con descripción del objeto
        return self.interactuar_penetrar(agujero, f"{objeto_descripcion} ({tamano})")
    

    def interactuar_directo(self, personaje, zona):
        """Interacción directa con el personaje consumiendo el recurso directamente"""
        if zona == "genitales":
            orina = personaje.recursos_disponibles.get("orina", 0)
            if orina > 0:
                personaje.recursos_disponibles["orina"] = 0
                return f"💦 Has bebido {orina:.1f}ml de orina directamente de los genitales de {personaje.nombre}"
            return "❌ No hay orina disponible en los genitales de este personaje"
        elif zona == "ano":
            excrementos = personaje.recursos_disponibles.get("excrementos", 0)
            if excrementos > 0:
                personaje.recursos_disponibles["excrementos"] = 0
                return f"💩 Has comido {excrementos:.1f}g de excrementos directamente del ano de {personaje.nombre}"
            return "❌ No hay excrementos disponibles en el ano de este personaje"
        elif zona == "boca":
            saliva = personaje.recursos_disponibles.get("saliva", 0)
            if saliva > 0:
                personaje.recursos_disponibles["saliva"] = 0
                return f"💧 Has besado a {personaje.nombre} y tragaste {saliva:.1f}ml de saliva"
            return "❌ No hay saliva disponible en la boca de este personaje"
        elif zona == "axilas":
            sudor = personaje.recursos_disponibles.get("sudor", 0)
            if sudor > 0:
                personaje.recursos_disponibles["sudor"] = 0
                return f"💦 Lamiste las axilas de {personaje.nombre} y bebiste {sudor:.1f}ml de sudor"
            return "❌ No hay sudor disponible en las axilas de este personaje"
        else:
            return "❌ Zona no válida"