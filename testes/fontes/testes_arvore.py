from arvore import arvore as Arvore
from arvore import INDEFINIDO
from pytest import raises
from erros import ItemNaoEncontrado, ParametroNaoInformado
from pyext import naoGeraErro


def arvorePronta():
    umaArvore = Arvore()
    umaArvore.inserir(0)
    umaArvore.inserir(1, 0)
    umaArvore.inserir(2, 0)
    umaArvore.inserir(3, 0)
    umaArvore.inserir(4, 1)
    umaArvore.inserir(5, 1)
    umaArvore.inserir(6, 3)
    umaArvore.inserir(7, 3)
    umaArvore.inserir(None, 6)
    umaArvore.inserir(8, 7)

    return umaArvore


def arvoreProntaMaior():
    umaArvore = arvorePronta()
    umaArvore.inserir(9, None)
    umaArvore.inserir(10, None)

    umaArvore.inserir(11, 8)
    umaArvore.inserir(12, 8)

    umaArvore.inserir(13, 9)
    umaArvore.inserir(14, 9)
    umaArvore.inserir(15, 9)

    umaArvore.inserir(16, 10)

    umaArvore.inserir(17, 11)
    umaArvore.inserir(18, 11)
    umaArvore.inserir(19, 11)
    umaArvore.inserir(20, 11)

    umaArvore.inserir(21, 12)
    umaArvore.inserir(22, 12)

    return umaArvore


arvore = arvorePronta()


def testes_metodo_inserir():
    numeros = Arvore()

    numeros.inserir(0)
    numeros.inserir(1, 0)
    numeros.inserir(2, 0)
    numeros.inserir(3, 0)
    assert numeros.filhos(0) == (1, 2, 3)
    assert numeros.pai(1) == 0
    assert numeros.pai(2) == 0
    assert numeros.pai(3) == 0

    numeros.inserir(4, 1)
    numeros.inserir(5, 1)
    assert numeros.filhos(1) == (4, 5)
    assert numeros.pai(4) == 1
    assert numeros.pai(5) == 1

    numeros.inserir(6, 3)
    numeros.inserir(7, 3)
    assert numeros.filhos(3) == (6, 7)
    assert numeros.pai(6) == 3
    assert numeros.pai(7) == 3

    numeros.inserir(None, 6)
    assert numeros.filhos(6) == (None, )
    assert numeros.pai(None) == 6

    numeros.inserir(8, 7)
    assert numeros.filhos(7) == (8, )
    assert numeros.pai(8) == 7


def testes_oMetodo_inserir_lancaraUmaExcacaoSeOPaiNaoForEncontrado():
    a = Arvore()
    a.inserir(0)

    with raises(ItemNaoEncontrado):
        a.inserir(4, -5)


def testes_oMetodo_inserir():
    definiraARaizDaArvoreSeOPaiNaoForInformadoEAArvoreEstiverVazia()
    lancaraUmaExcecaoSeOPaiNaoForInformadoEAArvoreNaoEstiverVazia()


def definiraARaizDaArvoreSeOPaiNaoForInformadoEAArvoreEstiverVazia():
    a = Arvore()
    a.inserir(0)

    assert a.raiz == 0


def lancaraUmaExcecaoSeOPaiNaoForInformadoEAArvoreNaoEstiverVazia():
    a = Arvore()
    a.inserir(0)

    with raises(ParametroNaoInformado):
        a.inserir(1)


def testeDoIteradorPosFixado():
    assert list(arvore) == [4, 5, 1, 2, None, 6, 8, 7, 3, 0]


def teste_IteradorPosFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in Arvore():
            pass


def testeDoIteradorPreFixado():
    assert list(arvore.preFixado()) == [0, 1, 4, 5, 2, 3, 6, None, 7, 8]


def teste_IteradorPreFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in Arvore().preFixado():
            pass


def testes_metodo_profundidade():
    assert arvore.profundidade(5) == 2
    assert arvore.profundidade(8) == 3
    assert arvore.profundidade(arvore.raiz) == 0


def testes_metodo_altura():
    assert arvore.altura(2) == 0 # item sem filhos
    assert arvore.altura(3) == 2
    assert arvore.altura() == arvore.altura(arvore.raiz) == 3


def teste_oMetodo_profundidade_lancaraUmaExcacaoSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.profundidade(10)


def teste_oMetodo_altura_lancaraUmaExcacaoSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.altura(-10)


def testes_doOperador_in():
    assert 7 in arvore
    assert 4 in arvore

    assert 10 not in arvore
    assert -1 not in arvore


def testes_doOperador_in_informandoARaizDaArvore():
    assert 0 in arvore


def testes_metodo_pai():
    assert arvore.pai(None) is 6
    assert arvore.pai(2) is 0
    assert arvore.pai(4) is 1


def testes_oMetodo_pai_retornaNoneSeOItemForARaizDaArvore():
    assert arvore.pai(arvore.raiz) is INDEFINIDO


