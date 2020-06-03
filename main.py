import threading
import queue

#
# A biblioteca queue provê a classe Queue que implementa a estrutura de dados
# que funciona como uma fila e tendo seus métodos sincronizados (o que quer
# dizer que são seguros para serem utilizados em aplicações concorrentes - 
# multi-threading).
#
# Para este simples exemplo nós podemos utilisar uma unica fila.
#
# Os elementos serão inseridos na fila por uma unica thread, que será a thread
# principal do programa.
#
# Porém, a leitura será feita por quatro threads.
#
# 
fila = queue.Queue(maxsize=4)

#
# imprimeSequencia:
#
# Esta é a função que será lançada como threads independentes. Ela lerá os
# números inteiros colocados na fila e imprimirá as sequencias de 0 ao numero
# lido no terminal.
def imprimeSequencia(fila=None):
    print("thread = {0}, iniciada".format(threading.currentThread().name))

    if fila is None:
        print("thread encerrada porque a fila não foi informada corretamente")
        return

    while True:
        limite = fila.get()
        print(
            "thread = {0}, novo número lido da fila: {1:d}".format(
                threading.currentThread().name,
                limite
            )
        )

        for n in range(limite):
            print(
                "thread = {0}, numero = {1:5d}".format(
                    threading.currentThread().name,
                    n
                )
            )

        fila.task_done()

#
# O trecho de código abaixo lança as quatro threads que farão a leitura dos
# elementos colocados na fila.
for t in range(4):
    threading.Thread(
        target=imprimeSequencia,
        kwargs={"fila":fila},
        name="IS-{0:d}".format(t),
        daemon=True
    ).start()

#
# O trecho de código abaixo escreve os números na fila.
for limite in range(1000, 10000, 1000):
    print(
        "thread = {0}, escrevendo novo número na fila: {1:d}".format(
            threading.currentThread().name,
            limite
        )
    )
    fila.put(limite)

#
# Este método bloqueia a thread principal fazendo com que o programa aguarde
# até que todas as threads finalizem o processamento.
fila.join()

print("processamento terminado")