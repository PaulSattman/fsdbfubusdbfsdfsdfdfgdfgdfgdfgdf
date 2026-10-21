# 🏭 Simulador de Granja - Gestión de Recursos

## 📁 Archivos del Proyecto

El juego consta de 5 archivos Python:

1. **main.py** - Programa principal con los menús
2. **personaje.py** - Clase que gestiona cada personaje
3. **granja.py** - Clase que gestiona la granja y almacén
4. **tienda.py** - Clase que gestiona encargos y ventas
5. **encargado.py** - Sistema de automatización con encargados y máquinas

## 🚀 Cómo Ejecutar

1. Asegúrate de tener todos los 5 archivos en la misma carpeta
2. Abre una terminal en esa carpeta
3. Ejecuta: `python main.py`

## 🎮 Cómo Jugar

### Personajes Iniciales
El juego comienza con 3 personajes de Genshin Impact:
- **Amber** (Outrider)
- **Barbara** (Diaconisa)
- **Fischl** (Investigadora)

### Sistema de Estados

Cada personaje tiene 4 estados principales:
- **🍖 Hambre** (0-100%): Aumenta con el tiempo, reducir alimentando
- **💧 Sed** (0-100%): Aumenta con el tiempo, reducir dando agua
- **🧼 Higiene** (0-100%): Disminuye con el tiempo, aumentar limpiando
- **⚡ Energía** (0-100%): Afecta la producción

### Recursos que Generan

Los personajes producen 10 tipos de recursos:
- **Líquidos**: Orina, Saliva, Leche, Fluido Vaginal, Vómito, Sudor (medidos en ml)
- **Sólidos**: Excrementos, Pelo de Cabeza, Pelo de Cuerpo, Pelo Púbico (medidos en g)

### Mecánicas de Producción

- **Orina**: Se genera del agua consumida (30-50% del agua bebida)
- **Excrementos**: Se generan de la comida consumida (15-25% de la comida)
- **Saliva**: Producción constante (5-15ml/hora)
- **Sudor**: Producción constante, mayor si está sucio (3-8ml/hora base)
- **Leche**: Solo si el personaje está bien alimentado (hambre < 40%)
- **Fluido Vaginal**: Producción constante pequeña (2-8ml/hora)
- **Pelos**: Producción aleatoria lenta
- **Vómito**: Probabilidad de ocurrir si está muy sucio o con mucha hambre

### Gestión de la Granja

**Alimentar Personajes**
- Cantidad recomendada: 300-500g de comida
- Reduce el hambre
- Genera materia para excrementos

**Dar Agua**
- Cantidad recomendada: 200-500ml
- Reduce la sed
- Genera materia para orina

**Limpiar**
- Restaura la higiene a 100%
- Reduce el sudor disponible en un 70%

**Recolectar Recursos**
- Mueve los recursos del personaje al almacén
- Los recursos se etiquetan por tipo y propietario
- Necesario para completar encargos

### Sistema de Tiempo

- El juego funciona por horas (empieza a las 8:00)
- Cada hora que avanza:
  - Los personajes generan recursos
  - Aumenta hambre y sed
  - Disminuye higiene
- Puedes avanzar el tiempo manualmente desde el menú

### La Tienda

**Tipos de Encargos**:

1. **Simples**: Un solo recurso de cualquier personaje
   - Ejemplo: "300ml de orina"
   - Pago: Base

2. **Mezclas**: Dos recursos diferentes
   - Ejemplo: "200ml de leche + 150ml de saliva"
   - Pago: +20%

3. **Específicos**: Recurso de un personaje concreto
   - Ejemplo: "250ml de orina de Amber"
   - Pago: +50%

**Completar Encargos**:
- Verifica que tengas los recursos en el almacén
- Los recursos se extraen automáticamente
- Recibes dinero por cada encargo completado
- Se generan nuevos encargos automáticamente

## 🤖 Sistema de Automatización

### Tipos de Encargados/Máquinas

1. **Humano**: Puede realizar cualquier tarea
2. **Máquina de Recolección**: Especializada en recolectar recursos
3. **Máquina de Alimentación**: Especializada en alimentar
4. **Máquina de Limpieza**: Especializada en limpiar

### Programar Tareas

