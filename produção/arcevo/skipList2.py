from erros import ItemNaoEncontrado as ChaveNaoEncontrada
from arvore import IGUAIS
from random import choice


def _encapsular(comparador):

    def _comparador(c1, c2):
        if c1 is _MENOR or c2 is _MAIOR:
            return c2
        if c1 is _MAIOR or c2 is _MENOR:
            return c1
        return comparador(c1, c2)

    return _comparador


def _nodosAbaixo(nodo):
    while nodo.abaixo is not None:
        nodo = nodo.abaixo
        yield nodo


def _inserir(anterior, nodo):
    sucessor = anterior.sucessor
    anterior.sucessor = nodo
    nodo.anterior = anterior
    nodo.sucessor = sucessor
    sucessor.anterior = nodo


def _criarNovaLista(nodo):
    raiz = _Nodo(_MENOR, None, sucessor=nodo)
    ultimo = _Nodo(_MAIOR, None, anterior=nodo)
    nodo.anterior = raiz
    nodo.sucessor = ultimo

    return raiz


def _listaVazia():
    raiz = _Nodo(_MENOR, None)
    ultimo = _Nodo(_MAIOR, None, anterior=raiz)
    raiz.sucessor = ultimo

    return raiz


def _ultimoNodoDaLista(nodo):
    while nodo.sucessor is not None:
        nodo = nodo.sucessor

    return nodo


def _estaVazia(lista):
    return lista.item is _MENOR and lista.sucessor.item is _MAIOR


def _proximo(iteravel, padrao):
    try:
        return next(iteravel)
    except StopIteration:
        return padrao


_MENOR = 'o menor valor possível para uma chave Recife_PE 08/07/2019 13:50'

_MAIOR = 'o maior valor possível para uma chave Recife_PE 08/07/2019 13:50'

TRUE_OR_FALSE = (True, False)


