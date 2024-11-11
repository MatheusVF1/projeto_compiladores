import socket
import threading
import json

has_error = False
symbol_table = {}
channels = {}

output_buffer = ""

with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Variáveis para funções de I/O
output_function = print  # Função padrão para exibir saída
input_function = input  # Função padrão para receber entrada

def execute_stmt(stmt): 
        
    if stmt[0] == 'SEQ':
        for s in stmt[1]:
            execute_stmt(s)
    
    elif stmt[0] == 'PAR':
        threads = []
        for s in stmt[1]:
            thread = threading.Thread(target=execute_stmt, args=(s,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
            
    elif stmt[0] == 'IF':
        if execute_bool(stmt[1]):
            for s in stmt[2]:
                execute_stmt(s)
                
    elif stmt[0] == 'WHILE':
        while execute_bool(stmt[1]):
            for s in stmt[2]:
                execute_stmt(s)
                
    elif stmt[0] == 'INPUT':
        var_name = stmt[1]
        if input_function:
            var_value = input_function()  # Chama a função diretamente
        else:
            var_value = input()  # Usa o input padrão se não for redirecionado
        symbol_table[var_name] = var_value


    elif stmt[0] == 'OUTPUT':
        if isinstance(stmt[1], tuple):
            for v in stmt[1]:
                execute_output(v)
        else:
            execute_output(stmt[1])
    
    elif stmt[0] == '=':
        var_name = stmt[1]
        value = stmt[2]

        if value == "INPUT":
            value = execute_stmt((value, var_name))     
        else:
            value = evaluate_expr(value)
            symbol_table[var_name] = value
            
    elif stmt[0] == "C_CHANNEL":
        channels[stmt[1]] = (stmt[2], stmt[3])
    
    elif not isinstance(stmt[0], tuple) and stmt[0] in channels:
        if stmt[1] == 'SEND':
            channel_name = stmt[0]
            channel = channels.get(channel_name)
            if channel:
                if len(stmt) == 6:
                    _, _, operation, value1, value2, result = stmt
                    send_data(config["port_1"], f"{symbol_table[operation]},{symbol_table[value1]},{symbol_table[value2]},{result}")
                elif len(stmt) == 3:
                    send_data(config["port_2"], f"{symbol_table[stmt[2]]}")
                    
        elif stmt[1] == "RECEIVE":
            channel_name = stmt[0]
            channel = channels.get(channel_name)
            if channel:
                if len(stmt) == 6:
                    stringRec = receive_data(config["port_1"])
                    if stringRec:  # Certifique-se de que stringRec não está vazia
                        operation, value1, value2, result = stringRec.split(",")
                        symbol_table[stmt[2]] = operation
                        symbol_table[stmt[3]] = int(value1) if value1 else 0  # Define um valor padrão
                        symbol_table[stmt[4]] = int(value2) if value2 else 0
                        symbol_table[stmt[5]] = result
                    else:
                        print("Erro: Dados recebidos estão vazios.")
                elif len(stmt) == 3:
                    stringRec = receive_data(config["port_2"])
                    if stringRec:
                        symbol_table[stmt[2]] = stringRec
                    else:
                        print("Erro: Dados recebidos estão vazios.")


    elif isinstance(stmt, tuple):
        for s in stmt:
            execute_stmt(s)

def execute_output(v):
    var_name = v
    var_value = symbol_table.get(var_name, None)
    if var_value is not None:
        formatted_output = str(var_value)
    else:
        formatted_output = var_name.replace("\\n", "\n")

    # Acumula no buffer, mas só envia se houver uma quebra de linha explícita
    global output_buffer

    output_buffer += formatted_output
    if "\n" in formatted_output:
        flush_output()  # Envia o conteúdo acumulado se houver uma nova linha


def flush_output():
    global output_buffer
    # Envia o conteúdo acumulado para a interface gráfica e limpa o buffer
    output_function(output_buffer)  # Usa a função de saída configurada
    output_buffer = ""  # Limpa o buffer


#executa expressões booleanas
def execute_bool(expr):
    if isinstance(expr, tuple):

        op, left, right = expr

        if left in symbol_table:
            left = symbol_table.get(left, 0)  # Obter o valor da variável ou 0 se não existir
        if right in symbol_table:
            right = symbol_table.get(right, 0)  # Obter o valor da variável ou 0 se não existir
            
        if op == '<':
            return evaluate_expr(left) < evaluate_expr(right)
        elif op == '>':
            return evaluate_expr(left) > evaluate_expr(right)
        elif op == '<=':
            return evaluate_expr(left) <= evaluate_expr(right)
        elif op == '>=':
            return evaluate_expr(left) >= evaluate_expr(right)
        elif op == '==':
            return evaluate_expr(left) == evaluate_expr(right)
        elif op == '!=':
            return evaluate_expr(left) != evaluate_expr(right)
    return False

#Avalia as expressões aritméticas
def evaluate_expr(expr):
    try:
        #se for um inteiro ou sinal de uma operação aritmética simples não precisa calcular nada, então apenas retorna o próprio valor
        if isinstance(expr, int) or expr in {'-', '+', '*', '/'}:
            return expr
        elif isinstance(expr, tuple):
            op, left, right = expr
            if op == '+':
                return evaluate_expr(left) + evaluate_expr(right)
            elif op == '-':
                return evaluate_expr(left) - evaluate_expr(right)
            elif op == '*':
                return evaluate_expr(left) * evaluate_expr(right)
            elif op == '/':
                return evaluate_expr(left) / evaluate_expr(right)
            elif any(op == x for x in ['<', '>', '<=', '>=', '==', '!=']):
                return execute_bool(expr)
        elif isinstance(expr, str):
            return symbol_table.get(expr, expr)  # Retorna o valor da variável na tabela de simbolos, se não tiver retorna a propria string
    except Exception as e:
        print(f"Erro de execução: {e} ao avaliar a expressão {expr}")
        has_error = True
        return None



def send_data(port, data):
    host = config["host"]

    # Cria um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta ao host e porta especificados
        sock.connect((host, port))
        # Envia os dados
        sock.sendall(data.encode())
    finally:
        # Fecha o socket
        sock.close()
        #print("conexão cliente fechada")


def receive_data(port):
    host = config["host"]

    # Cria um socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Associa o socket ao host e à porta especificados
        server_socket.bind((host, port))
        # Escuta por conexões
        server_socket.listen(5)
        #print("Aguardando conexão...")
        
        while True:
            # Aceita a conexão
            client_socket, address = server_socket.accept()
            #print(f"Conexão estabelecida com {address}")
            
            # Recebe os dados
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Retorna a string recebida
            return data.decode()
            # Fecha o socket do cliente
            client_socket.close()
    finally:
        # Fecha o socket do servidor
        server_socket.close()