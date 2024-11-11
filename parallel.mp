SEQ
# Inicializando variaveis para calc do fatorial
numero = 9
fatorial = 1
i = 1

# Inicializando variaveis para serie de fibonnaci
n = 20  # Número de termos da série Fibonacci
a = 0   #primeiro termo
b = 1   #segundo termo
j = 2   #count inicia em 2


Output("Fibonacci Sequence with ", n," terms:\n")  


PAR
while (i <= numero){
    fatorial = fatorial * i
    i = i+1
}
  
Output(a, " ")
Output(b, " ")

while (j < n ){
    c = a + b
    Output(c, " ")
    a = b
    b = c
    j = j+1
}



Output("\n\n")


SEQ
Output("fatorial(",numero,") = ", fatorial, "\n")