def testes_oMetodo_pai_lancaraUmaExcecaoSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.pai(-2)


def testes_metodo_filhos():
    assert arvore.filhos(3) == (6, 7)
    assert arvore.filhos(8) == ()
    assert arvore.filhos(arvore.raiz) == (1, 2, 3)


def testes_oMetodo_filhos_lancaraUmaExcecaoSeOItemNaoForEncontradoNaArvore():
    with raises(ItemNaoEncontrado):
        arvore.filhos(-2)


def testes_propriedade_tamanho_aposInserirAlgunsItensEmUmaArvore():
    numeros = Arvore()

    numeros.inserir(0)
    numeros.inserir(1, 0)
    numeros.inserir(2, 0)
    assert numeros.tamanho == 3

    numeros.inserir(3, 0)
    numeros.inserir(4, 1)
    assert numeros.tamanho == 5

    numeros.inserir(5, 1)
    assert numeros.tamanho == 6

    numeros.inserir(6, 3)
    numeros.inserir(7, 3)
    numeros.inserir(None, 6)
    numeros.inserir(8, 7)
    assert numeros.tamanho == 10


def testes_metodo_possuiFilhos():
    assert arvore.possuiFilhos(arvore.raiz)
    assert arvore.possuiFilhos(1)
    assert arvore.possuiFilhos(6)

    assert not arvore.possuiFilhos(2)
    assert not arvore.possuiFilhos(None)


def testes_oMetodo_possuiFilhos_lancaraUmaExcecaoSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.possuiFilhos(-7)


def testes_metodo_remover():
    numeros = arvorePronta()
    numeros.remover(1)

    assert numeros.filhos(numeros.raiz) == (2, 3)
    assert list(numeros) == [2, None, 6, 8, 7, 3, 0]

    numeros.remover(None)

    assert list(numeros) == [2, 6, 8, 7, 3, 0]

    numeros.remover(numeros.raiz)

    assert numeros.vazia
    assert numeros.raiz is None


def testes_oMetodo_remover_naoLancaraExcecaoSeOItemNaoForEncontrado():
    numeros = arvorePronta()

    with naoGeraErro():
        numeros.remover(-4)


def testes_propriedade_tamanho_aposRemoverAlgunsItensDeUmaArvore():
    numeros = arvorePronta()
    numeros.remover(None)

    assert numeros.tamanho == 9

    numeros.remover(1)

    assert numeros.tamanho == 6

    numeros.remover(numeros.raiz)

    assert numeros.tamanho == 0


def testes_oMetodo_tamanhoDaSubarvore():
    retornaOTamanhoDaSubarvoreEnraizadaNoItemInformado()
    lancaUmaExcecaoSeOItemInformadoNaoForEncontrado()


def retornaOTamanhoDaSubarvoreEnraizadaNoItemInformado():
    assert arvore.tamanhoDaSubarvore(3) == 5
    assert arvore.tamanhoDaSubarvore(1) == 3
    assert arvore.tamanhoDaSubarvore(2) == 1
    assert arvore.tamanhoDaSubarvore(arvore.raiz) == 10


def lancaUmaExcecaoSeOItemInformadoNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.tamanhoDaSubarvore(-8)


def testes_doIteradorPosFixadoPrivado():
    from arvore import _IteradorPosFixado
    nodo = arvore._nodo(1)

    assert [n.item for n in _IteradorPosFixado(nodo)] == [4, 5, 1]

    nodo = arvore._nodo(3)

    assert [n.item for n in _IteradorPosFixado(nodo)] == [None, 6, 8, 7, 3]


def testes_doIteradorPreFixadoPrivado():
    from arvore import _IteradorPreFixado
    nodo = arvore._nodo(1)

    assert [n.item for n in _IteradorPreFixado(nodo)] == [1, 4, 5]

    nodo = arvore._nodo(3)

    assert [n.item for n in _IteradorPreFixado(nodo)] == [3, 6, None, 7, 8]


def testes_oMetodo_nivel_retornaraTodosOsItensDeUmNivel():
    nums = arvoreProntaMaior()

    assert list(nums.nivel(0)) == [0]
    assert list(nums.nivel(2)) == [4, 5, 6, 7]
    assert list(nums.nivel(3)) == [None, 8]
    assert list(nums.nivel(5)) == [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


def testes_doIteradorPorNivel():
    from arvore import _IteradorPorNivel as Iterador
    nums = arvoreProntaMaior()
    raiz = nums._raiz

    assert [nodo.item for nodo in Iterador(raiz, 2)] == [4, 5, 6, 7]
    assert [nodo.item for nodo in Iterador(raiz, 3)] == [None, 8]
    assert [nodo.item for nodo in Iterador(raiz, 5)] == [13, 14, 15, 16, 17,
                                                         18, 19, 20, 21, 22]


# TODO um nível negativo
# TODO um nível muito grande