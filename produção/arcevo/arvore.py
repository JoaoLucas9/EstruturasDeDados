from erros import ItemNaoEncontrado, ParametroNaoInformado, FalhaNaOperacao, \
    ColecaoVazia
from iteruteis import tamanho as contar
from uteis import IteradorVazio

#As árvores não estão preparadas para lidar com itens duplicados
#proxima versão: aprimorar a capacidade delas para lidar com duplicados


def _itemNaoEncontrado():
    raise ItemNaoEncontrado


def _ancestrais(nodo):
    """Retorna os ancestrais do nodo, excluindo o própio nodo."""
    while nodo.pai is not None:
            nodo = nodo.pai
            yield nodo


def _possuiFilhos(nodo):
    return len(nodo.filhos) > 0


def _possui1Filho(nodo):
    return len(nodo.filhos) is 1


def _possui2Filhos(nodo):
    return len(nodo.filhos) is 2


def _permutarNodos(nodo1, nodo2):
        obj = nodo1.item
        nodo1.item = nodo2.item
        nodo2.item = obj

        p = nodo1.prioridade
        nodo1.prioridade = nodo2.prioridade
        nodo2.prioridade = p


def _nodosAncestrais(nodo):
        while nodo.pai is not None:
            nodo = nodo.pai
            yield nodo


_NAO_ESPECIFICADO = 'parâmetro_não_especificado_Recife_PE 16/06/2019 09:54h'
INDEFINIDO = 'indefinido_Recife_PE 29/06/2019 06:13h'
# utilizada para informar que as prioridades de dois itens são iguais
IGUAIS = 'as prioridades são iguais_Recife_PE 01/07/2019 14:42h'
PRETO = 0
VERMELHO = 1


class arvore:
    """Árvore genérica não ordenada."""

    def __init__(self):
        self._raiz = None
        self._tamanho = 0

    @property
    def raiz(self):
        """A raiz da árvore.
        Escrita: ✗
        """

        return None if self._raiz is None else self._raiz.item


    @property
    def tamanho(self):
        """Quantidade de itens na árvore.
        Escrita: ✗
        """
        return self._tamanho


    # TODO refatorar
    def inserir(self, item, pai=_NAO_ESPECIFICADO):
        """Insere o item na árvore.

        Parâmetros
           :param item -> o item que será inserido

           :param pai -> o pai do item, se a árvore estiver vazia ele não
           precisa ser informado, caso contrário, deve ser especificado.

        Exceções
           :exception ItemNaoEncontradoErro se o pai não for encontrado na
           árvore.

           :exception ParametroNaoEspecificadoErro se a árvore não estiver
           vazia e o pai não tiver sido informado.
        """
        nodo = _Nodo(item)

        if pai is _NAO_ESPECIFICADO:
            if not self.vazia:
                raise ParametroNaoInformado('pai')
            self._raiz = nodo
        else:
            pai = self._nodo(pai)
            pai.filhos.append(nodo)
            nodo.pai = pai

        self._tamanho += 1


    @property
    def vazia(self):
        return self._raiz is None


    def __iter__(self):
        """Retorna um iterador pós fixado."""
        if self.vazia:
            return IteradorVazio()
        return _Iterador(_IteradorPosFixado(self._raiz))


    def preFixado(self):
        """Retorna um iterador pré fixado."""
        if self.vazia:
            return IteradorVazio()
        return _Iterador(_IteradorPreFixado(self._raiz))


    def profundidade(self, item):
        return contar(_ancestrais(self._nodo(item)))


    def _nodo(self, item, funcao=_itemNaoEncontrado):
        """Procura por um nodo cujo item seja igual ao parâmetro item.

        Parâmetros
           :param item o alvo desta operação

           :param funcao a função que será invocada caso nehum nodo seja
           encontrado.

        :return o nodo encontrado.
        Caso nenhum nodo seja encontrado, então retorna-se o resultado da
        função, 'return funcao()'.
        Pode-se retornar um valor padrão ou gerar um erro, por exemplo.
        """
        for nodo in _IteradorPreFixado(self._raiz):
            if nodo.item == item:
                return nodo

        return funcao()


    def altura(self, item='raiz'):
        """Retorna a altura do item na árvore, se o item não for informado
        será retornada a altura da árvore."""
        filhos = self._filhos(self.raiz if item == 'raiz' else item)

        if len(filhos) == 0:
            return 0
        return max(self.altura(f) for f in filhos) +1


    def _filhos(self, item):
        if isinstance(item, _Nodo):
            return item.filhos
        return self._nodo(item).filhos


    def pai(self, item):
        """Retorna o pai de um item.

        Erros
           :exception ItemNaoEncontradoErro se o item não for encontrado
        """
        return INDEFINIDO if item == self.raiz else self._nodo(item).pai.item


    def filhos(self, item):
        """Retorna os filhos de um item.
        :exception ItemNaoEncontradoErro se o item não for encontrado
        """
        return tuple(nodo.item for nodo in self._nodo(item).filhos)


    def remover(self, item):
        """Remove a subarvore enraizada em item.
        Caso o item não seja encontrado, o método retorna normalmente,
        sem gerar erro.
        """
        nodo = self._nodo(item, lambda : 'não encontrado')

        if nodo is self._raiz:
            self._raiz = None
            self._tamanho = 0
        elif nodo != 'não encontrado':
            quantidadeDeItensRemovidos = self.tamanhoDaSubarvore(item)
            pai = nodo.pai
            pai.filhos.remove(nodo)
            nodo.pai = None
            self._tamanho -= quantidadeDeItensRemovidos


    # TODO informar a quantidade de filhos q um item deve ter p/ o met
    #  rtornar true
    def possuiFilhos(self, item):
        """Retorna true se o item possuir filhos, false caso contrário.
        Exceções
           :exception ItemNaoEncontradoErro se o item não for encontrado.
        """
        return len(self._nodo(item).filhos) > 0


    def tamanhoDaSubarvore(self, raiz):
        """Retorna o tamanho da subarvore enraizada em raiz.
        Exceções
           :exception ItemNaoEncontradoErro se o item não for encontrado.
        """
        return contar(_IteradorPreFixado(self._nodo(raiz)))


    def nivel(self, d):
        """Itera pelos nodos do nível d da árvore.

        :return um iterador que itera por todos os nodos no nível d.
        """
        return _Iterador(_IteradorPorNivel(self._raiz, d))


