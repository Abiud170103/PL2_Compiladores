# 🖥️ Manual de Usuario - Interfaz Gráfica

## Cómo Ejecutar

### Opción 1: Desde el menú principal
```bash
python PL2_U3.py
# Seleccionar opción 5
```

### Opción 2: Directamente
```bash
python interfaz_grafica.py
```

### Opción 3: Archivo batch (Windows)
```bash
# Hacer doble clic en:
ejecutar_GUI.bat
```

## 🎮 Guía de Uso

### Panel Izquierdo - Controles

#### 1. 📝 Entrada Manual
- **Campo de texto**: Escribe tu cadena directamente
- **Botón "Analizar"**: Procesa la cadena introducida
- **Enter**: También ejecuta el análisis

#### 2. 🎯 Simulador Visual
El simulador te permite construir cadenas interactivamente:

| Botón | Símbolo | Función | Restricción |
|-------|---------|---------|-------------|
| 💰 +$ | `$` | Insertar moneda | Ninguna |
| 🥤 R | `R` | Comprar refresco | Saldo ≥ 3 |
| ↩️ < | `<` | Devolver moneda | Saldo ≥ 1 |
| 📦 { } | `{ }` | Bloque anidado | Máx. 3 niveles |
| 🔄 Reset | - | Reiniciar | - |

#### 3. 📋 Ejemplos Predefinidos
- **Lista de ejemplos**: Casos válidos e inválidos
- **Doble clic**: Carga el ejemplo seleccionado
- **Botón "Cargar"**: Alternativa al doble clic

#### 4. 🛠️ Botones de Control
- **🔍 Analizar**: Procesa la cadena actual
- **🗑️ Limpiar**: Borra todos los resultados
- **📖 Ver GDA**: Abre ventana con gramática completa

### Panel Derecho - Resultados

#### 1. 🎯 Resultado del Análisis
- **✅ Verde**: Cadena aceptada semánticamente
- **❌ Rojo**: Cadena rechazada con error específico
- **Información adicional**: Saldo final y refrescos

#### 2. 🌳 Árbol de Derivación Decorado
- **Formato jerárquico**: Indentación por niveles
- **Atributos visibles**: saldo, valido, nivel, refrescos
- **Errores destacados**: [ERROR: descripción]
- **Scroll**: Para árboles grandes

## 🎨 Elementos Visuales

### 🎯 Simulador de Máquina
- **Rectángulo gris**: Cuerpo de la máquina
- **Saldo amarillo**: Monedas disponibles
- **Cadena actual**: Se actualiza en tiempo real
- **Iconos de operaciones**: 💰🥤↩️

### 🎨 Código de Colores
- **🟢 Verde**: Operaciones exitosas
- **🔴 Rojo**: Errores y rechazos
- **🟡 Amarillo**: Saldo y advertencias
- **🟣 Morado**: Gramática y documentación
- **🔵 Azul**: Controles principales

## 🚀 Flujo de Trabajo Recomendado

### Para Principiantes:
1. **Cargar un ejemplo** válido de la lista
2. **Analizar** para ver el resultado esperado
3. **Experimentar** con el simulador visual
4. **Probar modificaciones** manuales

### Para Usuarios Avanzados:
1. **Construir cadenas** directamente en el simulador
2. **Verificar reglas** en tiempo real
3. **Analizar el árbol** decorado detalladamente
4. **Consultar la GDA** cuando sea necesario

## ⚠️ Consejos y Trucos

### 💡 Uso del Simulador
- **Observa el saldo**: Se actualiza en tiempo real
- **Prueba operaciones inválidas**: El simulador te avisará
- **Construye gradualmente**: Paso a paso es más claro

### 🔍 Análisis de Errores
- **Lee el mensaje específico**: Cada error tiene su descripción
- **Verifica el árbol**: Encuentra dónde ocurre el error
- **Compara con ejemplos**: Usa casos válidos como referencia

### 🎯 Experimentación
- **Prueba límites**: Máximo 3 refrescos, 3 niveles
- **Explora combinaciones**: Bloques anidados complejos
- **Verifica independencia**: Saldos entre bloques

## 🐛 Solución de Problemas

### La interfaz no se abre:
1. Verifica que tienes Python instalado
2. Asegúrate de que tkinter esté disponible
3. Ejecuta desde la línea de comandos para ver errores

### Los ejemplos no se cargan:
1. Haz doble clic en la lista
2. O selecciona y presiona "Cargar Ejemplo"
3. Verifica que la selección esté marcada

### El simulador no funciona:
1. Presiona "Reset" para reiniciar
2. Verifica que el saldo sea suficiente
3. Recuerda las restricciones (3 monedas para refresco)

## 📚 Recursos Adicionales

- **README_Practica.md**: Documentación técnica completa
- **PL2_U3.py**: Código fuente con comentarios
- **GDA integrada**: Gramática completa en la interfaz

---

**¡Disfruta explorando el analizador semántico de manera visual e interactiva!** 🎉
