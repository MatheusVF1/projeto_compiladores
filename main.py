import tkinter as tk
from tkinter import scrolledtext
import threading
import syntax as ps
import lexical as lexic
import runner as exec
import sys
import os

class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniPar Interface")
        
        # Texto de saída (substitui o print)
        self.output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.output_box.grid(column=0, row=0, padx=10, pady=10)
        
        # Entrada de dados (substitui o input)
        self.input_box = tk.Entry(root, width=50)
        self.input_box.grid(column=0, row=1, padx=10, pady=(0,10))
        self.input_box.bind("<Return>", self.get_input)  # Captura 'Enter' para processar input
        
        self.input_value = None  # Variável para armazenar valor de entrada
        self.input_ready = threading.Event()  # Evento para sinalizar quando a entrada estiver pronta
    
    def print_to_interface(self, text):
        self.output_box.insert(tk.END, str(text) + "\n")  # Converte para string
        self.output_box.see(tk.END)

    def get_input(self, event=None):
        self.input_value = self.input_box.get()  # Pega o valor da caixa de entrada
        self.print_to_interface(self.input_value)  # Exibe o valor digitado na área de saída
        self.input_box.delete(0, tk.END)  # Limpa a caixa de entrada
        self.input_ready.set()  # Sinaliza que a entrada está pronta


    def wait_for_input(self):
        self.input_ready.wait()  # Espera até que a entrada esteja pronta
        self.input_ready.clear()  # Limpa o sinal para a próxima entrada
        return self.input_value

def read_program_from_file(file_path):
    with open(file_path, 'r') as file:
        program = file.read()
    return program

def run_interpreter(interface, program_code):
    # Certifica que input_function e output_function apontam para os métodos corretos da interface
    exec.output_function = interface.print_to_interface
    exec.input_function = interface.wait_for_input  # Aponta diretamente para wait_for_input

    lexer = lexic.lexer
    result = ps.parser.parse(program_code, lexer=lexer)
    
    if result:
        if not exec.has_error:
            exec.execute_stmt(result)
        else:
            interface.print_to_interface("Erro na execução do interpretador.")

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <nome_do_program.mp> ou minipar <nome_do_programa>")
        sys.exit(1)

    program_file = sys.argv[1]

    if not os.path.exists(program_file):
        print(f"Erro: O arquivo '{program_file}' não foi encontrado.")
        sys.exit(1)
    
    entrada = read_program_from_file(program_file)
    
    root = tk.Tk()
    interface = InterfaceGrafica(root)

    # Inicia o interpretador em uma nova thread
    interpreter_thread = threading.Thread(target=run_interpreter, args=(interface, entrada))
    interpreter_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