class _Nodo:

    def __init__(self, item, pai=None):
        self.item = item
        self.pai = pai
        self.filhos = []


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


class _IteradorPosFixado:

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


class _IteradorPorNivel:
    """Itera pelos nodos de uma árvore que estão em um nível específico."""

    # TODO se o nível for negativo então todos os nodos serão visitados,
    #  o que é um grande erro
    def __init__(self, raiz, nivel):
        """:param raiz : _Nodo a raiz de uma árvore.
        :param nivel : int nível da árvore que será percorrido.
        """
        self._citerador = self._iterador(raiz, 0) # c é de campo, campoiterador
        self._NIVEL = nivel


    def __iter__(self):
        return self


    def __next__(self):
        return next(self._citerador)


    def _iterador(self, nodo, nivelAtual):
        """O coração do _IteradorPorNivel.
        O principal requisito deste método é que ele seja otimizado para
        processar apenas os nodos de um determinado nível de uma árvore, a
        idéia é, se o nível do nodo atual é menor que o nível desejado então
        continuar descendo até chegar no nível que se deseja, se o nível no
        qual o nodo está é igual ao nível desejado, então retornar o nodo.
        A otimização deste método decorre principalmente do fato de que se
        evita descender para níveis além do desejado, exemplo, se um ou mais
        nodos estão no nível 10 mas deseja-se apenas os nodos do nível 2,
        então este método não deverá nem mesmo chegar aos nodos dos níveis
        3, 4, 5 ... evitando assim processamento desnecessário e
        economizado tempo.
        """
        if nivelAtual == self._NIVEL:
            yield nodo

        for n in (n for filho in nodo.filhos for n in self._iterador(filho,
                                                                 nivelAtual +1)):
            yield n


class _IteradorPreFixado:

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


class ArvoreBinaria(arvore):
    """Árvore binária não ordenada."""


    def __init__(self):
        super().__init__()


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
        if pai != _NAO_ESPECIFICADO and len(super().filhos(pai)) == 2:
            raise FalhaNaOperacao(f'{pai} já possui 2 filhos.')
        super().inserir(item, pai)


    def interFixado(self):
        """Retorna um iterador inter fixado."""
        if self.vazia:
            return IteradorVazio()
        return _Iterador(_IteradorInterFixado(self._raiz))


class _IteradorInterFixado:

    def __init__(self, nodo):
        self._citerador = self._iterador(nodo)


    def __next__(self):
        return next(self._citerador)


    def __iter__(self):
        return self


    # TODO retornar tupla
    def _iterador(self, nodo):
        """O coração do _IteradorInterFixado."""
        esquerdo = self._esquerdo(nodo)
        direito =  self._direito(nodo)

        if  esquerdo is not None:
            for n in self._iterador(esquerdo):
                yield n

        yield nodo

        if direito is not None:
            for n in self._iterador(direito):
                yield n


    def _esquerdo(self, nodo):
        if isinstance(nodo, _Nodo):
            return nodo.filhos[0] if len(nodo.filhos) >= 1 else None
        return nodo.esquerdo

    def _direito(self, nodo):
        if isinstance(nodo, _Nodo):
            return nodo.filhos[1] if len(nodo.filhos) == 2 else None
        return nodo.direito


