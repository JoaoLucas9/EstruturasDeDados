from excecoes import ItemNaoEncontradoErro

class arvore:

    def __init__(self):
        self._raiz = _Nodo(0)
        nodo1 = _Nodo(1, self._raiz)
        nodo2 = _Nodo(2, self._raiz)
        nodo3 = _Nodo(3, self._raiz)
        nodo4 = _Nodo(4, nodo1)
        nodo5 = _Nodo(5, nodo1)
        nodo6 = _Nodo(6, nodo3)
        nodo7 = _Nodo(7, nodo3)
        nodo8 = _Nodo(8, nodo7)
        nodoNone = _Nodo(None, nodo6)

        nodo1.filhos = [nodo4, nodo5]
        nodo3.filhos = [nodo6, nodo7]
        nodo6.filhos = [nodoNone]
        nodo7.filhos = [nodo8]

        self._raiz.filhos = [nodo1, nodo2, nodo3]


    def __iter__(self):
        return _Iterador(_IteradorPosFixadoNodo(self._raiz))


    def iterPreFixado(self):
        return _Iterador(_IteradorPreFixadoNodo(self._raiz))


    def profundidade(self, item):
        return sum(1 for nodo in self._ancestrais(self._nodo(item).pai))


    def _nodo(self, item):
        for nodo in _IteradorPreFixadoNodo(self._raiz):
            if nodo.item == item:
                return nodo

        raise ItemNaoEncontradoErro


    def _ancestrais(self, nodo):
        """Retorna os ancestrais do nodo, excluindo o própio nodo."""
        while nodo is not None:
            nodo = nodo.pai
            yield nodo


    # TODO refatorar
    def alturaBack(self, item='raiz'):
        """Retorna a altura do item na árvore, se o item não for informado
        será retornada a altura da árvore."""
        if item == 'raiz':
            item = self.raiz()

        nodo = item if isinstance(item, _Nodo) else self._nodo(item)
        alt = 0

        for filho in nodo.filhos:
            alt = max(alt, self.altura(filho))

        return 0 if len(nodo.filhos) == 0 else alt + 1

    def alturaBack2(self, item='raiz'):
        """Retorna a altura do item na árvore, se o item não for informado
        será retornada a altura da árvore."""
        filhos = self._filhos(self.raiz() if item == 'raiz' else item)
        alt = 0

        for filho in filhos:
            alt = max(alt, self.altura(filho))

        return 0 if len(filhos) == 0 else alt + 1

    def altura(self, item='raiz'):
        """Retorna a altura do item na árvore, se o item não for informado
        será retornada a altura da árvore."""
        filhos = self._filhos(self.raiz() if item == 'raiz' else item)

        if len(filhos) == 0:
            return 0
        return max(self.altura(f) for f in filhos) +1


    def _filhos(self, item):
        return item.filhos if isinstance(item, _Nodo) else self._nodo(item).filhos


    def raiz(self):
        return self._raiz.item


class _Nodo:

# TODO entender propriedades no python
    def __init__(self, item, pai=None, *filhos):
        self.item = item
        self.pai = pai
        self.filhos = list(filhos)


class _Iterador:
    """Serve como um encapsulador para _IteradorPosFixadoNodo e
    _IteradorPreFixadoNodo, para entender o funcionamento basta ver o
    código do método __next__."""

    def __init__(self, iterador: '_IteradorPosFixadoNodo | '
                                 '_IteradorPreFixadoNodo'):
        self._iterador = iterador


    def __iter__(self):
        return self


    def __next__(self):
        return next(self._iterador).item


class _IteradorPosFixadoNodo:

    def __init__(self, raiz):
        self._citerador = self._iterador(raiz) # c é de campo, campoiterador


    def __iter__(self):
        return self


    def __next__(self):
        return next(self._citerador)


    def _iterador(self, nodo):
        """O coração do _IteradorPosFixadoNodo."""
        for item in (item for f in nodo.filhos for item in self._iterador(f)):
            yield item

        yield nodo


class _IteradorPreFixadoNodo:

    def __init__(self, raiz):
        self._citerador = self._iterador(raiz) # c é de campo, campoiterador


    def __iter__(self):
        return self


    def __next__(self):
        return next(self._citerador)


    def _iterador(self, nodo):
        """O coração do _IteradorPreFixadoNodo."""
        yield nodo

        for item in (item for f in nodo.filhos for item in self._iterador(f)):
            yield item

