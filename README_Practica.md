# Práctica 2: Unidad 3- Análisis Semántico: Máquina Expendedora con Bloques Anidados

## Equipo de realización de la práctica:
-sinceridad ante todo profesor, la interfaz grafica fue realizada con ayuda de copilot JAJAJA :D, al igual que algunas de las funciones de prueba
-Peréz Rodriguez Alexis Gael
-Trejo Jiménez Abiud
-5CV3 - Compiladores

## Descripción
Esta práctica implementa un analizador semántico que decora el árbol de derivación de una gramática que modela el funcionamiento de una máquina expendedora de refrescos con bloques anidados.

## Características Implementadas

### ✅ Requisitos Cumplidos

1. **Construcción del árbol de derivación** ✓
2. **Decoración con atributos semánticos** ✓
3. **Validación semántica completa** ✓
4. **Entrada desde consola** ✓
5. **Visualización del árbol decorado** ✓
6. **Gramática Decorada con Atributos (GDA)** ✓
7. **Manejo de todos los casos de error** ✓

### Gramática Base (BNF)
```
P → { C }
C → A C | ε
A → $ | R | < | { C }
```

### Atributos Semánticos
- **saldo** (sintetizado): controla la cantidad de monedas disponibles
- **valido** (sintetizado): indica si el bloque fue ejecutado correctamente
- **nivel** (heredado): profundidad del bloque actual
- **refrescos** (sintetizado): número de refrescos comprados en el bloque
- **error** (sintetizado): descripción del error si existe

### Reglas Semánticas Implementadas

1. **Símbolo $**: Incrementa el saldo del bloque actual en +1
2. **Símbolo R**: Solo válido si saldo ≥ 3. Reduce el saldo en 3
3. **Símbolo <**: Devuelve una moneda (saldo -1) si saldo ≥ 1
4. **Bloques { C }**: Evalúan su propio saldo independiente
5. **Restricciones**:
   - Máximo 3 niveles de anidamiento
   - Máximo 3 refrescos por bloque
   - Saldo nunca negativo

## Uso del Programa

### Ejecutar el analizador:
```bash
python PL2_U3.py
```

### 🖥️ Interfaz Gráfica (GUI):
```bash
python interfaz_grafica.py
# O hacer doble clic en: ejecutar_GUI.bat
```

### Opciones disponibles (Modo Consola):
1. **Analizar cadena manual**: Permite introducir una cadena personalizada
2. **Probar ejemplos de la práctica**: Ejecuta todos los casos de prueba
3. **Mostrar árboles decorados**: Visualiza árboles de ejemplos específicos
4. **Mostrar GDA**: Muestra la Gramática Decorada con Atributos completa
5. **🖥️ Interfaz Gráfica**: Lanza la GUI interactiva

### 🎮 Características de la Interfaz Gráfica:
- **Simulador Visual**: Construye cadenas interactivamente con botones
- **Análisis en Tiempo Real**: Ve el resultado inmediatamente
- **Ejemplos Predefinidos**: Carga ejemplos con doble clic
- **Visualización del Árbol**: Árbol decorado con colores y formato
- **GDA Integrada**: Ventana con la gramática completa
- **Interfaz Intuitiva**: Fácil de usar con iconos y colores

## 🖥️ Interfaz Gráfica

### Características Principales:
1. **Panel de Entrada**: Campo para introducir cadenas manualmente
2. **Simulador Visual**: Construye cadenas usando botones interactivos
   - 💰 `$`: Insertar moneda
   - 🥤 `R`: Comprar refresco
   - ↩️ `<`: Devolver moneda
   - 📦 `{}`: Agregar bloque anidado
3. **Ejemplos Predefinidos**: Lista de ejemplos con descripciones
4. **Panel de Resultados**: Muestra el árbol decorado y el resultado
5. **Gramática GDA**: Ventana separada con la gramática completa

### Componentes Visuales:
- **Simulador de Máquina**: Representación visual con saldo actual
- **Árbol Sintáctico**: Visualización con colores y formato
- **Indicadores de Estado**: Íconos y colores para resultados
- **Controles Intuitivos**: Botones grandes con emojis descriptivos

### Ventajas de la GUI:
- ✅ **Facilidad de uso**: No requiere conocimiento de sintaxis
- ✅ **Visualización clara**: Colores y formato para mejor comprensión
- ✅ **Experimentación**: Prueba rápida de diferentes combinaciones
- ✅ **Educativo**: Ideal para aprender las reglas semánticas

## Ejemplos de Prueba

### Cadenas Válidas:
- `{ $ $ $ R }` → 3 monedas, 1 refresco. Saldo final = 0
- `{ $ { $ $ $ R } < }` → Bloque anidado válido + devolución
- `{ $ $ $ $ $ $ $ $ $ R R R }` → 9 monedas, 3 refrescos (máximo permitido)

### Cadenas Inválidas:
- `{ $ R }` → Saldo insuficiente para refresco
- `{ $ { $ $ R } < }` → Bloque anidado con saldo insuficiente
- `{ { { { $ $ $ R } } } }` → Exceso de anidamiento (>3 niveles)
- `{ < }` → Intento de devolución sin monedas

## Salida del Programa

### Árbol Decorado Ejemplo:
```
P () [saldo=0, valido=True, nivel=1, refrescos=1]
  C () [saldo=0, valido=True, nivel=1, refrescos=1]
    A ($) [saldo=1, valido=True, nivel=1, refrescos=0]
    A ($) [saldo=2, valido=True, nivel=1, refrescos=0]
    A ($) [saldo=3, valido=True, nivel=1, refrescos=0]
    A (R) [saldo=0, valido=True, nivel=1, refrescos=1]
```

### Resultado del Análisis:
```
✅ Cadena ACEPTADA SEMÁNTICAMENTE.
   Saldo final: 0
   Refrescos comprados: 1
```

## Estructura del Código

### Clases Principales:
- **Nodo**: Representa nodos del árbol con atributos semánticos
- **Parser**: Analizador sintáctico recursivo descendente

### Funciones Principales:
- **analisis_semantico()**: Función unificada para análisis semántico
- **test_examples()**: Prueba todos los casos de la práctica
- **test_cadena()**: Analiza una cadena específica mostrando el árbol
- **generar_gda()**: Muestra la Gramática Decorada con Atributos

## Validaciones Implementadas

1. **Saldo suficiente**: Verifica que haya monedas para operaciones
2. **Límite de anidamiento**: Máximo 3 niveles permitidos
3. **Límite de refrescos**: Máximo 3 refrescos por bloque
4. **Saldo no negativo**: Previene saldos negativos en cualquier momento
5. **Independencia de bloques**: Cada bloque maneja su propio saldo

## Manejo de Errores

El programa detecta y reporta los siguientes errores semánticos:
- "Saldo insuficiente para refresco"
- "No hay monedas para devolver"
- "Exceso de anidamiento (>3)"
- "Exceso de refrescos en bloque (>3)"


### 🎯 Funcionalidades Extra:
- Simulador visual interactivo
- Ejemplos predefinidos integrados
- Múltiples modos de ejecución
- Documentación completa
- Archivos de inicio (.bat)
- Interfaz intuitiva con emojis y colores