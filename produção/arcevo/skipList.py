from arvore import IGUAIS


def _ultimoDaTorre(nodo):
    while nodo.abaixo is not None:
        nodo = nodo.abaixo

    return nodo


class SkipList:


    def __init__(self):
        raiz_4 = _Nodo(-1000, None)
        nodo1_4 = _Nodo(1000, None)
        raiz_4.sucessor = nodo1_4
        nodo1_4.anterior = raiz_4

        raiz_3 = _Nodo(-1000, None)
        nodo1_3 = _Nodo(100, None)
        nodo2_3 = _Nodo(1000, None)
        raiz_3.sucessor = nodo1_3
        nodo1_3.anterior = raiz_3
        nodo1_3.sucessor = nodo2_3
        nodo2_3.anterior = nodo1_3

        raiz_2 = _Nodo(-1000, None)
        nodo1_2 = _Nodo(15, None)
        nodo2_2 = _Nodo(100, None)
        nodo3_2 = _Nodo(1000, None)
        raiz_2.sucessor = nodo1_2
        nodo1_2.anterior = raiz_2
        nodo1_2.sucessor = nodo2_2
        nodo2_2.anterior = nodo1_2
        nodo2_2.sucessor = nodo3_2
        nodo3_2.anterior = nodo2_2

        raiz_1 = _Nodo(-1000, None)
        nodo1_1 = _Nodo(5, None)
        nodo2_1 = _Nodo(15, None)
        nodo3_1 = _Nodo(50, None)
        nodo4_1 = _Nodo(100, None)
        nodo5_1 = _Nodo(1000, None)
        raiz_1.sucessor = nodo1_1
        nodo1_1.anterior = raiz_1
        nodo1_1.sucessor = nodo2_1
        nodo2_1.anterior = nodo1_1
        nodo2_1.sucessor = nodo3_1
        nodo3_1.anterior = nodo2_1
        nodo3_1.sucessor = nodo4_1
        nodo4_1.anterior = nodo3_1
        nodo4_1.sucessor = nodo5_1
        nodo5_1.anterior = nodo4_1

        raiz_0 = _Nodo(-1000, None)
        nodo1_0 = _Nodo(2, 'caneta')
        nodo2_0 = _Nodo(5, 'regua')
        nodo3_0 = _Nodo(10, 'caderno')
        nodo4_0 = _Nodo(15, 'estojo')
        nodo5_0 = _Nodo(30, 'livro')
        nodo6_0 = _Nodo(50, 'mochila')
        nodo7_0 = _Nodo(60, 'fone')
        nodo8_0 = _Nodo(100, 'uniforme')
        nodo9_0 = _Nodo(1000, None)
        raiz_0.sucessor = nodo1_0
        nodo1_0.anterior = raiz_0
        nodo1_0.sucessor = nodo2_0
        nodo2_0.anterior = nodo1_0
        nodo2_0.sucessor = nodo3_0
        nodo3_0.anterior = nodo2_0
        nodo3_0.sucessor = nodo4_0
        nodo4_0.anterior = nodo3_0
        nodo4_0.sucessor = nodo5_0
        nodo5_0.anterior = nodo4_0
        nodo5_0.sucessor = nodo6_0
        nodo6_0.anterior = nodo5_0
        nodo6_0.sucessor = nodo7_0
        nodo7_0.anterior = nodo6_0
        nodo7_0.sucessor = nodo8_0
        nodo8_0.anterior = nodo7_0
        nodo8_0.sucessor = nodo9_0
        nodo9_0.anterior = nodo8_0

        raiz_4.abaixo = raiz_3
        raiz_3.abaixo = raiz_2
        raiz_2.abaixo = raiz_1
        raiz_1.abaixo = raiz_0

        nodo1_4.abaixo = nodo2_3
        nodo2_3.abaixo = nodo3_2
        nodo3_2.abaixo = nodo5_1
        nodo5_1.abaixo = nodo9_0

        nodo1_3.abaixo = nodo2_2
        nodo1_2.abaixo = nodo2_1
        nodo2_2.abaixo = nodo4_1
        nodo1_1.abaixo = nodo2_0
        nodo2_1.abaixo = nodo4_0
        nodo3_1.abaixo = nodo6_0
        nodo4_1.abaixo = nodo8_0

        self._raiz = raiz_4
        self._maior = lambda c1, c2: IGUAIS if c1 == c2 else max(c1, c2)


    def maiorChave(self, chave):
        """Retorna uma tupla contendo a maior chave menor igual a chave
        informada e o valor associado a ela.
        Em outras palavras, procura pela maior chave no SkipList (vamos
        chamá-la de C), sendo que C deve ser menor igual a chave informada,
        e retorna-se a tupla (C, valor associado a C).
        """
        nodo = self._skipSearch(chave)

        return nodo.chave, nodo.item


    def _skipSearch(self, chave):
        """Retorna o nodo que possui a maior chave menor igual a chave.
        Retorna o nodo que possui a maior chave, sendo que a chave deste
        nodo deve ser menor igual ao parâmetro chave informado.
        Procura por todas as listas do SkipList.
        """
        nodo = self._maiorChaveNestaLista(chave, self._raiz)

        while nodo.chave != chave and nodo.abaixo is not None:
            nodo = self._maiorChaveNestaLista(chave, nodo.abaixo)

        return _ultimoDaTorre(nodo)

    # verificado ✓
    def _maiorChaveNestaLista(self, chave, nodo):
        """Retorna o nodo que possui a maior chave menor igual a chave.
        Retorna o nodo que possui a maior chave, sendo que a chave deste
        nodo deve ser menor igual ao parâmetro chave informado.
        Percorre apenas a lista na qual o nodo esta.
        """
        while self._maior(nodo.chave, chave) is chave:
            nodo = nodo.sucessor

        return nodo if self._maior(nodo.chave, chave) is IGUAIS else nodo.anterior


class _Nodo:

    def __init__(self, chave, item, anterior=None, sucessor=None, abaixo=None):
        self.chave = chave
        self.item = item
        self.anterior = anterior
        self.sucessor = sucessor
        self.abaixo = abaixo
