class Nodo:
    def __init__(self, tipo, hijos=None, valor=None):
        self.tipo = tipo  # P, C, A, etc.
        self.hijos = hijos if hijos is not None else []
        self.valor = valor  # $, R, <, None, etc.
        # Atributos semánticos
        self.saldo = 0
        self.valido = True
        self.nivel = 1
        self.refrescos = 0
        self.error = None

    def __str__(self, nivel=0):
        indent = '  ' * nivel
        s = f"{indent}{self.tipo} ({self.valor if self.valor else ''}) [saldo={self.saldo}, valido={self.valido}, nivel={self.nivel}, refrescos={self.refrescos}]"
        if self.error:
            s += f" [ERROR: {self.error}]"
        for hijo in self.hijos:
            s += '\n' + hijo.__str__(nivel + 1)
        return s

class Parser:
    def __init__(self, cadena):
        self.cadena = cadena.replace(' ', '')
        self.i = 0
        self.n = len(self.cadena)

    def parse(self):
        nodo = self.P(1)
        if self.i != self.n:
            raise Exception('Cadena no consumida completamente')
        return nodo

    def P(self, nivel):
        if self.i < self.n and self.cadena[self.i] == '{':
            self.i += 1
            c = self.C(nivel)
            if self.i < self.n and self.cadena[self.i] == '}':
                self.i += 1
                return Nodo('P', [c], valor=None)
            else:
                raise Exception('Falta }')
        else:
            raise Exception('Falta {')

    def C(self, nivel):
        hijos = []
        while self.i < self.n and self.cadena[self.i] in ['$', 'R', '<', '{']:
            hijos.append(self.A(nivel))
        return Nodo('C', hijos)

    def A(self, nivel):
        if self.i < self.n:
            c = self.cadena[self.i]
            if c == '$':
                self.i += 1
                return Nodo('A', valor='$')
            elif c == 'R':
                self.i += 1
                return Nodo('A', valor='R')
            elif c == '<':
                self.i += 1
                return Nodo('A', valor='<')
            elif c == '{':
                self.i += 1
                if nivel >= 3:
                    # Exceso de anidamiento
                    subc = self.C(nivel+1)
                    if self.i < self.n and self.cadena[self.i] == '}':
                        self.i += 1
                        nodo = Nodo('A', [subc], valor='{C}')
                        nodo.nivel = nivel+1
                        nodo.valido = False
                        nodo.error = 'Exceso de anidamiento (>3)'
                        return nodo
                    else:
                        raise Exception('Falta } en bloque anidado')
                else:
                    subc = self.C(nivel+1)
                    if self.i < self.n and self.cadena[self.i] == '}':
                        self.i += 1
                        nodo = Nodo('A', [subc], valor='{C}')
                        nodo.nivel = nivel+1
                        return nodo
                    else:
                        raise Exception('Falta } en bloque anidado')
        raise Exception('Símbolo inesperado en A')

def analisis_semantico(nodo, nivel=1):
    """
    Función unificada que realiza el análisis semántico completo.
    Decora el árbol y evalúa las reglas semánticas.
    """
    nodo.nivel = nivel
    
    if nodo.tipo == 'P':
        # P → { C }
        resultado = analisis_semantico(nodo.hijos[0], nivel)
        nodo.saldo = resultado['saldo']
        nodo.valido = resultado['valido']
        nodo.refrescos = resultado['refrescos']
        nodo.error = resultado['error']
        return resultado
        
    elif nodo.tipo == 'C':
        # C → A C | ε
        saldo_local = 0
        refrescos_total = 0
        valido = True
        error = None
        
        for hijo in nodo.hijos:
            if hijo.valor == '$':
                # Insertar moneda
                saldo_local += 1
                hijo.saldo = saldo_local
                hijo.valido = True
                hijo.refrescos = 0
                hijo.nivel = nivel
                
            elif hijo.valor == 'R':
                # Comprar refresco
                if saldo_local >= 3:
                    saldo_local -= 3
                    refrescos_total += 1
                    hijo.saldo = saldo_local
                    hijo.valido = True
                    hijo.refrescos = refrescos_total
                else:
                    valido = False
                    error = 'Saldo insuficiente para refresco'
                    hijo.valido = False
                    hijo.error = error
                hijo.nivel = nivel
                
            elif hijo.valor == '<':
                # Devolver moneda
                if saldo_local >= 1:
                    saldo_local -= 1
                    hijo.saldo = saldo_local
                    hijo.valido = True
                    hijo.refrescos = 0
                else:
                    valido = False
                    error = 'No hay monedas para devolver'
                    hijo.valido = False
                    hijo.error = error
                hijo.nivel = nivel
                
            elif hijo.valor == '{C}':
                # Bloque anidado
                if nivel >= 3:
                    valido = False
                    error = 'Exceso de anidamiento (>3)'
                    hijo.valido = False
                    hijo.error = error
                    hijo.nivel = nivel + 1
                    # Aún así procesamos el bloque interno
                    analisis_semantico(hijo.hijos[0], nivel + 1)
                else:
                    # Procesar bloque con saldo independiente (inicia en 0)
                    resultado_bloque = analisis_semantico(hijo.hijos[0], nivel + 1)
                    hijo.saldo = 0  # Los bloques no transfieren saldo
                    hijo.valido = resultado_bloque['valido']
                    hijo.refrescos = 0  # Los refrescos del bloque no se cuentan afuera
                    hijo.error = resultado_bloque['error']
                    hijo.nivel = nivel + 1
                    
                    if not resultado_bloque['valido']:
                        valido = False
                        error = resultado_bloque['error']
            
            # Si alguna operación falla, el bloque completo falla
            if not valido:
                break
        
        # Verificar límite de refrescos por bloque
        if refrescos_total > 3:
            valido = False
            error = 'Exceso de refrescos en bloque (>3)'
        
        nodo.saldo = saldo_local
        nodo.valido = valido
        nodo.refrescos = refrescos_total
        nodo.error = error
        
        return {
            'saldo': saldo_local,
            'valido': valido,
            'refrescos': refrescos_total,
            'error': error
        }
    
    return {'saldo': 0, 'valido': True, 'refrescos': 0, 'error': None}

