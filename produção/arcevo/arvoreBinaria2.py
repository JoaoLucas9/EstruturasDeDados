from arvore import arvore, _Iterador
from erros import FalhaNaOperacao

class ArvoreBinaria(arvore):


    _NAO_ESPECIFICADO = -2


    def __init__(self):
        super().__init__()
        # self._NAO_ESPECIFICADO = super()._NAO_ESPECIFICAO


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
        if pai != self._NAO_ESPECIFICADO and len(super().filhos(pai)) == 2:
            raise FalhaNaOperacao
        super().inserir(item, pai)


    def iterInterFixado(self):
        """Retorna um iterador inter fixado."""
        return _Iterador(_IteradorInterFixado(self._raiz))


class _IteradorInterFixado:

    def __init__(self, nodo):
        self._citerador = self._iterador(nodo)


    def __next__(self):
        return next(self._citerador)


    def __iter__(self):
        return self

    # TODO refatorar
    def _iterador(self, nodo):
        """O coração do _IteradorInterFixado."""
        esquerdo =  nodo.filhos[0] if len(nodo.filhos) >= 1 else None
        direito =  nodo.filhos[1] if len(nodo.filhos) == 2 else None

        if  esquerdo is not None:
            for n in self._iterador(esquerdo):
                yield n

        yield nodo

        if direito is not None:
            for n in self._iterador(direito):
                yield n
