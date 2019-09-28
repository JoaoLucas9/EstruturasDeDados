"""Implementação de uma SkipList.

Autor: João Lucas Alves Almeida Santos
Versão: 0.1 beta
"""

from erros import ItemNaoEncontrado as ChaveNaoEncontrada
from arvore import IGUAIS
from random import choice
from erros import ColecaoVazia as ListaVazia


def _nodosAbaixo(nodo):
    while nodo.abaixo is not None:
        nodo = nodo.abaixo
        yield nodo


def _inserir(anterior, nodo):
    """Insere o nodo após o anterior.

    Parâmetros:
       :param anterior: _Nodo -> antecessor do nodo

       :param nodo: _Nodo -> o nodo que será inserido
    """
    sucessor = anterior.sucessor
    anterior.sucessor = nodo
    nodo.anterior = anterior
    nodo.sucessor = sucessor
    sucessor.anterior = nodo


def _novaListaVazia():
    raiz = _Nodo(_MENOR, None)
    ultimo = _Nodo(_MAIOR, None, anterior=raiz)
    raiz.sucessor = ultimo

    return raiz


def _ultimoNodo(nodo):
    while nodo.sucessor.chave is not _MAIOR:
        nodo = nodo.sucessor

    return nodo


def _proximo(iteravel, padrao):
    try:
        return next(iteravel)
    except StopIteration:
        return padrao


def _remover(nodo):
    antecessor = nodo.anterior
    sucessor = nodo.sucessor
    antecessor.sucessor = sucessor
    sucessor.anterior = antecessor


def _ultimoNodoDaTorre(nodo):
    while nodo.abaixo is not None:
        nodo = nodo.abaixo

    return nodo


_MENOR = 'o menor valor das chave Recife_PE 08/07/2019 13:50'

_MAIOR = 'o maior valor das chave Recife_PE 08/07/2019 13:50'

_TRUE_OR_FALSE = (True, False)