def main():
    print('=== ANALIZADOR SEMÁNTICO - MÁQUINA EXPENDEDORA ===')
    print('Introduce la cadena a analizar:')
    entrada = input().strip()
    
    if not entrada:
        print('Error: Cadena vacía')
        return
        
    try:
        parser = Parser(entrada)
        arbol = parser.parse()
        
        # Realizar análisis semántico
        analisis_semantico(arbol)
        
        print('\n=== ÁRBOL DE DERIVACIÓN DECORADO ===')
        print(arbol)
        
        print('\n=== RESULTADO DEL ANÁLISIS ===')
        if arbol.valido:
            print('✅ Cadena ACEPTADA SEMÁNTICAMENTE.')
            print(f'   Saldo final: {arbol.saldo}')
            print(f'   Refrescos comprados: {arbol.refrescos}')
        else:
            print('❌ Cadena RECHAZADA SEMÁNTICAMENTE.')
            print(f'   Error: {arbol.error}')
            
    except Exception as e:
        print(f'❌ Error de análisis sintáctico: {e}')

def test_examples():
    """Función para probar los ejemplos de la práctica"""
    ejemplos = [
        ('{ $ $ $ R }', 'Válido. 3 monedas, 1 refresco. Saldo final = 0'),
        ('{ $ { $ $ $ R } < }', 'Válido. Bloque anidado compra 1 refresco, exterior devuelve 1 moneda'),
        ('{ $ $ $ $ $ $ $ $ $ R R R }', 'Válido. 9 monedas, 3 refrescos (máximo permitido)'),
        ('{ $ R }', 'No válido. Solo 1 moneda, no se puede comprar refresco'),
        ('{ $ { $ $ R } < }', 'No válido. Bloque anidado con saldo insuficiente'),
        ('{ { { { $ $ $ R } } } }', 'No válido. Excede 3 niveles de anidación'),
        ('{ < }', 'No válido. Intenta devolver sin monedas'),
    ]
    
    print('\n=== PROBANDO EJEMPLOS DE LA PRÁCTICA ===')
    for i, (cadena, descripcion) in enumerate(ejemplos, 1):
        print(f'\n--- Ejemplo {i}: {cadena} ---')
        print(f'Descripción: {descripcion}')
        
        try:
            parser = Parser(cadena)
            arbol = parser.parse()
            analisis_semantico(arbol)
            
            if arbol.valido:
                print('✅ ACEPTADA')
            else:
                print(f'❌ RECHAZADA: {arbol.error}')
        except Exception as e:
            print(f'❌ Error sintáctico: {e}')

def test_cadena(cadena):
    """Función para probar una cadena específica y mostrar el árbol decorado"""
    print(f'=== ANALIZANDO: {cadena} ===')
    
    try:
        parser = Parser(cadena)
        arbol = parser.parse()
        
        # Realizar análisis semántico
        analisis_semantico(arbol)
        
        print('\n=== ÁRBOL DE DERIVACIÓN DECORADO ===')
        print(arbol)
        
        print('\n=== RESULTADO DEL ANÁLISIS ===')
        if arbol.valido:
            print('✅ Cadena ACEPTADA SEMÁNTICAMENTE.')
            print(f'   Saldo final: {arbol.saldo}')
            print(f'   Refrescos comprados: {arbol.refrescos}')
        else:
            print('❌ Cadena RECHAZADA SEMÁNTICAMENTE.')
            print(f'   Error: {arbol.error}')
            
    except Exception as e:
        print(f'❌ Error de análisis sintáctico: {e}')

