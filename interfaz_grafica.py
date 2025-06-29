import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PL2_U3 import Parser, analisis_semantico
import threading

class MaquinaExpendedoraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Semántico - Máquina Expendedora")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.cadena_actual = tk.StringVar()
        self.resultado_var = tk.StringVar()
        
        self.setup_ui()
        self.cargar_ejemplos()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🥤 ANALIZADOR SEMÁNTICO - MÁQUINA EXPENDEDORA 🥤", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=15)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Panel izquierdo - Entrada y controles
        left_panel = tk.LabelFrame(main_frame, text="Entrada y Controles", 
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Entrada de cadena
        input_frame = tk.Frame(left_panel, bg='#f0f0f0')
        input_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(input_frame, text="Cadena a analizar:", 
                font=('Arial', 11, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        self.entry_cadena = tk.Entry(input_frame, textvariable=self.cadena_actual, 
                                    font=('Courier', 12), width=40)
        self.entry_cadena.pack(fill='x', pady=5)
        self.entry_cadena.bind('<Return>', lambda e: self.analizar_cadena())
        
        # Botones principales
        button_frame = tk.Frame(left_panel, bg='#f0f0f0')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        self.btn_analizar = tk.Button(button_frame, text="🔍 Analizar", 
                                     command=self.analizar_cadena,
                                     bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                                     relief='raised', bd=2)
        self.btn_analizar.pack(side='left', padx=(0, 5), pady=5)
        
        self.btn_limpiar = tk.Button(button_frame, text="🗑️ Limpiar", 
                                    command=self.limpiar_resultados,
                                    bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                                    relief='raised', bd=2)
        self.btn_limpiar.pack(side='left', padx=5, pady=5)
        
        self.btn_gda = tk.Button(button_frame, text="📖 Ver GDA", 
                                command=self.mostrar_gda,
                                bg='#9b59b6', fg='white', font=('Arial', 11, 'bold'),
                                relief='raised', bd=2)
        self.btn_gda.pack(side='left', padx=5, pady=5)
        
        # Simulador visual
        self.setup_simulador(left_panel)
        
        # Ejemplos predefinidos
        self.setup_ejemplos(left_panel)
        
        # Panel derecho - Resultados
        right_panel = tk.LabelFrame(main_frame, text="Resultados del Análisis", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Resultado del análisis
        result_frame = tk.Frame(right_panel, bg='#f0f0f0')
        result_frame.pack(fill='x', padx=10, pady=10)
        
        self.result_label = tk.Label(result_frame, text="Resultado: Esperando análisis...", 
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.result_label.pack(anchor='w')
        
        # Árbol de derivación
        tree_frame = tk.Frame(right_panel, bg='#f0f0f0')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        tk.Label(tree_frame, text="Árbol de Derivación Decorado:", 
                font=('Arial', 11, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        self.tree_text = scrolledtext.ScrolledText(tree_frame, font=('Courier', 10), 
                                                  height=20, bg='#2c3e50', fg='#ecf0f1',
                                                  insertbackground='white')
        self.tree_text.pack(fill='both', expand=True, pady=5)
        
    def setup_simulador(self, parent):
        """Configurar el simulador visual de la máquina"""
        sim_frame = tk.LabelFrame(parent, text="Simulador Visual", 
                                 font=('Arial', 11, 'bold'), bg='#f0f0f0')
        sim_frame.pack(fill='x', padx=10, pady=10)
        
        # Canvas para la simulación
        self.canvas = tk.Canvas(sim_frame, height=150, bg='#34495e', relief='sunken', bd=2)
        self.canvas.pack(fill='x', padx=5, pady=5)
        
        # Controles del simulador
        sim_controls = tk.Frame(sim_frame, bg='#f0f0f0')
        sim_controls.pack(fill='x', padx=5, pady=5)
        
        tk.Button(sim_controls, text="💰 +$", command=lambda: self.simular_accion('$'),
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
        tk.Button(sim_controls, text="🥤 R", command=lambda: self.simular_accion('R'),
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
        tk.Button(sim_controls, text="↩️ <", command=lambda: self.simular_accion('<'),
                 bg='#e67e22', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
        tk.Button(sim_controls, text="📦 { }", command=lambda: self.simular_accion('{}'),
                 bg='#8e44ad', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=2)
        
        tk.Button(sim_controls, text="🔄 Reset", command=self.reset_simulador,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='right', padx=2)
        
        # Estado del simulador
        self.saldo_sim = 0
        self.cadena_sim = "{ "
        self.actualizar_simulador()
        
    def setup_ejemplos(self, parent):
        """Configurar la sección de ejemplos"""
        ejemplos_frame = tk.LabelFrame(parent, text="Ejemplos Predefinidos", 
                                      font=('Arial', 11, 'bold'), bg='#f0f0f0')
        ejemplos_frame.pack(fill='x', padx=10, pady=10)
        
        # Lista de ejemplos
        self.ejemplos_listbox = tk.Listbox(ejemplos_frame, height=6, font=('Courier', 10))
        self.ejemplos_listbox.pack(fill='x', padx=5, pady=5)
        self.ejemplos_listbox.bind('<Double-Button-1>', self.cargar_ejemplo_seleccionado)
        
        # Botón para cargar ejemplo
        tk.Button(ejemplos_frame, text="📋 Cargar Ejemplo Seleccionado", 
                 command=self.cargar_ejemplo_seleccionado,
                 bg='#16a085', fg='white', font=('Arial', 10, 'bold')).pack(pady=5)
        
    def cargar_ejemplos(self):
        """Cargar ejemplos en la lista"""
        ejemplos = [
            "{ $ $ $ R } - Válido: 3 monedas, 1 refresco",
            "{ $ { $ $ $ R } < } - Válido: Bloque anidado + devolución",
            "{ $ $ $ $ $ $ $ $ $ R R R } - Válido: 9 monedas, 3 refrescos",
            "{ $ R } - Inválido: Saldo insuficiente",
            "{ $ { $ $ R } < } - Inválido: Bloque anidado inválido",
            "{ { { { $ $ $ R } } } } - Inválido: Exceso anidamiento",
            "{ < } - Inválido: Sin monedas para devolver"
        ]
        
        for ejemplo in ejemplos:
            self.ejemplos_listbox.insert(tk.END, ejemplo)
    
    def cargar_ejemplo_seleccionado(self, event=None):
        """Cargar el ejemplo seleccionado en el campo de entrada"""
        try:
            selection = self.ejemplos_listbox.curselection()
            if selection:
                ejemplo_completo = self.ejemplos_listbox.get(selection[0])
                # Extraer solo la cadena (parte antes del primer " - ")
                cadena = ejemplo_completo.split(" - ")[0]
                self.cadena_actual.set(cadena)
                self.entry_cadena.focus()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ejemplo: {e}")
    
    def simular_accion(self, accion):
        """Simular una acción en el simulador visual"""
        if accion == '$':
            self.saldo_sim += 1
            self.cadena_sim += "$ "
        elif accion == 'R':
            if self.saldo_sim >= 3:
                self.saldo_sim -= 3
                self.cadena_sim += "R "
            else:
                messagebox.showwarning("Simulador", "Saldo insuficiente para refresco (necesitas 3 monedas)")
                return
        elif accion == '<':
            if self.saldo_sim >= 1:
                self.saldo_sim -= 1
                self.cadena_sim += "< "
            else:
                messagebox.showwarning("Simulador", "No hay monedas para devolver")
                return
        elif accion == '{}':
            self.cadena_sim += "{ } "
        
        self.actualizar_simulador()
    
    def reset_simulador(self):
        """Resetear el simulador"""
        self.saldo_sim = 0
        self.cadena_sim = "{ "
        self.actualizar_simulador()
    
    def actualizar_simulador(self):
        """Actualizar la visualización del simulador"""
        self.canvas.delete("all")
        
        # Dibujar la máquina
        self.canvas.create_rectangle(20, 20, 180, 130, fill='#7f8c8d', outline='#2c3e50', width=2)
        self.canvas.create_text(100, 35, text="MÁQUINA EXPENDEDORA", font=('Arial', 8, 'bold'), fill='white')
        
        # Mostrar saldo
        self.canvas.create_text(100, 55, text=f"Saldo: ${self.saldo_sim}", 
                               font=('Arial', 12, 'bold'), fill='#f1c40f')
        
        # Mostrar cadena actual
        cadena_display = self.cadena_sim + "}"
        if len(cadena_display) > 25:
            cadena_display = cadena_display[:22] + "..."
        self.canvas.create_text(100, 80, text=f"Cadena: {cadena_display}", 
                               font=('Courier', 9), fill='white')
        
        # Ranura para monedas
        self.canvas.create_oval(200, 40, 220, 60, fill='#f39c12', outline='#d68910')
        self.canvas.create_text(230, 50, text="💰", font=('Arial', 12))
        
        # Dispensador de refrescos
        self.canvas.create_rectangle(200, 70, 240, 100, fill='#27ae60', outline='#1e8449')
        self.canvas.create_text(260, 85, text="🥤", font=('Arial', 12))
        
        # Devolución
        self.canvas.create_rectangle(200, 110, 240, 130, fill='#e67e22', outline='#d35400')
        self.canvas.create_text(260, 120, text="↩️", font=('Arial', 12))
        
        # Actualizar campo de entrada con la cadena del simulador
        if len(self.cadena_sim.strip()) > 2:  # Si hay más que solo "{ "
            cadena_completa = self.cadena_sim.strip() + " }"
            self.cadena_actual.set(cadena_completa)
    
    def analizar_cadena(self):
        """Analizar la cadena introducida"""
        cadena = self.cadena_actual.get().strip()
        
        if not cadena:
            messagebox.showwarning("Advertencia", "Introduce una cadena para analizar")
            return
        
        try:
            # Realizar análisis
            parser = Parser(cadena)
            arbol = parser.parse()
            analisis_semantico(arbol)
            
            # Mostrar resultado
            if arbol.valido:
                self.result_label.config(text="✅ Cadena ACEPTADA SEMÁNTICAMENTE", 
                                       fg='#27ae60', bg='#d5f4e6')
                resultado = f"✅ ACEPTADA\\nSaldo final: {arbol.saldo}\\nRefrescos: {arbol.refrescos}"
            else:
                self.result_label.config(text=f"❌ Cadena RECHAZADA: {arbol.error}", 
                                       fg='#e74c3c', bg='#fadbd8')
                resultado = f"❌ RECHAZADA\\nError: {arbol.error}"
            
            # Mostrar árbol decorado
            self.tree_text.delete(1.0, tk.END)
            self.tree_text.insert(tk.END, str(arbol))
            
            # Scroll al inicio
            self.tree_text.see(1.0)
            
        except Exception as e:
            self.result_label.config(text=f"❌ Error de análisis sintáctico: {e}", 
                                   fg='#e74c3c', bg='#fadbd8')
            self.tree_text.delete(1.0, tk.END)
            self.tree_text.insert(tk.END, f"Error de análisis sintáctico:\\n{e}")
    
    def limpiar_resultados(self):
        """Limpiar todos los resultados"""
        self.cadena_actual.set("")
        self.result_label.config(text="Resultado: Esperando análisis...", 
                               fg='black', bg='#f0f0f0')
        self.tree_text.delete(1.0, tk.END)
        self.reset_simulador()
    
    def mostrar_gda(self):
        """Mostrar la Gramática Decorada con Atributos en una ventana nueva"""
        gda_window = tk.Toplevel(self.root)
        gda_window.title("Gramática Decorada con Atributos (GDA)")
        gda_window.geometry("800x600")
        gda_window.configure(bg='#f0f0f0')
        
        # Crear texto scrollable
        gda_text = scrolledtext.ScrolledText(gda_window, font=('Courier', 10),
                                           bg='#2c3e50', fg='#ecf0f1')
        gda_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Contenido de la GDA
        gda_content = """=== GRAMÁTICA DECORADA CON ATRIBUTOS (GDA) ===

GRAMÁTICA BASE:
P → { C }
C → A C | ε
A → $ | R | < | { C }

ATRIBUTOS SEMÁNTICOS:
• saldo (sintetizado): cantidad de monedas disponibles
• valido (sintetizado): validez semántica del bloque
• nivel (heredado): profundidad de anidamiento
• refrescos (sintetizado): número de refrescos comprados
• error (sintetizado): descripción del error si existe

REGLAS SEMÁNTICAS:

P → { C }
  P.saldo = C.saldo
  P.valido = C.valido
  P.refrescos = C.refrescos
  P.error = C.error
  C.nivel = P.nivel

C → A C₁
  C.saldo = procesar_secuencia(A, C₁)
  C.valido = A.valido AND C₁.valido
  C.refrescos = contar_refrescos(A, C₁)
  A.nivel = C.nivel
  C₁.nivel = C.nivel

C → ε
  C.saldo = 0
  C.valido = true
  C.refrescos = 0

A → $
  A.saldo = saldo_actual + 1
  A.valido = true
  A.refrescos = 0

A → R
  if saldo_actual >= 3 then
    A.saldo = saldo_actual - 3
    A.valido = true
    A.refrescos = 1
  else
    A.valido = false
    A.error = 'Saldo insuficiente para refresco'

A → <
  if saldo_actual >= 1 then
    A.saldo = saldo_actual - 1
    A.valido = true
  else
    A.valido = false
    A.error = 'No hay monedas para devolver'

A → { C }
  if A.nivel >= 3 then
    A.valido = false
    A.error = 'Exceso de anidamiento (>3)'
  else
    C.nivel = A.nivel + 1
    A.saldo = 0  // Los bloques no transfieren saldo
    A.valido = C.valido
    A.refrescos = 0  // Los refrescos del bloque no se cuentan

RESTRICCIONES ADICIONALES:
• Máximo 3 refrescos por bloque
• Máximo 3 niveles de anidamiento
• Saldo nunca puede ser negativo
• Cada bloque maneja su propio saldo independiente"""
        
        gda_text.insert(tk.END, gda_content)
        gda_text.config(state='disabled')

def main():
    """Función principal de la interfaz gráfica"""
    root = tk.Tk()
    app = MaquinaExpendedoraGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()

if __name__ == "__main__":
    main()
