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
        return _IteradorPosFixado(self._raiz)


    def iterPreFixado(self):
        return _IteradorPreFixado(self._raiz)


    def profundidade(self, item):
        nodo = self._nodo(item)
        prof = 0

        while nodo.pai is not None:
            nodo = nodo.pai
            prof += 1

        return prof


    def _nodo(self, item):
        for nodo in _IteradorPreFixadoNodo(self._raiz):
            if nodo.item == item:
                return nodo

        raise ModuleNotFoundError

    def altura(self, item):
        nodo = item if isinstance(item, _Nodo) else self._nodo(item)
        alt = 0

        for filho in nodo.filhos:
            alt = max(alt, self.altura(filho))

        return 0 if len(nodo.filhos) == 0 else alt + 1

class _Nodo:

    def __init__(self, item, pai=None, *filhos):
        self.item = item
        self.pai = pai
        self.filhos = list(filhos)


class _IteradorPosFixado:

    def __init__(self, raiz):
        self._citerador = self._iterador(raiz) # c é de campo, campoiterador


    def __iter__(self):
        return self


    def __next__(self):
        return next(self._citerador)


    def _iterador(self, nodo):
        """O coração do IteradorPosFixado."""
        for item in (item for f in nodo.filhos for item in self._iterador(f)):
            yield item

        yield nodo.item


class _IteradorPreFixado:

    def __init__(self, raiz):
        self._citerador = self._iterador(raiz) # c é de campo, campoiterador


    def __iter__(self):
        return self


    def __next__(self):
        return next(self._citerador)


    def _iterador(self, nodo):
        """O coração do IteradorPosFixado."""
        yield nodo.item

        for item in (item for f in nodo.filhos for item in self._iterador(f)):
            yield item


class _IteradorPosFixadoNodo:

    def __init__(self, raiz):
        self._citerador = self._iterador(raiz) # c é de campo, campoiterador


    def __iter__(self):
        return self


    def __next__(self):
        return next(self._citerador)


    def _iterador(self, nodo):
        """O coração do IteradorPosFixado."""
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
        """O coração do IteradorPosFixado."""
        yield nodo

        for item in (item for f in nodo.filhos for item in self._iterador(f)):
            yield item