def generar_gda():
    """Generar y mostrar la Gramática Decorada con Atributos (GDA)"""
    print("=== GRAMÁTICA DECORADA CON ATRIBUTOS (GDA) ===")
    print()
    print("GRAMÁTICA BASE:")
    print("P → { C }")
    print("C → A C | ε")
    print("A → $ | R | < | { C }")
    print()
    print("ATRIBUTOS SEMÁNTICOS:")
    print("• saldo (sintetizado): cantidad de monedas disponibles")
    print("• valido (sintetizado): validez semántica del bloque")
    print("• nivel (heredado): profundidad de anidamiento")
    print("• refrescos (sintetizado): número de refrescos comprados")
    print("• error (sintetizado): descripción del error si existe")
    print()
    print("REGLAS SEMÁNTICAS:")
    print()
    print("P → { C }")
    print("  P.saldo = C.saldo")
    print("  P.valido = C.valido")
    print("  P.refrescos = C.refrescos")
    print("  P.error = C.error")
    print("  C.nivel = P.nivel")
    print()
    print("C → A C₁")
    print("  C.saldo = procesar_secuencia(A, C₁)")
    print("  C.valido = A.valido AND C₁.valido")
    print("  C.refrescos = contar_refrescos(A, C₁)")
    print("  A.nivel = C.nivel")
    print("  C₁.nivel = C.nivel")
    print()
    print("C → ε")
    print("  C.saldo = 0")
    print("  C.valido = true")
    print("  C.refrescos = 0")
    print()
    print("A → $")
    print("  A.saldo = saldo_actual + 1")
    print("  A.valido = true")
    print("  A.refrescos = 0")
    print()
    print("A → R")
    print("  if saldo_actual >= 3 then")
    print("    A.saldo = saldo_actual - 3")
    print("    A.valido = true")
    print("    A.refrescos = 1")
    print("  else")
    print("    A.valido = false")
    print("    A.error = 'Saldo insuficiente para refresco'")
    print()
    print("A → <")
    print("  if saldo_actual >= 1 then")
    print("    A.saldo = saldo_actual - 1")
    print("    A.valido = true")
    print("  else")
    print("    A.valido = false")
    print("    A.error = 'No hay monedas para devolver'")
    print()
    print("A → { C }")
    print("  if A.nivel >= 3 then")
    print("    A.valido = false")
    print("    A.error = 'Exceso de anidamiento (>3)'")
    print("  else")
    print("    C.nivel = A.nivel + 1")
    print("    A.saldo = 0  // Los bloques no transfieren saldo")
    print("    A.valido = C.valido")
    print("    A.refrescos = 0  // Los refrescos del bloque no se cuentan")
    print()
    print("RESTRICCIONES ADICIONALES:")
    print("• Máximo 3 refrescos por bloque")
    print("• Máximo 3 niveles de anidamiento")
    print("• Saldo nunca puede ser negativo")
    print("• Cada bloque maneja su propio saldo independiente")

def ejecutar_interfaz_grafica():
    """Ejecutar la interfaz gráfica"""
    try:
        import tkinter as tk
        from interfaz_grafica import MaquinaExpendedoraGUI
        
        print("🖥️  Iniciando interfaz gráfica...")
        root = tk.Tk()
        app = MaquinaExpendedoraGUI(root)
        root.mainloop()
    except ImportError:
        print("❌ Error: tkinter no está disponible. Usa el modo consola.")
    except Exception as e:
        print(f"❌ Error al iniciar interfaz gráfica: {e}")

if __name__ == '__main__':
    print('=== ANALIZADOR SEMÁNTICO - MÁQUINA EXPENDEDORA ===')
    print('Selecciona una opción:')
    print('1. Analizar cadena manual (consola)')
    print('2. Probar ejemplos de la práctica')
    print('3. Mostrar árboles decorados de ejemplos')
    print('4. Mostrar Gramática Decorada con Atributos (GDA)')
    print('5. 🖥️  Interfaz Gráfica (GUI)')
    opcion = input('Opción (1-5): ').strip()
    
    if opcion == '2':
        test_examples()
    elif opcion == '3':
        # Probar algunas cadenas específicas para mostrar el árbol
        cadenas_ejemplo = [
            '{ $ $ $ R }',
            '{ $ { $ $ R } < }',
            '{ < }'
        ]
        for cadena in cadenas_ejemplo:
            test_cadena(cadena)
            print('\n' + '='*50 + '\n')
    elif opcion == '4':
        generar_gda()
    elif opcion == '5':
        ejecutar_interfaz_grafica()
    else:
        main()