class Heap:
    """Ordem do heap: para qualquer item i da árvore, o pai de i terá uma
    prioridade maior igual a de i. O elemento no topo do heap é o de mais
    alta prioridade, e a medida que vamos descendo pelo heap as prioridades
    vão diminuindo (ou pelo menos se manterão constante).
    É possível associar uma prioridade (explicitamente), a cada item na
    árvore, contudo ressalta-se que não é obrigatório (ver método inserir).
    """


    def __init__(self, comparador):
        """
        Parâmetros:
           :param comparador deve receber dois objetos e determinar qual
           deles possui a maior prioridade. Os objetos informados serão os
           própios itens se no momento de inseri-los não forem informadas,
           explicitamente, suas prioridades, caso elas sejam, então estes
           objetos 'prioridade' serão informados.
        """
        self._raiz = None
        self._maior = comparador
        self._tamanho = 0


    @property
    def topo(self):
        """A raiz da árvore.
        Escrita: ✗

        Erro
           :exception FalhaNaOperacao se o heap estiver vazio.
        """
        if self.vazio:
            raise FalhaNaOperacao('O heap está vazio.')
        return self._raiz.item


    @property
    def niveis(self):
        """O total de níveis que a árvore possui.
        Escrita: ✗
        """
        niveis = 0
        nodo = self._raiz

        while nodo is not None:
            niveis += 1
            nodo = None if len(nodo.filhos) is 0 else nodo.filhos[0]

        return niveis


    @property
    def ultimoNivel(self):
        """Último nível da árvore, se ela estiver vazia então o seu valor será
        arvore.INDEFINIDO.
        Escrita: ✗
        """
        return INDEFINIDO if self.vazio else self.niveis - 1


    @property
    def vazio(self):
        """True se o heap estiver vazio, false caso contrário.
        Escrita: ✗
        """
        return self.tamanho is 0


    @property
    def tamanho(self):
        """Quantidade de itens na árvore.
        Escrita: ✗
        """
        return self._tamanho


    def inserir(self, item, prioridade=_NAO_ESPECIFICADO):
        """Insere o item na árvore.
        As prioridades dos itens podem ser configuradas explicitamente,
        se este for o caso, então os objetos que representam os objetos
        'prioridade' serão informados ao comparador, se as prioridades não
        forem informadas, então os própios itens serão passados ao comparador,
        que, em qualquer um dos casos, deverá retornar o objeto de maior
        prioridade.

        Parâmetros
           :param item o item que será inserido na árvore, sua localização
           depende de sua prioridade.

           :param prioridade a prioridade do item, opcional.
        """
        nodo = self._nodoPrioritario(item, prioridade)

        if self.vazio:
            self._raiz = nodo
        else:
            self._inserirNodoNaArvore(nodo, self._econtrarLocalDeInsercao())
            self._upHeapBubbling(nodo)

        self._tamanho += 1


    def _nodoPrioritario(self, item, prioridade):
        nodo = _Nodo(item)
        nodo.prioridade = item if prioridade == _NAO_ESPECIFICADO else prioridade

        return nodo


    def _inserirNodoNaArvore(self, nodo, pai):
        pai.filhos.append(nodo)
        nodo.pai = pai


    def _econtrarLocalDeInsercao(self):
        for nodo in _IteradorPorNivel(self._raiz, self.ultimoNivel - 1):
            if not _possui2Filhos(nodo):
                return nodo

        return self._extremaEsquerda()


    def __iter__(self):
        if self.vazio:
            return IteradorVazio()
        return _Iterador(_IteradorPosFixado(self._raiz))


    def preFixado(self):
        """Retorna um iterador pré fixado."""
        if self.vazio:
            return IteradorVazio()
        return _Iterador(_IteradorPreFixado(self._raiz))


    def interFixado(self):
        """Retorna um iterador inter fixado."""
        if self.vazio:
            return IteradorVazio()
        return _Iterador(_IteradorInterFixado(self._raiz))


    def pai(self, item):
        """Retorna o pai do item.

        :return arvore.INDEFINIDO se o item for a raiz da árvore.

        Exceções
           :exception ItemNaoEncontradoErro se o item não for encontrado
        """
        return INDEFINIDO if item == self.topo else self._nodo(item).pai.item


    def _nodo(self, item, funcao=_itemNaoEncontrado):
        """Procura por um nodo cujo item seja igual ao parâmetro item.

        Parâmetros
           :param item o alvo desta operação

           :param funcao a função que será invocada caso nenhum nodo seja
           encontrado.

        :return o nodo encontrado.
        Caso nenhum nodo seja encontrado, então retorna-se o resultado da
        função, 'return funcao()'.
        Pode-se retornar um valor padrão ou gerar um erro, por exemplo.
        """
        for nodo in _IteradorPreFixado(self._raiz):
            if nodo.item == item:
                return nodo

        return funcao()


    def filhos(self, item):
        """Retorna os filhos de um item.
        :exception ItemNaoEncontradoErro se o item não for encontrado
        """
        return tuple(nodo.item for nodo in self._nodo(item).filhos)


    def _extremaEsquerda(self):
        """Descer o máximo que puder e retornar o _Nodo que está lá na
        extrema esquerda."""
        # TODO iteradortinterfixado deve ser melhor
        return next(_IteradorPosFixado(self._raiz))


    def _upHeapBubbling(self, nodo):
        for anc in _nodosAncestrais(nodo):
            if self._maior(nodo.prioridade, anc.prioridade) is nodo.prioridade:
                _permutarNodos(nodo, anc)
                nodo = anc


    def ancestrais(self, item):
        """Retorna um iterador que percorre o caminho item-raiz, visitando
        todos os ancestrais do item, excluindo o própio item.

        Erros
           :exception ItemNaoEncontrado caso o item não seja encontrado.
        """
        return (nodo.item for nodo in _nodosAncestrais(self._nodo(item)))


    def remover(self):
        """Remove o item que está no topo do heap.

        Erro
           :exception FalhaNaOperacao se o heap estiver vazio.
        """
        item = self.topo
        nodo = self._desligarDaArvore(self._ultimoNodoDaArvore())

        if self._raiz is not None:
            _permutarNodos(self._raiz, nodo)
            self._downHeapBubbling(self._raiz)

        self._tamanho -= 1

        return item


    def _ultimoNodoDaArvore(self):
        nodo = None
        for nodo in _IteradorPorNivel(self._raiz, self.ultimoNivel):
            pass

        return nodo


    def _desligarDaArvore(self, nodo):
        if nodo is self._raiz:
            self._raiz = None
        else:
            nodo.pai.filhos.remove(nodo)

        return nodo


    def _downHeapBubbling(self, nodo):
        if not _possuiFilhos(nodo):
            return

        filho = self._filhoComPrioridadeMaisAlta(nodo)
        if self._maior(filho.prioridade, nodo.prioridade) is filho.prioridade:
            _permutarNodos(nodo, filho)
            self._downHeapBubbling(filho)


    def _filhoComPrioridadeMaisAlta(self, nodo):
        if _possui1Filho(nodo):
            return nodo.filhos[0]

        esquerdo = nodo.filhos[0]
        direito = nodo.filhos[1]
        comparacao = self._maior(esquerdo.prioridade, direito.prioridade)

        if comparacao == esquerdo.prioridade or comparacao == IGUAIS:
            return esquerdo
        return direito


    def quantidadeDeFilhos(self, item):
        """Retorna a quantidade de filhos do item.

        Erros
           :exception ItemNaoEncontrado se o item não for encontrado.
        """
        return len(self._nodo(item).filhos)


