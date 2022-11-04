import threading
import time
import random



class Filosofo(threading.Thread):

    def __init__(self, nome, garfo_esquerdo, garfo_direito):
        threading.Thread.__init__(self)
        self.nome = nome
        self.garfo_esquerdo = garfo_esquerdo
        self.garfo_direito = garfo_direito
        self.tempo_comida = random.randint(20, 25)
        self.inicio = random.randint(30, 35)
        self.tempo = True

    def run(self):
        while self.tempo:
            print(f'\nO filósofo {self.nome} começou a pensar')
            time.sleep(5)

            if self.inicio > self.tempo_comida:
                self.tentar_comer()


    def parar(self):
        self.tempo = False

    def tentar_comer(self):
        while self.tempo:
            atual = time.time()
            if self.inicio < self.tempo_comida:
                print(f'\nO filósofo {self.nome} ficou muito tempo sem comer')
                self.garfo_esquerdo.acquire(False)
                self.garfo_esquerdo.acquire(False)


            self.garfo_esquerdo.acquire(True)
            resultado = self.garfo_direito.acquire(False)
            if resultado:
                break
            self.garfo_esquerdo.release()

        else:
            return

        print(f"\n {self.nome} começou a comer")
        time.sleep(random.randint(5, 10))
        print(f"\n {self.nome} parou de comer")

        self.garfo_esquerdo.release()  # libera o garfo 1
        self.garfo_direito.release()  # libera o garfo 2
        self.inicio = atual



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
