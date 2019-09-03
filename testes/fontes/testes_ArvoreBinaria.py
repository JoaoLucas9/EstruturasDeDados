from pytest import raises
from arvore import ArvoreBinaria, INDEFINIDO
from erros import ItemNaoEncontrado, ParametroNaoInformado, FalhaNaOperacao
from pyext import naoGeraErro


def arvorePronta():
    arv = ArvoreBinaria()
    arv.inserir(0)
    arv.inserir(1, 0)
    arv.inserir(2, 0)
    arv.inserir(3, 1)
    arv.inserir(4, 1)
    arv.inserir(None, 4)
    arv.inserir(5, 2)
    arv.inserir(6, 2)
    arv.inserir(7, 5)

    return arv


arvore = arvorePronta()


def testes_metodo_inserir():
    numeros = ArvoreBinaria()
    numeros.inserir(0)
    numeros.inserir(1, 0)
    numeros.inserir(2, 0)

    assert numeros.filhos(0) == (1, 2)
    assert numeros.pai(1) == numeros.pai(2) == 0

    numeros.inserir(3, 1)
    numeros.inserir(4, 1)

    assert numeros.filhos(1) == (3, 4)
    assert numeros.pai(3) == numeros.pai(4) == 1

    numeros.inserir(None, 4)

    assert numeros.filhos(4) == (None, )
    assert numeros.pai(None) == 4

    numeros.inserir(5, 2)
    numeros.inserir(6, 2)

    assert numeros.filhos(2) == (5, 6)
    assert numeros.pai(5) == numeros.pai(6) == 2


def testes_oMetodo_inserir():
    definiraARaizDaArvoreSeOPaiNaoForInformadoEAArvoreEstiverVazia()
    iraDispararUmErroSeOPaiNaoForInformadoEAArvoreNaoEstiverVazia()
    iraDispararUmErroSeOPaiNaoForLocalizado()
    iraDispararUmErroSeOPaiJaPossuir2Filhos()


def definiraARaizDaArvoreSeOPaiNaoForInformadoEAArvoreEstiverVazia():
    a = ArvoreBinaria()
    a.inserir(0)

    assert a.raiz == 0


def iraDispararUmErroSeOPaiNaoForInformadoEAArvoreNaoEstiverVazia():
    a = ArvoreBinaria()
    a.inserir(0)

    with raises(ParametroNaoInformado):
        a.inserir(1)


def iraDispararUmErroSeOPaiNaoForLocalizado():
    num = ArvoreBinaria()
    num.inserir(0)

    with raises(ItemNaoEncontrado):
        num.inserir(1, 1)


def iraDispararUmErroSeOPaiJaPossuir2Filhos():
    numeros = ArvoreBinaria()
    numeros.inserir(0)
    numeros.inserir(1, 0)
    numeros.inserir(2, 0)

    with raises(FalhaNaOperacao):
        numeros.inserir(3,0)


def testeDoIteradorPosFixado():
    assert [x for x in arvore] == [3, None, 4, 1, 7, 5, 6, 2, 0]


def teste_IteradorPosFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in ArvoreBinaria():
            pass


def testeDoIteradorPreFixado():
    assert [x for x in arvore.preFixado()] == [0, 1, 3, 4, None, 2, 5,
                                               7, 6]


def teste_IteradorPreFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in ArvoreBinaria().preFixado():
            pass


def testeDoIteradorInterFixado():
    assert [x for x in arvore.interFixado()] == [3, 1, None, 4, 0, 7, 5,
                                                 2, 6]


def teste_IteradorInterFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in ArvoreBinaria().interFixado():
            pass


def testes_metodo_altura():
    assert arvore.altura(2) == 2
    assert arvore.altura(None) == 0
    assert arvore.altura(arvore.raiz) == 3


def testes_oMetodo_altura_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.altura(-4)


def testes_metodo_profundidade():
    assert arvore.profundidade(5) == 2
    assert arvore.profundidade(None) == 3
    assert arvore.profundidade(arvore.raiz) == 0


def testes_oMetodo_profundidade_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.profundidade(-9)


def testes_metodo_filhos():
    assert arvore.filhos(1) == (3, 4)
    assert arvore.filhos(None) == tuple()
    assert arvore.filhos(arvore.raiz) == (1, 2)


def testes_oMetodo_filhos_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhos(70)


def testes_metodo_pai():
    assert arvore.pai(4) == 1
    assert arvore.pai(None) == 4
    assert arvore.pai(arvore.raiz) is INDEFINIDO


def testes_oMetodo_pai_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.pai(70)


def testes_daPropiedade_tamanho_aposInserirAlgunsItens():
    numeros = ArvoreBinaria()
    numeros.inserir(0)

    assert numeros.tamanho == 1

    numeros.inserir(1, 0)
    numeros.inserir(2, 0)

    assert numeros.tamanho == 3

    numeros.inserir(3, 1)
    numeros.inserir(4, 1)

    assert numeros.tamanho == 5

    numeros.inserir(None, 4)

    assert numeros.tamanho == 6


def testes_iteradorInterFixadoNodos():
    from arvore import _IteradorInterFixado as Iterador

    assert [nodo.item for nodo in Iterador(arvore._nodo(1))] == [3, 1, None, 4]

    assert [nodo.item for nodo in Iterador(arvore._nodo(2))] == [7, 5, 2, 6]


def testes_metodo_tamanhoSubArvore():
    assert arvore.tamanhoDaSubarvore(2) == 4
    assert arvore.tamanhoDaSubarvore(None) == 1
    assert arvore.tamanhoDaSubarvore(arvore.raiz) == 9


def testes_oMetodo_tamanhoSubArvore_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.tamanhoDaSubarvore(-7)


def testes_metodo_remover():
    numeros = arvorePronta()
    numeros.remover(4)

    assert numeros.filhos(1) == (3, )

    numeros.remover(7)

    assert numeros.filhos(5) == tuple()

    #verificar a estrutura final da árvore
    assert numeros.filhos(0) == (1, 2)
    assert numeros.filhos(1) == (3, )
    assert numeros.filhos(2) == (5, 6)


def testes_metodo_remover_removerARaizDarvore():
    nums = arvorePronta()
    nums.remover(nums.raiz)

    assert nums.raiz is None
    assert nums.vazia


def testes_oMetodo_remover_iraGerarUmErroSeOItemNaoForLocalizado():
    with naoGeraErro():
        arvore.remover(-5)


def testes_daPropiedade_tamanho_aposRemoverAlgunsItens():
    nums = arvorePronta()
    nums.remover(5)

    assert nums.tamanho == 7

    nums.remover(None)

    assert nums.tamanho == 6


def testes_daPropiedade_tamanho_aposRemoverARaiz():
    nums = arvorePronta()
    nums.remover(nums.raiz)

    assert nums.tamanho == 0


def testes_operador_in():
    assert 4 in arvore
    assert None in arvore
    assert arvore.raiz in arvore

