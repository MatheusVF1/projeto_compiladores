SEQ
result = 0
c_channel calc("localhost","localhost")

value1 = 0
value2 = 0
operation = 'null'

Output("Waiting for connections...\n\n")

calc.receive(operation, value1, value2, result)

Output("Conection established\n\n")
Output("Operation:  ")
Output(value1,operation,value2, "\n\n")

if (operation == '-'){
    result = value1 - value2
}
if (operation == '+'){
    result = value1 + value2
}
if (operation == '*'){
    result = value1 * value2
}
if (operation == '/') {
    result = value1 / value2
}

Output("\nResult: ", result, "\n\n")
Output("Sending result...\n\n")
calc.send(result)

Output("Finished\n")
