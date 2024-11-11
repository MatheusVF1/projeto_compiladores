SEQ
Output("Connected to server \n\n")

Output("=/=/=/=/=/=/=/= MINIPAR CALCULATOR =/=/=/=/=/=/=/= \n\n")
Output("Operators: + - * /\n")

Output("\nChoose the operator: ")
operation = Input()
            
Output("\nEnter the first number: ")
valor1 = Input()

Output("\nEnter the second number: ")
valor2 = Input()

result = 0
c_channel calc("localhost","localhost")

calc.send(operation, valor1, valor2, result)
calc.receive(result)

Output("\nResultado: ", result, "\n")