import threading
import time
import random



class Filosofo(threading.Thread):

    def __init__(self, nome, garfo_esquerdo, garfo_direito):
        threading.Thread.__init__(self)
        self.nome = nome
        self.garfo_esquerdo = garfo_esquerdo
        self.garfo_direito = garfo_direito
        self.max_comida = random.randint(40, 60)
        self.inicio = time.time()
        self.comida = self.max_comida
        self.tempo = True

    def run(self):
        while self.tempo:
            print(f'O filósofo {self.nome} começou a pensar')
            time.sleep(random.randint(10, 20))
            print(f'O filósofo {self.nome} começou a comer')
            self.tentar_comer()


    def parar(self):
        self.tempo = False

    def tentar_comer(self):
        while self.tempo:
            liberado1 = self.garfo_esquerdo.acquire(False)
            liberado2 = self.garfo_direito.acquire(False)
            atual = time.time()

            if atual - self.inicio > self.max_comida:
                print(f'O filósofo {self.nome} ficou muito tempo sem comer')

            if liberado1 and liberado2:
                self.comida = self.max_comida
                self.garfo_esquerdo.release()
                self.garfo_direito.release()

                print(f'O filósofo {self.nome} terminou de comer')
                self.inicio = atual
                return


if __name__ == '__main__':
    nomes_filosofos = [f'filosofo {i}' for i in range(1, 5+1)]
    garfos = [threading.Lock() for _ in range(len(nomes_filosofos))]
    filosofos = []

    for num_filosofo in range(len(nomes_filosofos)):
        if num_filosofo == 0:
            filosofos.append(Filosofo(nomes_filosofos[num_filosofo], garfos[4], garfos[0]))
        else:
            filosofos.append(Filosofo(nomes_filosofos[num_filosofo], garfos[num_filosofo-1], garfos[num_filosofo]))

    for num_filosofo in range(len(filosofos)):
        filosofos[num_filosofo].start()
        time.sleep(1)

    time.sleep(120)
    for num_filosofo in range(len(filosofos)):
        filosofos[num_filosofo].parar()

