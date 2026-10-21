# 📦 Guía de Instalación - Simulador de Granja

## 🔧 Requisitos del Sistema

- **Python 3.7 o superior**
- No requiere librerías externas (solo usa la biblioteca estándar de Python)

## 📥 Instalación

### Paso 1: Verificar Python

Abre una terminal y ejecuta:

```bash
python --version
```

o

```bash
python3 --version
```

Deberías ver algo como: `Python 3.x.x`

### Paso 2: Descargar los Archivos

Necesitas estos 5 archivos en la misma carpeta:

```
📁 simulador_granja/
   ├── main.py
   ├── personaje.py
   ├── granja.py
   ├── tienda.py
   └── encargado.py
```

### Paso 3: Ejecutar el Juego

Navega a la carpeta donde descargaste los archivos:

```bash
cd ruta/a/simulador_granja
```

Ejecuta el programa principal:

```bash
python main.py
```

o

```bash
python3 main.py
```

## 🧪 Ejecutar la Demo

Si quieres ver una demostración automática primero:

```bash
python demo_prueba.py
```

Esta demo te mostrará todas las funcionalidades del juego en acción.

## 🖥️ Compatibilidad

✅ **Windows**: Funciona perfectamente
✅ **macOS**: Funciona perfectamente  
✅ **Linux**: Funciona perfectamente

## ❓ Solución de Problemas

### Error: "python no se reconoce como comando"

**Solución Windows**: 
- Instala Python desde python.org
- Asegúrate de marcar "Add Python to PATH" durante la instalación

**Solución macOS/Linux**:
- Usa `python3` en lugar de `python`

### Error: "No module named 'xxx'"

**No debería ocurrir** - El juego solo usa librerías estándar de Python:
- `random`: Generación de números aleatorios
- `time`: Manejo de pausas en la demo
- `collections`: Estructura de datos defaultdict

Si ocurre, reinstala Python.

### Error: "ModuleNotFoundError: No module named 'granja'"

**Solución**: Asegúrate de que todos los archivos estén en la misma carpeta y que estés ejecutando desde esa carpeta.

## 🎮 Comandos Útiles

```bash
# Ejecutar el juego
python main.py

# Ejecutar la demo automática
python demo_prueba.py

# Ver ayuda de Python
python --help
```

## 📝 Notas Importantes

1. **No requiere instalación de paquetes adicionales** - Todo está incluido en Python estándar
2. **Multiplataforma** - Funciona en cualquier sistema operativo con Python
3. **Sin dependencias externas** - No necesitas pip install de nada
4. **Interfaz de consola** - El juego se ejecuta completamente en la terminal

## 🚀 Inicio Rápido

```bash
# 1. Asegúrate de tener Python 3.7+
python --version

# 2. Navega a la carpeta del juego
cd simulador_granja

# 3. Ejecuta
python main.py

# 4. ¡Disfruta!
```

## 🔄 Actualizar el Juego

Si modificas el código:
1. Guarda todos los archivos
2. Cierra el juego si está abierto
3. Vuelve a ejecutar `python main.py`

Los cambios se aplicarán inmediatamente.

## 💾 Guardar Progreso

**Nota**: Actualmente el juego NO guarda el progreso al cerrar. 

Si quieres implementar guardado:
- Puedes usar el módulo `pickle` o `json` de Python
- Guarda los objetos `granja` y `tienda` en un archivo
- Carga el archivo al iniciar el juego

## 📞 Soporte

Si tienes problemas:
1. Verifica que todos los archivos estén en la misma carpeta
2. Verifica que tengas Python 3.7 o superior
3. Ejecuta la demo primero para ver si hay errores
4. Revisa los mensajes de error en la consola

¡Listo para jugar! 🎮