class SkipList:
    """Implementação de um mapa que mantém as chaves ordenadas."""

    def __init__(self, comparador):
        """
        Parâmetros
           :param comparador : Callable compara duas chaves e retorna a
           maior delas, se elas forem iguais então o comparador deve
           retornar arvore.IGUAIS.
           Se você deseja registrar e carregar a SkipList em/de um arquivo
           utilizando as funções pickle.dump() e pickle.load(), o comparador
           não pode ser uma função lambda.
        """
        self._raiz = _novaListaVazia()

        if comparador is None:
            raise TypeError('O comparador não pode ser None.')
        self._comparador = comparador
        self._tamanho = 0


    def _maior(self, c1, c2):
        """Determina qual a maior de duas chaves"""
        if c1 is _MENOR or c2 is _MAIOR:
            return c2
        if c1 is _MAIOR or c2 is _MENOR:
            return c1
        return self._comparador(c1, c2)


    @property
    def tamanho(self):
        """Quantidade de pares chave-valor na SkipList.
        Escrita: ✗
        """
        return self._tamanho


    @property
    def vazia(self):
        """True se o heap estiver vazio, false caso contrário.
        Escrita: ✗
        """
        return self.tamanho == 0


    def  __setitem__(self, chave, valor):
        """Insere o par chave-valor ou substitui o atual
        valor da chave (se ela já estiver presente na lista).


        Parâmetros:
           :param chave uma chave

           :param valor
           1) não é um callable: simplesmente insere-se a chave juntamente
           com o valor na tabela.

           2) é um callable: informa-se a chave e o seu valor atual para o
           callable (nesta ordem), o valor retornado da função será inserido
           juntamente com a chave, ou o atual valor da chave será substituido.
           Se a chave ainda não estiver na tabela, então None será informado
           como o valor.
        """
        iterador = reversed(self._skipSearchPath(chave))
        n = next(iterador)

        if self._saoIguais(n.chave, chave):
            n.valor = valor(chave, n.valor) if callable(valor) else valor
            return

        nodo = _Nodo(chave, valor(chave, None) if callable(valor) else valor)
        _inserir(n, nodo)

        while choice(_TRUE_OR_FALSE):
            nodo = _Nodo(chave, None, abaixo=nodo)
            n = _proximo(iterador, self._adicionarNovaLista())
            _inserir(n, nodo)

        self._tamanho += 1


    def _saoIguais(self, c1, c2):
        return self._maior(c1, c2) is IGUAIS


    def _adicionarNovaLista(self):
        """Cria uma lista vazia, adiciona-a ao conjunto de listas
        e reconfigura a raiz deste SkipList.

        :return a raiz da nova lista
        """
        ultimo = _Nodo(_MAIOR, None, abaixo=_ultimoNodo(self._raiz))
        raiz = _Nodo(_MENOR, None, abaixo=self._raiz, sucessor=ultimo)
        ultimo.anterior = raiz
        self._raiz = raiz

        return raiz


    def _skipSearchPath(self, chave):
        """Versão modificada do SkipSearch.
        Registra o nodo que possue a maior chave menor igual a chave
        informada, para cada um dos níveis deste SkipSearch e retorna este
        registro.
        """
        nodo = self._maiorChaveMenorIgual(chave, self._raiz)
        caminho = [nodo]

        while self._maior(nodo.chave, chave) is chave and nodo.abaixo is not None:
            nodo = self._maiorChaveMenorIgual(chave, nodo.abaixo)
            caminho.append(nodo)
        caminho +=  _nodosAbaixo(nodo)

        return caminho


    def parMenorIgual(self, chave):
        """Retorna o par que possui a maior chave menor igual a chave
        informada.
        Em outras palavras, procura pela maior chave no SkipList (vamos
        chamá-la de C), sendo que C deve ser menor igual a chave informada

        Seja p o par retornado, para obter a chave basta fazer p.chave,
        analogamente, para obter o valor basta fazer p.valor.

        Erros
           :exception ItemNaoEncontrado se não for encontrada nenhuma chave
           menor igual a chave informada.
        """
        nodo = self._skipSearch(chave)

        if nodo.chave is _MENOR:
            raise ChaveNaoEncontrada(f'Não foi localizada nenhuma chave '
                                     f'menor igual a chave {chave}.')
        return nodo


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


    def parMaiorIgual(self, chave):
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
        return nodo


    def __getitem__(self, chave):
        """Retorna o valor associado a chave.

        Erros
           :exception ItemNaoEncontrado se a chave não for localizada.
        """
        nodo = self._skipSearch(chave)

        if self._maior(nodo.chave, chave) is not IGUAIS:
            raise ChaveNaoEncontrada(f'A chave {chave} não foi localizada.')

        return nodo.valor


    def __contains__(self, chave):
        """Determina se uma chave está presente na lista.

        :return true se a chave for localizada, false caso contrário.
        """
        return self._saoIguais(self._skipSearch(chave).chave, chave)


    def __delitem__(self, chave):
        """Remove o par que possui a chave informada.

        Erro
           :exception ItemNaoEncontrado se a chave não for localizada
        """
        nodo = self._nodo(chave)

        while nodo is not None:
            _remover(nodo)
            nodo = nodo.abaixo

        self._tamanho -= 1


    def _nodo(self, chave):
        """Retorna o primeiro nodo encontrado que possui a chave informada.
        O nodo estará na lista mais alta possível, diferentemente do método
        SkipSearch que retorna o nodo que está na lista mais baixa.
        """
        for nodo in self._skipSearchPath(chave):
            if self._saoIguais(nodo.chave, chave):
                return nodo
        raise ChaveNaoEncontrada(f'A chave {chave} não foi localizada.')


    def _nodosComChave(self, chave):
        """Retorna todos os nodos que possuem a chave informada."""
        caminho = self._skipSearchPath(chave)
        return (nodo for nodo in caminho if self._saoIguais(nodo.chave, chave))


    def __iter__(self):
        """Retorna um iterador que percorre as chaves da tabela."""
        return (par.chave for par in self.pares())


    def __eq__(self, obj):
        """Compara self com obj.

        Serão iguais se obj for uma SkipList e os pares chave-valor de self
        e obj forem iguais e se estiverem na mesma ordem.

        Dois pares p1 e p2 serão iguais se a chave de p1 for igual a chave
        de p2 e o valor de p1 for igual ao valor de p2.

        As chaves serão comparadas utilizando o comparador de self enquanto
        que os valores serão comparados com o operador ==.
        """
        if not isinstance(obj, SkipList) or self.tamanho != obj.tamanho:
            return False
        iguais = lambda n1, n2: n1.valor == n2.valor and self._saoIguais(
            n1.chave, n2.chave)

        return all(iguais(n1, n2) for n1, n2 in zip(self.pares(), obj.pares()))


    def pares(self):
        """Gerador que percorre todos os pares da tabela.

        Seja p um dos pares da tabela, para obter a chave basta fazer
        p.chave, analogamente, para obter o valor basta fazer p.valor.
        """
        nodo = _ultimoNodoDaTorre(self._raiz).sucessor

        while nodo.chave is not _MAIOR:
            yield nodo
            nodo = nodo.sucessor


    def valores(self):
        """Retorna um iterador que percorre os valores da tabela."""
        return (par.valor for par in self.pares())


    def menorChave(self):
        """Retorna a menor chave.

        Erros
           :exception ColecaoVazia se a estrutura estiver vazia.
        """
        if self.tamanho == 0:
            raise ListaVazia
        return _ultimoNodoDaTorre(self._raiz).sucessor.chave


    def maiorChave(self):
        """Retorna a maior chave.

        Erros
           :exception ColecaoVazia se a estrutura estiver vazia.
        """
        if self.tamanho == 0:
            raise ListaVazia
        return _ultimoNodo(_ultimoNodoDaTorre(self._raiz)).chave


    def menorPar(self):
        """Retorna o par que possui a menor chave da lista.

        Erros
           :exception ColecaoVazia se a lista estiver vazia
        """
        if self.vazia:
            raise ListaVazia

        return _ultimoNodoDaTorre(self._raiz).sucessor


    def maiorPar(self):
        """Retorna o par que possui a maior chave da lista.

        Erros
           :exception ColecaoVazia se a lista estiver vazia
        """
        if self.vazia:
            raise ListaVazia

        return _ultimoNodo(_ultimoNodoDaTorre(self._raiz))


    def valor(self, chave, padrao=None):
        """Retorna o valor associado com a chave se ela estiver na lista,
        senão padrao."""
        e = self._skipSearch(chave)

        return e.valor if self._saoIguais(e.chave, chave) else padrao


class _Nodo:

    def __init__(self, chave, valor, anterior=None, sucessor=None,
                 abaixo=None):
        self.chave = chave
        self.valor = valor
        self.anterior = anterior
        self.sucessor = sucessor
        self.abaixo = abaixo