class SkipList:

    def __init__(self, comparador):
        self._raiz = _listaVazia()
        self._maior = _encapsular(comparador)
    

    def prePronta(self):
        raiz_4 = _Nodo(_MENOR, None)
        nodo1_4 = _Nodo(_MAIOR, None)
        raiz_4.sucessor = nodo1_4
        nodo1_4.anterior = raiz_4

        raiz_3 = _Nodo(_MENOR, None)
        nodo1_3 = _Nodo(100, None)
        nodo2_3 = _Nodo(_MAIOR, None)
        raiz_3.sucessor = nodo1_3
        nodo1_3.anterior = raiz_3
        nodo1_3.sucessor = nodo2_3
        nodo2_3.anterior = nodo1_3

        raiz_2 = _Nodo(_MENOR, None)
        nodo1_2 = _Nodo(15, None)
        nodo2_2 = _Nodo(100, None)
        nodo3_2 = _Nodo(_MAIOR, None)
        raiz_2.sucessor = nodo1_2
        nodo1_2.anterior = raiz_2
        nodo1_2.sucessor = nodo2_2
        nodo2_2.anterior = nodo1_2
        nodo2_2.sucessor = nodo3_2
        nodo3_2.anterior = nodo2_2

        raiz_1 = _Nodo(_MENOR, None)
        nodo1_1 = _Nodo(5, None)
        nodo2_1 = _Nodo(15, None)
        nodo3_1 = _Nodo(50, None)
        nodo4_1 = _Nodo(100, None)
        nodo5_1 = _Nodo(_MAIOR, None)
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

        raiz_0 = _Nodo(_MENOR, None)
        nodo1_0 = _Nodo(2, 'caneta')
        nodo2_0 = _Nodo(5, 'regua')
        nodo3_0 = _Nodo(10, 'caderno')
        nodo4_0 = _Nodo(15, 'estojo')
        nodo5_0 = _Nodo(30, 'livro')
        nodo6_0 = _Nodo(50, 'mochila')
        nodo7_0 = _Nodo(60, 'fone')
        nodo8_0 = _Nodo(100, 'uniforme')
        nodo9_0 = _Nodo(_MAIOR, None)
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
        return self


    def  __setitem__(self, chave, valor):
        nodo = _Nodo(chave, valor)

        iterador = reversed(self._skipSearchPath(chave))

        _inserir(next(iterador), nodo)

        while choice(TRUE_OR_FALSE):
            nodo = _Nodo(chave, None, abaixo=nodo)
            lista = _proximo(iterador, _listaVazia())
            _inserir(lista, nodo)

            if lista.abaixo is None:
                self._adicionar(lista)

        if not _estaVazia(self._raiz):
            self._adicionar(_listaVazia())



    def _adicionar(self, lista):
        raiz = self._raiz
        lista.abaixo = raiz
        _ultimoNodoDaLista(lista).abaixo = _ultimoNodoDaLista(raiz)
        self._raiz = lista


    def _skipSearchPath(self, chave):
        """Retorna o nodo que possui a maior chave menor igual a chave.
        Retorna o nodo que possui a maior chave, sendo que a chave deste
        nodo deve ser menor igual ao parâmetro chave informado.
        Procura por todas as listas do SkipList.
        Pode retornar o nodo com a chave _MENOR.
        """
        nodo = self._maiorChaveMenorIgual(chave, self._raiz)
        caminho = [nodo]

        while self._maior(nodo.chave, chave) is chave and nodo.abaixo is not None:
            nodo = self._maiorChaveMenorIgual(chave, nodo.abaixo)
            caminho.append(nodo)
        caminho +=  _nodosAbaixo(nodo)

        return caminho


    def maiorChave(self, chave):
        """Retorna uma tupla contendo a maior chave menor igual a chave
        informada e o valor associado a ela.
        Em outras palavras, procura pela maior chave no SkipList (vamos
        chamá-la de C), sendo que C deve ser menor igual a chave informada,
        e retorna-se a tupla (C, valor associado a C).

        Erros
           :exception ItemNaoEncontrado se não for encontrada nenhuma chave
           menor igual a chave informada.
        """
        nodo = self._skipSearch(chave)

        if nodo.chave is _MENOR:
            raise ChaveNaoEncontrada(f'Não foi localizada nenhuma chave '
                                     f'menor igual a chave {chave}.')
        return nodo.chave, nodo.item


    def _skipSearch(self, chave):
        """Retorna o nodo que possui a maior chave menor igual a chave.
        Retorna o nodo que possui a maior chave, sendo que a chave deste
        nodo deve ser menor igual ao parâmetro chave informado.
        Procura por todas as listas do SkipList.
        Pode retornar o nodo com a chave _MENOR.
        """
        return self._skipSearchPath(chave)[-1]


    def _maiorChaveMenorIgual(self, chave, nodo):
        """Retorna o nodo que possui a maior chave menor igual a chave.
        Retorna o nodo que possui a maior chave, sendo que a chave deste
        nodo deve ser menor igual ao parâmetro chave informado.
        Percorre apenas a lista na qual o nodo esta.
        Pode retornar o nodo com a chave _MENOR.
        """
        while self._maior(nodo.chave, chave) is chave:
            nodo = nodo.sucessor

        return nodo.anterior if self._maior(nodo.chave, chave) is nodo.chave else nodo


    def menorChave(self, chave):
        """Retorna uma tupla contendo a menor chave maior igual a chave
        informada e o valor associado a ela.
        Em outras palavras, procura pela menor chave no SkipList (vamos
        chamá-la de C), sendo que C deve ser maior igual a chave informada,
        e retorna-se a tupla (C, valor associado a C).

        Erros
           :exception ItemNaoEncontrado se não for encontrada nenhuma chave
           maior igual a chave informada.
        """
        nodo = self._skipSearch(chave)

        if self._maior(nodo.chave, chave) is chave:
            nodo = nodo.sucessor

        if nodo.chave is _MAIOR:
            raise ChaveNaoEncontrada(f'Não foi localizada nenhuma chave '
                                     f'maior igual a {chave}.')
        return nodo.chave, nodo.item


    def __getitem__(self, chave):
        """Retorna o valor associado a chave.

        Erros
           :exception ItemNaoEncontrado se a chave não for localizada.
        """
        nodo = self._skipSearch(chave)

        if self._maior(nodo.chave, chave) is not IGUAIS:
            raise ChaveNaoEncontrada(f'A chave {chave} não foi localizada.')

        return nodo.item


    def __contains__(self, chave):
        """Determina se uma chave está presente na lista.

        :return true se a chave for localizada, false caso contrário.
        """
        return self._maior(self._skipSearch(chave).chave, chave) is IGUAIS


class _Nodo:

    def __init__(self, chave, item, anterior=None, sucessor=None, abaixo=None):
        self.chave = chave
        self.item = item
        self.anterior = anterior
        self.sucessor = sucessor
        self.abaixo = abaixo
