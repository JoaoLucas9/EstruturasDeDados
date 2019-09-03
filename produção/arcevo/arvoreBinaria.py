from erros import ItemNaoEncontrado, ParametroNaoInformado, FalhaNaOperacao
from iteruteis import tamanho as contar

def _itemNaoEncontrado():
    raise ItemNaoEncontrado


def _registrar(filho, pai):
    possui2Filhos = pai.esquerdo is not None and pai.direito is not None

    if possui2Filhos:
        raise FalhaNaOperacao

    if pai.esquerdo is None:
        pai.esquerdo = filho
    else:
        pai.direito = filho

    filho.pai = pai


def _desregistrar(filho, pai):
    if filho is pai.esquerdo:
        pai.esquerdo = None
    else:
        pai.direito = None


def _eUmNodo(obj):
    return isinstance(obj, _Nodo)


class ArvoreBinaria:


    _NAO_ESPECIFICADO = \
        'valor_padrão_para_parâmetros_Recife_PERNAMBUCO 14/06/2019 06:13'


    def __init__(self):
        self._raiz = None
        self._tamanho = 0


    def __iter__(self):
        return _Iterador(_IteradorPosFixado(self._raiz))


    @property
    def raiz(self):
        """Raiz da árvore."""
        return None if self._raiz is None else self._raiz.item

    @property
    def tamanho(self):
        """Quantidade de itens na árvore."""
        return self._tamanho


    def inserir(self, item, pai=_NAO_ESPECIFICADO):
        """Insere o item na árvore.

        Parâmetros
           :param item -> o item que será inserido

           :param pai -> o pai do item, se a árvore estiver vazia ele não
           precisa ser informado, caso contrário, deve ser especificado.
           O pai deve possuir menos de 2 filhos.

        Exceções
           :exception ItemNaoEncontradoErro se o pai não for encontrado na
           árvore.

           :exception ParametroNaoEspecificadoErro se a árvore não estiver
           vazia e o pai não tiver sido informado.

           :exception FalhaNaOperacao se o pai já possuir 2 filhos.
        """
        nodo = _Nodo(item)

        if pai is self._NAO_ESPECIFICADO:
            if not self.vazia():
                raise ParametroNaoInformado('pai')
            self._raiz = nodo
        else:
            _registrar(nodo, self._nodo(pai))

        self._tamanho += 1


    def vazia(self):
        """:return true se a árvore estiver vazia, false caso contrário."""
        return self.raiz is None


    def iterPreFixado(self):
        """Retorna um iterador pré fixado."""
        return _Iterador(_IteradorPreFixado(self._raiz))


    def iterInterFixado(self):
        """Retorna um iterador inter fixado."""
        return _Iterador(_IteradorInterFixado(self._raiz))


    # TODO nodo deve possuir o valor padrão raiz
    def altura(self, item):
        """:return a altura do item na árvore

        Erros
           :exception gera um ItemNaoEncontradoErro se o item não for
           localizado.
        """
        return self._calcularAltura(self._nodo(item))


    def _nodo(self, item, funcao=_itemNaoEncontrado):
        for nodo in _IteradorPosFixado(self._raiz):
            if nodo.item == item:
                return nodo

        return funcao()


    def _calcularAltura(self, nodo):
        #se o nodo ñ possui nenhum filho
        #se os dois filhos forem none
        """Retorna a altura do item na árvore."""
        if nodo.esquerdo is nodo.direito is None:
            return 0
        return max(self._calcularAltura(filho) for filho in _filhos(nodo)) +1


    def profundidade(self, item):
        """:return a profundidade do item.

        Erros
           :exception dispara um ItemNaoEncontradoErro se o item não puder ser
           localizado.
        """
        return contar(self._ancestrais(self._nodo(item)))


    def _ancestrais(self, nodo):
        while nodo.pai is not None:
            nodo = nodo.pai
            yield nodo


    def filhos(self, item):
        """:return os filhos do item.

        Erros
           :exception dispara um ItemNaoEncontradoErro se o item não puder ser
           localizado.
        """
        return tuple(nodo.item for nodo in _filhos(self._nodo(item)))


    def pai(self, item):
        """:return o pai do item.

        Erros
           :exception dispara um ItemNaoEncontradoErro se o item não puder ser
           encontrado.
        """
        return None if item == self.raiz else self._nodo(item).pai.item


    # TODO refatorar
    def remover(self, item):
        """Remove a subarvore enraizada em item.
        Caso o item não seja encontrado, o método retorna normalmente,
        sem gerar erro.
        """
        nodo = self._nodo(item, lambda :'não localizado')

        if nodo is self._raiz:
            self._raiz = None
            self._tamanho = 0
        elif _eUmNodo(nodo):
            tamanho = self.tamanhoSubArvore(item)
            _desregistrar(nodo, nodo.pai)
            self._tamanho -= tamanho


    def tamanhoSubArvore(self, raiz):
        """
        Parâmetros
           :param raiz a raiz da subarvore.

        :return o tamanho da subarvore enraizada em raiz.

        Erros
           :exception dispara um ItemNaoEncontradoErro se o item não for
           localizado.
        """
        return contar(_IteradorPosFixado(self._nodo(raiz)))


class _Nodo:

    def __init__(self, item):
        self.pai = self.esquerdo = self.direito = None
        self.item = item


class _Iterador:
    """Encapsulador para _IteradorPosFixado e _IteradorPreFixado."""

    def __init__(self, iterador):
        self._iteradorNodo = iterador


    def __next__(self):
        return next(self._iteradorNodo).item


    def __iter__(self):
        return self


class _IteradorPosFixado:

    def __init__(self, nodo):
        self._citerador = self._iterador(nodo)

    def __next__(self):
        return next(self._citerador)

    def __iter__(self):
        return self

    def _iterador(self, nodo):
        """O coração do _IteradorPosFixado."""
        for filho in _filhos(nodo):
            for e in self._iterador(filho):
                yield e

        yield nodo


def _filhos(nodo):
    if nodo.esquerdo is not None:
        yield nodo.esquerdo

    if nodo.direito is not None:
        yield nodo.direito


class _IteradorPreFixado:

    def __init__(self, nodo):
        self._citerador = self._iterador(nodo)

    def __next__(self):
        return next(self._citerador)

    def __iter__(self):
        return self

    def _iterador(self, nodo):
        """O coração do _IteradorPreFixado."""
        yield nodo

        for filho in _filhos(nodo):
            for e in self._iterador(filho):
                yield e


class _IteradorInterFixado:

    def __init__(self, nodo):
        self._citerador = self._iterador(nodo)

    def __next__(self):
        return next(self._citerador)

    def __iter__(self):
        return self

    def _iterador(self, nodo):
        """O coração do _IteradorInterFixado."""
        if nodo.esquerdo is not None:
            for n in self._iterador(nodo.esquerdo):
                yield n

        yield nodo

        if nodo.direito is not None:
            for n in self._iterador(nodo.direito):
                yield n