Puedes programar tareas automáticas para cada encargado:
- **Recolectar**: Recolectar todos los recursos o solo recursos específicos
- **Alimentar**: Con cantidad personalizable
- **Dar agua**: Con cantidad personalizable
- **Limpiar**: Restaurar higiene

### Ejecución Automática

- Las tareas se ejecutan cuando avanzas el tiempo
- Puedes ejecutar la automatización manualmente
- Activa/desactiva encargados según necesites
- Programa múltiples tareas por encargado

## 🔞 Interacciones Especiales

### Lamer
Zonas disponibles: cara, pecho, genitales, pies, espalda, axilas
- Genera saliva adicional
- Lamber genitales genera fluido vaginal extra
- Lamer axilas/pies genera sudor extra

### Tocar/Acariciar
Zonas disponibles: cara, pecho, genitales, muslos, espalda, cabello
Intensidades: suave, normal, intenso
- Tocar genera sudor
- Tocar genitales genera fluido vaginal
- Tocar pecho intensamente genera leche
- Acariciar cabello hace que caiga pelo

### Penetrar
Agujeros disponibles: vaginal, anal, oral
Objetos: dedo, juguete_pequeño, juguete_grande, otro, o sin objeto
- **Vaginal**: Genera fluido vaginal y sudor
- **Anal**: Genera sudor, puede estimular evacuación
- **Oral**: Genera saliva, puede provocar vómito si es muy intenso

### Insertar Objetos
- Describe el objeto que quieras usar
- Elige el agujero (vaginal, anal, oral)
- Selecciona el tamaño (pequeño, mediano, grande)
- Genera recursos según el tipo de interacción

**Nota**: Las interacciones reducen la higiene del personaje

## 📊 Consejos de Juego

1. **Alimenta y da agua regularmente** - Los personajes producen más recursos cuando están bien cuidados
2. **Recolecta recursos frecuentemente** - No se acumulan infinitamente
3. **Observa los estados** - Los iconos 🟢🟡🔴 indican prioridades
4. **Planifica los encargos** - Algunos requieren recursos de personajes específicos
5. **Avanza el tiempo** - La producción de recursos requiere tiempo
6. **Mantén la higiene** - Personajes muy sucios pueden vomitar
7. **🆕 Usa la automatización** - Crea encargados para tareas repetitivas
8. **🆕 Interacciones generan recursos extras** - Pero reducen la higiene
9. **🆕 Programa tareas específicas** - Recolecta solo los recursos que necesites

## 🎯 Ejemplo de Sesión de Juego

```
1. Alimentar a los 3 personajes (400g cada uno)
2. Dar agua a los 3 personajes (300ml cada uno)
3. Realizar interacciones especiales (opcional)
4. Crear un encargado automático
5. Programar tareas de recolección automática
6. Avanzar tiempo 2-3 horas (ejecuta automatización)
7. Ir a la tienda y completar encargos
8. Repetir el ciclo
```

## 🤖 Ejemplo de Automatización

```
1. Crear "Recolector-01" (máquina de recolección)
2. Programar:
   - Recolectar orina y leche de Amber
   - Recolectar todos los recursos de Barbara
3. Crear "Alimentador-01" (máquina de alimentación)
4. Programar:
   - Alimentar a todos con 350g
5. Avanzar tiempo → La automatización se ejecuta
``` Ir a la tienda y completar encargos
6. Repetir el ciclo
```

## 💰 Sistema Económico

- Dinero inicial: $1000
- Los encargos pagan según:
  - Cantidad de recursos
  - Complejidad (simple/mezcla/específico)
  - Factor aleatorio (×0.8 a ×1.2)

## ⚠️ Alertas Importantes

- **Hambre/Sed > 70%**: El personaje necesita atención urgente
- **Higiene < 30%**: Riesgo de vómito y menor producción
- **Recursos no recolectados**: Revisa qué personajes tienen recursos disponibles

## 🔄 Actualizaciones Futuras Posibles

- Más personajes de Genshin Impact
- Nuevos tipos de recursos
- Mejoras para la granja
- Sistema de experiencia
- Eventos especiales por hora del día
- Recetas para combinar recursos
- Más tipos de máquinas especializadas
- Sistema de niveles para encargados
- Interacciones más complejas
- Sistema de relaciones entre personajes





Como iniciar: python gui_app.py