class ArvoreAVL:


    def __init__(self, comparador):
        """
        Parâmetros
            :param comparador Callable capaz de comparar dois itens
            quaisquer da árvore. Deve retornar o maior deles ou a constante
            arvore.IGUAIS se os valores comparados forem iguais."""
        self._raiz = None
        self._maior = comparador
        self._tamanho = 0


    @property
    def raiz(self):
        """Raiz da árvore.
        Escrita: ✗
        """
        return self._raiz.item


    @property
    def tamanho(self):
        """Tamanho da árvore.
        Escrita: ✗
        """
        return self._tamanho

    @property
    def vazia(self):
        """True se a árvore estiver vazia, false caso contrário.
        Escrita: ✗
        """
        return self._tamanho is 0


    def inserir(self, item):
        """Insere o item na árvore."""
        nodo = _NodoBin(item)

        if self.vazia:
            self._raiz = nodo
        else:
            self._registrarFilho(nodo, self._localDeInsercao(item, self._raiz))
            z = self._primeiroNodoDesbalanceado(nodo)
            if z is not None:
                self._rebalancear(z)

        self._tamanho += 1


    def _registrarFilho(self, nodo, pai):
        if self._maior(pai.item, nodo.item) is nodo.item:
            pai.direito = nodo
        else:
            pai.esquerdo = nodo

        nodo.pai = pai


    def _localDeInsercao(self, item, nodo):
        if self._maior(nodo.item, item) is item:
            if nodo.direito is None:
                return nodo
            return self._localDeInsercao(item, nodo.direito)

        elif nodo.esquerdo is None:
            return nodo
        else:
            return self._localDeInsercao(item, nodo.esquerdo)


    def _primeiroNodoDesbalanceado(self, nodo):
        for nodo in _ancestrais(nodo):
            if self._desbalanceado(nodo):
                return nodo

        return None


    def _desbalanceado(self, nodo):
        filhos = nodo.esquerdo, nodo.direito

        alturaEsquerdo = -1 if filhos[0] is None else self._altura(filhos[0])
        alturaDireito = -1 if filhos[1] is None else self._altura(filhos[1])

        return abs(alturaEsquerdo - alturaDireito) > 1


    # O rebalanceamento utilizado  está descrito no livro "Estruturas de
    # Dados e Algoritmos em Java", de Goodrich e Tamassia, 5ª edição
    # capítulo 10, seção 10.2.1, página 449
    # TODO refatorar
    def _rebalancear(self, z):
        y = self._filhoMaisAlto(z)
        x = self._filhoMaisAlto(y)
        a, b, c = self._abc(z, y, x)
        t1, t2 = self._t1t2(a, b, c)

        b.esquerdo, b.direito = a, c
        if z is self._raiz:
            self._raiz = b
            b.pai = None
        else:
            self._registrarFilho(b, z.pai)

        a.pai = c.pai = b
        if t1 is not None:
            t1.pai = a

        if t2 is not None:
            t2.pai = c

        a.direito = t1
        c.esquerdo = t2

        return b


    def _filhoMaisAlto(self, nodo):
        """Dentre os filhos do nodo, retorna o mais alto, caso ambos possuam a
        mesam altura retorna o filho no mesmo lado do pai, ou seja, se p for o
        pai do nodo e p por sua vez é um filho a esquerda de um outro nodo,
        então este método retorna o filho a esquerda do nodo, caso p seja um
        filho a direita de um outro nodo, esntão este método retorna o
        filho a direita do nodo."""
        filhos = nodo.esquerdo, nodo.direito

        alturaEsquerdo = -1 if filhos[0] is None else self._altura(filhos[0])
        alturaDireito = -1 if filhos[1] is None else self._altura(filhos[1])

        if alturaEsquerdo == alturaDireito and nodo.pai is not None:
            pai = nodo.pai
            return nodo.esquerdo if pai.esquerdo is nodo else nodo.direito

        return filhos[0] if alturaEsquerdo > alturaDireito else filhos[1]


    def _abc(self, z, y, x):
        if y is z.direito and x is y.direito:
            return z, y, x

        if y is z.esquerdo and x is y.esquerdo:
            return x, y, z

        if y is z.direito and x is y.esquerdo:
            return z, x, y
        return y, x, z


    def _t1t2(self, a, b, c):
        t1 = a.direito if a is b.esquerdo else b.esquerdo
        t2 = c.esquerdo if c is b.direito else b.direito

        return t1, t2


    def _nodo(self, item, funcao=_itemNaoEncontrado):
        nodo = self._raiz

        while nodo is not None:
            if self._saoIguais(nodo.item, item):
                return nodo

            if self._maior(nodo.item, item) is item:
                nodo = nodo.direito
            else:
                nodo = nodo.esquerdo

        return funcao()


    def _saoIguais(self, item1, item2):
        return self._maior(item1, item2) is IGUAIS


    def pai(self, item):
        """Retorna o pai de um item.

        Erros
           :exception ItemNaoEncontradoErro se o item não for encontrado
        """
        nodo = self._nodo(item)

        return INDEFINIDO if nodo is self._raiz else nodo.pai.item


    def filhos(self, item):
        """Retorna os filhos de um item.

        Erros
           :exception ItemNaoEncontradoErro se o item não for encontrado
        """
        return tuple(nodo.item for nodo in self._nodo(item).filhos)


    def __iter__(self):
        """Retorna um iterador pós fixado."""
        if self.vazia:
            return IteradorVazio()
        return _Iterador(_IteradorPosFixado(self._raiz))


    def preFixado(self):
        """Retorna um iterador pré fixado."""
        if self.vazia:
            return IteradorVazio()
        return _Iterador(_IteradorPreFixado(self._raiz))


    def interFixado(self):
        """Retorna um iterador inter fixado."""
        if self.vazia:
            return IteradorVazio()
        return _Iterador(_IteradorInterFixado(self._raiz))


    def menor(self):
        """Retorna o menor item da árvore.

        Erros
           :exception ColecaoVazia se a árvore estiver vazia
        """
        if self.vazia:
            raise ColecaoVazia('A árvore está vazia.')

        nodo = self._raiz
        while nodo.esquerdo is not None:
            nodo = nodo.esquerdo

        return nodo.item


    def maior(self):
        """Retorna o maior item da árvore.

        Erros
            :exception ColecaoVazia se a árvore estiver vazia
        """
        if self.vazia:
            raise ColecaoVazia('A árvore está vazia.')

        nodo = self._raiz
        while nodo.direito is not None:
            nodo = nodo.direito

        return nodo.item


    def __contains__(self, item):
        """Determina se um item está presente na árvore.

        :return true se o item for localizado, false caso contrário.
        """
        return self._nodo(item, lambda : None) is not None


    def ancestrais(self, item):
        """Retorna um iterador que percorre o caminho item-raiz, visitando
        todos os ancestrais do item, excluindo o própio item.

        Erros
           :exception ItemNaoEncontrado caso o item não seja encontrado.
        """
        return (ancestral.item for ancestral in _ancestrais(self._nodo(item)))


    def altura(self, item=INDEFINIDO):
        """Retorna a altura do item na árvore ou a altura da árvore se o
        item não for informado.

        Erro
           :exception ItemNaoEncontrado se o item não for localizado
        """
        if item is INDEFINIDO:
            return self._altura(self._raiz)
        return self._altura(self._nodo(item))



    def _altura(self, nodo):
        if not _possuiFilhos(nodo):
            return 0
        return max(self._altura(n) for n in nodo.filhos) +1



    def remover(self, item):
        """Remove o item da árvore.

        Erro
           :exception ItemNaoEncontrado se o item não for localizado.
        """
        nodo = self._nodo(item)

        if nodo is self._raiz and not _possui2Filhos(nodo):
            self._removerRaiz()
        else:
            nodo = self._primeiroNodoDesbalanceado(self._remover(nodo))
            while nodo is not None:
                nodo = self._primeiroNodoDesbalanceado(self._rebalancear(nodo))

        self._tamanho -= 1


    def _removerRaiz(self):
        """A raiz deve possuir 0 ou 1 filho.
        Este método não deve ser utilizado caso a raiz possua 2 filhos.
        """
        if not _possuiFilhos(self._raiz):
            self._raiz = None
        else: # considera-se que possui apenas um filho
            self._raiz = self._filho(self._raiz)
            self._raiz.pai = INDEFINIDO


    def _remover(self, nodo):
        if not _possuiFilhos(nodo):
            self._desligarDaArvore(nodo)
        elif _possui1Filho(nodo):
            self._registrarFilho(self._filho(nodo), nodo.pai)
        else:
            y = self._extremaEsquerda(nodo.direito)
            nodo.item = y.item
            return self._remover(y)
        return nodo


    def _filho(self, nodo):
        return nodo.esquerdo if nodo.esquerdo is not None else nodo.direito


    def _extremaEsquerda(self, nodo):
        """Descer o máximo que puder e retornar o _Nodo que está lá na
        extrema esquerda."""
        return next(_IteradorInterFixado(nodo))


    def _desligarDaArvore(self, nodo):
        if nodo is self._raiz:
            self._raiz = None
        else:
            pai = nodo.pai
            setattr(pai, 'esquerdo' if pai.esquerdo is nodo else 'direito', None)


    def filhoEsquerdo(self, item):
        """Retorna o filho a esquerda do item.

        Erros
           :exception ItemNaoEncontrado se o item não for localizado.

           :exception FalhaNaOperacao se o item não possuir um filho a
           esquerda.
        """
        nodo = self._nodo(item).esquerdo

        if nodo is None:
            raise FalhaNaOperacao(f'{item} não possui filho a esquerda.')
        return nodo.item


    def filhoDireito(self, item):
        """Retorna o filho a direita do item.

        Erros
            :exception ItemNaoEncontrado se o item não for localizado.

            :exception FalhaNaOperacao se o item não possuir um filho a
            direita.
        """
        nodo = self._nodo(item).direito

        if nodo is None:
            raise FalhaNaOperacao(f'{item} não possui filho a direita.')
        return nodo.item


class _NodoBin:

    def __init__(self, item, pai=None, esquerdo=None, direito=None):
        self.item = item
        self.pai = pai
        self.esquerdo = esquerdo
        self.direito = direito


    @property
    def filhos(self):
        if self.esquerdo is not None and self.direito is not None:
            return self.esquerdo, self.direito
        if self.esquerdo is None and self.direito is None:
            return tuple()
        return self.esquerdo if self.esquerdo is not None else self.direito,


class ArvoreVP:


    def __init__(self, comparador):
        self._raiz = None
        self._maior = comparador
        self._tamanho = 0


    @property
    def raiz(self):
        """Raiz da árvore.
        Escrita: ✗
        """
        return self._raiz.item


    @property
    def vazia(self):
        return self._raiz is None


    @property
    def tamanho(self):
        return self._tamanho


    @property
    def itensSemFilhos(self):
        """Iterador que percorre todos os itens da árvore que não possuem
        filhos."""
        return (nodo.item for nodo in self._nodosExternos())


    def _nodosExternos(self):
        if self.vazia:
            return IteradorVazio()
        iter = _IteradorPosFixado(self._raiz)

        return (nodo for nodo in iter if not _possuiFilhos(nodo))


    def inserir(self, item):
        nodo = _NodoBin(item)

        if self.vazia:
            self._raiz = nodo
            nodo.cor = PRETO
        else:
            nodo.cor = VERMELHO
            self._registrarFilho(nodo, self._localDeInsercao(item, self._raiz))

            while nodo.cor is VERMELHO and nodo.pai.cor is VERMELHO:
                nodo = self._reequilibrarArvore(nodo)

        self._tamanho += 1


    def _localDeInsercao(self, item, nodo):
        if self._maior(nodo.item, item) is item:
            if nodo.direito is None:
                return nodo
            return self._localDeInsercao(item, nodo.direito)

        elif nodo.esquerdo is None:
            return nodo
        else:
            return self._localDeInsercao(item, nodo.esquerdo)


    def _registrarFilho(self, nodo, pai):
        if self._maior(pai.item, nodo.item) is nodo.item:
            pai.direito = nodo
        else:
            pai.esquerdo = nodo

        nodo.pai = pai


    def _reequilibrarArvore(self, z):
        u, v = z.pai.pai, z.pai
        w = u.direito if v is u.esquerdo else u.esquerdo

        if w is not None and w.cor is VERMELHO:
            corU = VERMELHO if u is not self._raiz else PRETO
            self._recolorirN({u: corU, v: PRETO, w: PRETO})
            return u
        else:
            b = self._reestruturar(u, v, z)
            self._recolorirN({b: PRETO, b.esquerdo:VERMELHO, b.direito:VERMELHO})
            return b


    def _recolorir(self, u, v, w):
        if u is not self._raiz:
            u.cor = VERMELHO
        v.cor = w.cor = PRETO

        return u


    def _reestruturar(self, u, v, z):
        a, b, c = self._abc(u, v, z)
        t1, t2 = self._t1t2(a, b, c)

        b.esquerdo, b.direito = a, c
        if u is self._raiz:
            self._raiz = b
            b.pai = None
        else:
            self._registrarFilho(b, u.pai)

        a.pai = c.pai = b
        if t1 is not None:
            t1.pai = a

        if t2 is not None:
            t2.pai = c

        a.direito = t1
        c.esquerdo = t2

        # b.cor = PRETO
        # a.cor = c.cor = VERMELHO

        return b


    def _abc(self, u, v, z):
        """
        :param u pai de v
        :param v pai de z
        """
        if v is u.direito and z is v.direito:
            return u, v, z

        if v is u.esquerdo and z is v.esquerdo:
            return z, v, u

        if v is u.direito and z is v.esquerdo:
            return u, z, v
        return v, z, u


    def _t1t2(self, a, b, c):
        t1 = a.direito if a is b.esquerdo else b.esquerdo
        t2 = c.esquerdo if c is b.direito else b.direito

        return t1, t2


    def __iter__(self):
        """Retorna um iterador pós fixado."""
        if self.vazia:
            return IteradorVazio()
        return _Iterador(_IteradorPosFixado(self._raiz))


    def preFixado(self):
        """Retorna um iterador pré fixado."""
        if self.vazia:
            return IteradorVazio()
        return _Iterador(_IteradorPreFixado(self._raiz))


    def interFixado(self):
        """Retorna um iterador inter fixado."""
        if self.vazia:
            return IteradorVazio()
        return _Iterador(_IteradorInterFixado(self._raiz))


    def _nodo(self, item, funcao=_itemNaoEncontrado):
        nodo = self._raiz

        while nodo is not None:
            if self._saoIguais(nodo.item, item):
                return nodo

            if self._maior(nodo.item, item) is item:
                nodo = nodo.direito
            else:
                nodo = nodo.esquerdo

        return funcao()


    def _saoIguais(self, valor1, valor2):
        return self._maior(valor1, valor2) is IGUAIS


    # aprimorado
    def pai(self, item):
        """Retorna o pai de um item.

        Erros
           :exception ItemNaoEncontradoErro se o item não for encontrado
        """
        nodo = self._nodo(item)

        return INDEFINIDO if nodo.pai is None else nodo.pai.item


    def filhos(self, item):
        """Retorna os filhos de um item.

        Erros
           :exception ItemNaoEncontradoErro se o item não for encontrado
        """
        return tuple(nodo.item for nodo in self._nodo(item).filhos)


    def filhoEsquerdo(self, item):
        """Retorna o filho a esquerda do item.

        Erros
           :exception ItemNaoEncontrado se o item não for localizado.

           :exception FalhaNaOperacao se o item não possuir um filho a
           esquerda.
        """
        nodo = self._nodo(item).esquerdo

        if nodo is None:
            raise FalhaNaOperacao(f'{item} não possui filho a esquerda.')
        return nodo.item


    def filhoDireito(self, item):
        """Retorna o filho a direita do item.

        Erros
           :exception ItemNaoEncontrado se o item não for localizado.

           :exception FalhaNaOperacao se o item não possuir um filho a
           direita.
        """
        nodo = self._nodo(item).direito

        if nodo is None:
            raise FalhaNaOperacao(f'{item} não possui filho a direita.')
        return nodo.item


    def cor(self, item):
        """Retorna a cor de um item na árvore.

         Erros
           :exception ItemNaoEncontrado se o item não for localizado.
        """
        return self._nodo(item).cor


    def __contains__(self, item):
        return self._nodo(item, lambda : None) is not None


    def profundidadePreta(self, item):
        """Retorna a profundidade preta do item.

        Erros
           :exception dispara um ItemNaoEncontradoErro se o item não for
           localizado.
        """
        nodo = self._nodo(item)

        if nodo.cor is PRETO:
            return sum(1 for n in _ancestrais(nodo) if n.cor is PRETO)
        return sum(1 for n in _ancestrais(nodo) if n.cor is PRETO) -1


    def remover(self, item):
        self._remover(self._nodo(item))


    def _remover(self, nodo):
        if not _possuiFilhos(nodo):
            self._desligarDaArvore(nodo)

            if nodo.cor is PRETO:
                self._resolverDuploPreto(nodo.pai)
        elif _possui1Filho(nodo):
            f = nodo.esquerdo if nodo.direito is None else nodo.direito
            self._registrarFilho(f, nodo.pai)

            if nodo.cor is VERMELHO or f.cor is VERMELHO:
                f.cor = PRETO
        else:
            f = self._extremaEsquerda(nodo.direito)
            self._desligarDaArvore(f)
            nodo.item = f.item

            if f.direito is not None:
                self._registrarFilho(f.direito, f.pai)


    def _desligarDaArvore(self, nodo):
        pai = nodo.pai
        setattr(pai, 'esquerdo' if nodo is pai.esquerdo else 'direito', None)


    def _extremaEsquerda(self, nodo):
        return next(_IteradorInterFixado(nodo))


    def _resolverDuploPretoOriginal(self, x):
        """:param x pai do duplo preto"""
        y = x.esquerdo if x.direito is None else x.direito
        if not _possuiFilhos(y): # trata do caso 2
            y.cor = VERMELHO

            # já sei que x é vermelho, contudo x pode ser preto, neste caso o
            # tratamento é diferente, este código deve ser aprimorado
            x.cor = PRETO
        elif _possui1Filho(y): # assume-se que o filho é vermelho, aprimorar
            filho = y.esquerdo if y.direito is None else y.direito
            # salvar a cor do x agora na variavel 'c'
            # b = self.reestruturar(params)
            # b.cor = c
            self._reequilibrarArvoreRemocao(filho)
        elif y.cor is VERMELHO:
            self._ajustarArvore(x, y)


    def _resolverDuploPreto(self, x):
        """:param x pai do duplo preto"""
        y = x.esquerdo if x.direito is None else x.direito

        if not _possuiFilhos(y):
            y.cor = VERMELHO
            x.cor = PRETO
        elif _possui1Filho(y): # assume-se que o filho é vermelho
            z = y.esquerdo if y.direito is None else y.direito
            # c = x.cor
            b = self._reestruturar(x, y, z)
            self._recolorirN({b:x.cor, b.esquerdo:PRETO, b.direito:PRETO})
            # b.cor = c
            # b.esquerdo.cor = b.direito.cor = PRETO
        elif y.cor is VERMELHO:
            self._ajustarArvore(x, y)


    def _reequilibrarArvoreRemocao(self, z): # trata do caso 1
        y, x = z.pai, z.pai.pai
        a, b, c = self._abc(x, y, z)
        t1, t2 = self._t1t2(a, b, c)

        b.esquerdo, b.direito = a, c
        # if u is self._raiz:
        #     self._raiz = b
        #     b.pai = None
        # else:
        self._registrarFilho(b, x.pai)

        a.pai = c.pai = b
        if t1 is not None:
            t1.pai = a

        if t2 is not None:
            t2.pai = c

        a.direito = t1
        c.esquerdo = t2

        b.cor = x.cor
        a.cor = c.cor = PRETO


    def _ajustarArvore(self, x, y): # trata do caso 3
        z = y.direito if y is x.direito else y.esquerdo
        # c = z.cor
        b = self._reestruturar(x, y, z)
        self._recolorirN({y:PRETO, x: VERMELHO})
        # y.cor = PRETO
        # x.cor = VERMELHO
        # z.cor = c

        self._resolverDuploPreto(x)


    def _recolorirN(self, nodo_cor):# o N serve apenas para diferenciar do
        # antigo recolorir
        for nodo, cor in nodo_cor.items():
            nodo.cor = cor

