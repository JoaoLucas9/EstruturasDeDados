from arvore import arvore as Arvore
from uteis import INDEFINIDO
from pytest import raises
from erros import ItemNaoEncontrado, ParametroNaoInformado
from pyext import naoGeraErro
from iteruteis import vazio
from uteistestes import pickle, load, deletar


def arvoreDeTestes():
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


def arvoreDeTestes2():
    umaArvore = arvoreDeTestes()
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


def arvoreParaTestesComItensDuplicados():
    arvore = Arvore()
    arvore.inserir('paises')
    arvore.inserir('br', 'paises')
    arvore.inserir('en', 'paises')
    arvore.inserir('eu', 'paises')
    arvore.inserir('cult', 'en')
    arvore.inserir('cult', 'eu')

    arvore.inserir('cult', 'br')
    arvore.inserir('musicas', 'br', 'cult')
    arvore.inserir('comidas', 'br', 'cult')
    arvore.inserir('sol', 'br', 'cult', 'musicas')
    arvore.inserir('chuva', 'musicas')
    arvore.inserir('feijao', 'comidas')

    arvore.inserir('comidas', 'en')
    arvore.inserir('musicas', 'en', 'cult')
    arvore.inserir('help',  'en', 'cult', 'musicas')

    arvore.inserir('musicas', 'eu')
    arvore.inserir('country', 'eu', 'musicas')
    arvore.inserir('pop', 'eu', 'musicas')
    arvore.inserir('1999', 'pop')
    arvore.inserir('2000', 'pop')
    arvore.inserir('sweet', '2000')
    arvore.inserir('happy', '2000')
    arvore.inserir('comidas', 'eu', 'cult')
    arvore.inserir('pie', 'eu', 'cult', 'comidas')
    arvore.inserir('donnuts', 'eu', 'cult', 'comidas')
    arvore.inserir('burger', 'eu', 'cult', 'comidas')

    return arvore


arvore = arvoreDeTestes()
arvoreD = arvoreParaTestesComItensDuplicados()


def testes_metodo_inserir():
    numeros = Arvore()

    numeros.inserir(0)
    numeros.inserir(1, 0)
    numeros.inserir(2, 0)
    numeros.inserir(3, 0)
    assert numeros.filhos(0) == (1, 2, 3)
    assert numeros.pai(1) is 0
    assert numeros.pai(2) is 0
    assert numeros.pai(3) is 0

    numeros.inserir(4, 1)
    numeros.inserir(5, 1)
    assert numeros.filhos(1) == (4, 5)
    assert numeros.pai(4) is 1
    assert numeros.pai(5) is 1

    numeros.inserir(6, 3)
    numeros.inserir(7, 3)
    assert numeros.filhos(3) == (6, 7)
    assert numeros.pai(6) is 3
    assert numeros.pai(7) is 3

    numeros.inserir(None, 6)
    assert numeros.filhos(6) == (None, )
    assert numeros.pai(None) is 6

    numeros.inserir(8, 7)
    assert numeros.filhos(7) == (8, )
    assert numeros.pai(8) is 7


def testes_oMetodo_inserir_geraUmErroSeOItemNaoForEncontrado():
    a = Arvore()
    a.inserir(0)

    with raises(ItemNaoEncontrado):
        a.inserir(4, -5)

    with raises(ItemNaoEncontrado):
        arvoreD.inserir('amor', 'br', 'musicas')


def testes_oMetodo_inserir():
    definiraARaizDaArvoreSeOPaiNaoForInformadoEAArvoreEstiverVazia()
    geraUmErroSeOPaiNaoForInformadoEAArvoreNaoEstiverVazia()


def definiraARaizDaArvoreSeOPaiNaoForInformadoEAArvoreEstiverVazia():
    a = Arvore()
    a.inserir(0)

    assert a.raiz == 0


def geraUmErroSeOPaiNaoForInformadoEAArvoreNaoEstiverVazia():
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


def teste_oMetodo_profundidade_geraUmErroSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.profundidade(10)

    with raises(ItemNaoEncontrado):
        arvoreD.profundidade('1999', 'en', 'cult', 'musicas')


def testes_oMetodo_profundidade_geraUmErroSeNenhumItemForInformado():
    with raises(ParametroNaoInformado):
        arvore.profundidade()


def testes_metodo_altura():
    assert arvore.altura(2) == 0
    assert arvore.altura(3) == 2
    assert arvore.altura() == arvore.altura(arvore.raiz) == 3


def teste_oMetodo_altura_geraUmErroSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.altura(-10)

    with raises(ItemNaoEncontrado):
        arvoreD.altura('historia', 'br')


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


def testes_oMetodo_pai_geraUmErroSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.pai(-2)


def testes_metodo_filhos():
    assert arvore.filhos(3) == (6, 7)
    assert arvore.filhos(8) == ()
    assert arvore.filhos(arvore.raiz) == (1, 2, 3)


def testes_oMetodo_filhos_geraUmErroSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.filhos(-2)

    with raises(ItemNaoEncontrado):
        arvoreD.filhos('comidas', 'en', 'cult')


def testes_oMetodo_filhos_geraUmErroSeNenhumItemForInformado():
    with raises(ParametroNaoInformado):
        arvore.filhos()


def testes_propriedade_tamanho_aposInserirAlgunsItens():
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


def testes_oMetodo_possuiFilhos_retornaraTrueSeOItemPossuirUmOuMaisFilhos():
    assert arvore.possuiFilhos(arvore.raiz)
    assert arvore.possuiFilhos(1)
    assert arvore.possuiFilhos(6)


def testes_oMetodo_possuiFilhos_retornaraFalseSeOItemNaoPossuirNenhumFilho():
    assert not arvore.possuiFilhos(2)
    assert not arvore.possuiFilhos(None)


def testes_oMetodo_possuiFilhos_geraUmErroSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.possuiFilhos(-7)

    with raises(ItemNaoEncontrado):
        arvoreD.possuiFilhos('futebol', 'paises', 'en')


def testes_oMetodo_possuiFilhos_geraUmErroSeNenhumItemForInformado():
    with raises(ParametroNaoInformado):
        arvore.possuiFilhos()


def testes_metodo_remover():
    numeros = arvoreDeTestes()
    numeros.remover(1)

    assert numeros.filhos(numeros.raiz) == (2, 3)
    assert list(numeros) == [2, None, 6, 8, 7, 3, 0]

    numeros.remover(None)

    assert list(numeros) == [2, 6, 8, 7, 3, 0]

    numeros.remover(numeros.raiz)

    assert numeros.vazia
    assert numeros.raiz is None


def testes_oMetodo_remover_naoLancaraExcecaoSeOItemNaoForEncontrado():
    numeros = arvoreDeTestes()

    with naoGeraErro():
        numeros.remover(-4)


def testes_oMetodo_remover_geraUmErroSeNenhumItemForInformado():
    with raises(ParametroNaoInformado):
        arvore.remover()


def testes_propriedade_tamanho_aposRemoverAlgunsItensDeUmaArvore():
    numeros = arvoreDeTestes()
    numeros.remover(None)

    assert numeros.tamanho == 9

    numeros.remover(1)

    assert numeros.tamanho == 6

    numeros.remover(numeros.raiz)

    assert numeros.tamanho == 0


def testes_metodo_tamanhoDaSubarvore():
    assert arvore.tamanhoDaSubarvore(3) == 5
    assert arvore.tamanhoDaSubarvore(1) == 3
    assert arvore.tamanhoDaSubarvore(2) == 1
    assert arvore.tamanhoDaSubarvore(arvore.raiz) == 10


def testes_metodo_tamanhoDaSubarvore_geraUmErroSeOItemNaoForEncontrado():
    with raises(ItemNaoEncontrado):
        arvore.tamanhoDaSubarvore(-8)

    with raises(ItemNaoEncontrado):
        arvoreD.tamanhoDaSubarvore('amor', 'musicas')


def testes_oMetodo_tamanhoDaSubarvore_geraUmErroSeNenhumItemForInformado():
    with raises(ParametroNaoInformado):
        arvore.tamanhoDaSubarvore()


def testes_doIteradorPosFixadoPrivado():
    from arvore import _IteradorPosFixado
    nodo = arvore._nodo([1])

    assert [n.item for n in _IteradorPosFixado(nodo)] == [4, 5, 1]

    nodo = arvore._nodo([3])

    assert [n.item for n in _IteradorPosFixado(nodo)] == [None, 6, 8, 7, 3]


def testes_doIteradorPreFixadoPrivado():
    from arvore import _IteradorPreFixado
    nodo = arvore._nodo([1])

    assert [n.item for n in _IteradorPreFixado(nodo)] == [1, 4, 5]

    nodo = arvore._nodo([3])

    assert [n.item for n in _IteradorPreFixado(nodo)] == [3, 6, None, 7, 8]


def testes_oMetodo_nivel_retornaraTodosOsItensDeUmNivel():
    nums = arvoreDeTestes2()

    assert list(nums.nivel(0)) == [0]
    assert list(nums.nivel(2)) == [4, 5, 6, 7]
    assert list(nums.nivel(3)) == [None, 8]
    assert list(nums.nivel(5)) == [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


def testes_doIteradorPorNivel():
    from arvore import _IteradorPorNivel as Iterador
    nums = arvoreDeTestes2()
    raiz = nums._raiz

    assert [nodo.item for nodo in Iterador(raiz, 2)] == [4, 5, 6, 7]
    assert [nodo.item for nodo in Iterador(raiz, 3)] == [None, 8]
    assert [nodo.item for nodo in Iterador(raiz, 5)] == [13, 14, 15, 16, 17,
                                                         18, 19, 20, 21, 22]


def testes_metodo_filhos_caminhoComecandoNaRaiz():
    assert arvoreD.filhos('paises', 'en') == ('cult', 'comidas')
    assert arvoreD.filhos('paises', 'eu', 'cult', 'comidas') == \
           ('pie', 'donnuts', 'burger')

    assert arvoreD.filhos('paises', 'br', 'cult', 'musicas') == ('sol',
                                                                 'chuva')


def testes_metodo_filhos_caminhoNaoComecaNaRaiz():
    assert arvoreD.filhos('musicas', 'pop') == ('1999', '2000')
    assert arvoreD.filhos('br', 'cult', 'comidas') == ('feijao', )
    assert vazio(arvoreD.filhos('musicas', 'help'))


def testes_metodo_profundidade_caminhoComecandoNaRaiz():
    assert arvoreD.profundidade('paises', 'en', 'comidas') is 2


def testes_metodo_profundidade_caminhoNaoComecaNaRaiz():
    assert arvoreD.profundidade('eu', 'cult', 'comidas') is 3
    assert arvoreD.profundidade('comidas', 'feijao') is 4


def testes_metodo_altura_caminhoComecandoNaRaiz():
    assert arvoreD.altura('paises', 'eu', 'musicas', 'country') is 0
    assert arvoreD.altura('paises', 'eu', 'musicas') is 3


def testes_metodo_altura_caminhoNaoComecaNaRaiz():
    assert arvoreD.altura('musicas', 'sol') is 0
    assert arvoreD.altura('br', 'cult', 'musicas') is 1


def testes_metodo_possuiFilhos_caminhoComecandoNaRaiz():
    assert arvoreD.possuiFilhos('paises', 'br', 'cult')
    assert not arvoreD.possuiFilhos('paises', 'eu', 'musicas', 'country')


def testes_metodo_possuiFilhos_caminhoNaoComecaNaRaiz():
    assert arvoreD.possuiFilhos('eu', 'cult', 'comidas')
    assert not arvoreD.possuiFilhos('en', 'comidas')


def testes_metodo_tamanhoDaSubarvore_caminhoComecandoNaRaiz():
    assert arvoreD.tamanhoDaSubarvore('paises', 'eu', 'musicas') is 7
    assert arvoreD.tamanhoDaSubarvore('paises', 'en', 'comidas') is 1


def testes_metodo_tamanhoDaSubarvore_caminhoNaoComecaNaRaiz():
    assert arvoreD.tamanhoDaSubarvore('br', 'cult', 'musicas') is 3
    assert arvoreD.tamanhoDaSubarvore('en', 'cult', 'musicas') is 2


def testes_metodo_inserir_inserirItensDuplicados():
    arvore = Arvore()
    arvore.inserir('paises')
    arvore.inserir('br', 'paises')
    arvore.inserir('en', 'paises')
    arvore.inserir('eu', 'paises')
    arvore.inserir('cult', 'br')
    arvore.inserir('cult', 'en')
    arvore.inserir('cult', 'eu')

    arvore.inserir('musicas', 'br', 'cult')
    arvore.inserir('comidas', 'br', 'cult')

    assert arvore.filhos('br', 'cult') == ('musicas', 'comidas')
    assert vazio(arvore.filhos('en', 'cult'))
    assert vazio(arvore.filhos('eu', 'cult'))

    arvore.inserir('comidas', 'en')
    arvore.inserir('comidas', 'eu', 'cult')
    arvore.inserir('pie', 'eu', 'cult', 'comidas')
    arvore.inserir('burger', 'eu', 'cult', 'comidas')

    assert vazio(arvore.filhos('br', 'cult', 'comidas'))
    assert vazio(arvore.filhos('en', 'comidas'))
    assert arvore.filhos('eu', 'cult', 'comidas') == ('pie', 'burger')

    arvore.inserir('musicas', 'paises', 'en', 'cult')
    arvore.inserir('help', 'en', 'cult', 'musicas')

    assert arvore.filhos('en', 'cult', 'musicas') == ('help', )

    arvore.inserir('musicas', 'eu')
    arvore.inserir('country', 'eu', 'musicas')
    arvore.inserir('pop', 'eu', 'musicas')

    assert arvore.filhos('eu', 'musicas') == ('country', 'pop')

    arvore.inserir('1999', 'paises', 'eu', 'musicas', 'pop')
    arvore.inserir('2000', 'pop')

    assert arvore.filhos('paises') == ('br', 'en', 'eu')
    assert arvore.filhos('br') == ('cult', )
    assert arvore.filhos('br', 'cult') == ('musicas', 'comidas')
    assert vazio(arvore.filhos('br', 'cult', 'musicas'))
    assert vazio(arvore.filhos('br', 'cult', 'comidas'))

    assert arvore.filhos('en') == ('cult', 'comidas')
    assert arvore.filhos('en', 'cult') == ('musicas', )
    assert arvore.filhos('en', 'cult', 'musicas') == ('help', )
    assert vazio(arvore.filhos('en', 'comidas'))

    assert arvore.filhos('eu') == ('cult', 'musicas')
    assert arvore.filhos('eu', 'cult') == ('comidas', )
    assert arvore.filhos('eu', 'cult', 'comidas') == ('pie', 'burger')
    assert arvore.filhos('eu', 'musicas') == ('country', 'pop')
    assert arvore.filhos('pop') == ('1999', '2000')
    assert vazio(arvore.filhos('pie'))
    assert vazio(arvore.filhos('burger'))
    assert vazio(arvore.filhos('1999'))
    assert vazio(arvore.filhos('2000'))
    assert vazio(arvore.filhos('country'))


def testes_metodo_remover_deUmaArvoreQuePossuiItensDuplicados():
    arvore = arvoreParaTestesComItensDuplicados()
    arvore.remover('br', 'cult', 'comidas')

    assert arvore.filhos('br', 'cult') == ('musicas', )
    assert arvore.filhos('en') == ('cult', 'comidas')
    assert arvore.filhos('eu', 'cult') == ('comidas', )

    arvore.remover('en', 'cult', 'musicas')

    assert vazio(arvore.filhos('en', 'cult'))
    assert arvore.filhos('br', 'cult') == ('musicas', )
    assert arvore.filhos('eu') == ('cult', 'musicas')

    arvore.remover('eu', 'cult')

    assert arvore.filhos('eu') == ('musicas', )
    assert arvore.filhos('en') == ('cult', 'comidas')
    assert arvore.filhos('br') == ('cult', )


def testes_oOperadorDe_igualdade_retornaTrueSe():
    asArvoresPossuiremAMesmaEstrutura()
    asArvoresEstiveremVazias()
    comparadaComUmaArvoreAVLComAMesmaEstrutura()
    comparadaComUmaArvoreVPComAMesmaEstrutura()


# duas árvores serão iguais se o pai e os filhos de qualquer um dos itens
# na árvore A forem iguais ao pai e aos filhos, respectivamente, do mesmo item
# na árvore B, isto implica que todos os itens de uma das árvores devem
# estar presentes na outra também.
def asArvoresPossuiremAMesmaEstrutura():
    """Mesma estrutura significa que o pai e os filhos de qualquer um dos
    itens na árvore A forem iguais ao pai e aos filhos, respectivamente,
    do mesmo item na árvore B e vice-versa."""
    assert arvoreDeTestes2() == arvoreDeTestes2()


def asArvoresEstiveremVazias():
    assert Arvore() == Arvore()


def comparadaComUmaArvoreAVLComAMesmaEstrutura():
    from testes_ArvoreAVL import arvore as arvoreAVL

    arvore = Arvore()
    arvore.inserir(6)
    arvore.inserir(3, 6)
    arvore.inserir(9, 6)
    arvore.inserir(1, 3)
    arvore.inserir(4, 3)
    arvore.inserir(8, 9)
    arvore.inserir(10, 9)
    arvore.inserir(0, 1)
    arvore.inserir(2, 1)

    assert arvore == arvoreAVL


def comparadaComUmaArvoreVPComAMesmaEstrutura():
    from testes_ArvoreVP import arvore as arvoreVP

    arvore = Arvore()
    arvore.inserir(6)
    arvore.inserir(3, 6)
    arvore.inserir(9, 6)
    arvore.inserir(1, 3)
    arvore.inserir(4, 3)
    arvore.inserir(8, 9)
    arvore.inserir(10, 9)
    arvore.inserir(0, 1)
    arvore.inserir(2, 1)

    assert arvore == arvoreVP


def testes_oOperadorDe_igualdade_retornaFalseSe():
    """As árvores são diferentes mas os seus iteradores pré ou pós fixado
    são iguais"""
    osIteradoresPreFixadosDasArvoresSaoIguaisMasAsEstrutursDelasNao()
    osIteradoresPosFixadosDasArvoresSaoIguaisMasAsEstrutursDelasNao()
    aOrdemDosFilhosDeUmItemEmUmaArvoreDiferirDaOrdemDosFilhosDoItemNaOutra()
    osFIlhosDeUmDosItensForDiferenteDosFilhosDoItemNaOutraArvore()
    oObjetoInformadoNaoForUmaArvore()
    asRaizesDasArvoresForemDiferentes()
    apenasUmaDasArvoresEstiverVazia()


def osIteradoresPreFixadosDasArvoresSaoIguaisMasAsEstrutursDelasNao():
    arvore1 = Arvore()
    arvore1.inserir(0)
    arvore1.inserir(1, 0)
    arvore1.inserir(2, 1)

    arvore2 = Arvore()
    arvore2.inserir(0)
    arvore2.inserir(1, 0)
    arvore2.inserir(2, 0)

    assert arvore1 != arvore2


def osIteradoresPosFixadosDasArvoresSaoIguaisMasAsEstrutursDelasNao():
    arvore1 = Arvore()
    arvore1.inserir(0)
    arvore1.inserir(1, 0)
    arvore1.inserir(2, 1)

    arvore2 = Arvore()
    arvore2.inserir(0)
    arvore2.inserir(2, 0)
    arvore2.inserir(1, 0)

    assert arvore1 != arvore2


def aOrdemDosFilhosDeUmItemEmUmaArvoreDiferirDaOrdemDosFilhosDoItemNaOutra():
    # as árvores 1 e 2 são quase iguais, as raizes de ambas são iguais bem
    # como os filhos dos seus itens, contudo a ordem dos filhos do 0
    # diferem, por isso 1 e 2 são diferentes
    arvore1 = Arvore()
    arvore1.inserir(0)
    arvore1.inserir(1, 0)
    arvore1.inserir(2, 0) # filhos do 0: 1 e 2

    arvore2 = Arvore()
    arvore2.inserir(0)
    arvore2.inserir(2, 0)
    arvore2.inserir(1, 0) # filhos do 0: 2 e 1

    assert arvore1 != arvore2


def osFIlhosDeUmDosItensForDiferenteDosFilhosDoItemNaOutraArvore():
    arvore1 = Arvore()
    arvore1.inserir(0)
    arvore1.inserir(1, 0)
    arvore1.inserir(2, 0) # filhos do 0: 1 e 2

    arvore2 = Arvore()
    arvore2.inserir(0)
    arvore2.inserir(1, 0)
    arvore2.inserir(2, 0)
    arvore2.inserir(3, 0) # filhos do 0: 1, 2 e 3
    # os filhos do 0 na arvore1 são diferentes dos filhos do 0 na arvore2

    assert arvore1 != arvore2


def oObjetoInformadoNaoForUmaArvore():
    assert arvore != 1


def asRaizesDasArvoresForemDiferentes():
    arvore = Arvore()
    arvore.inserir(0)

    arvore1 = Arvore()
    arvore1.inserir(1)

    assert arvore != arvore1

    arvore.inserir(2, 0)
    arvore.inserir(3, 0)

    arvore1.inserir(2, 1)
    arvore1.inserir(3, 1)

    assert arvore != arvore1


def apenasUmaDasArvoresEstiverVazia():
    assert arvore != Arvore()
    assert Arvore() != arvore


def testesDasFuncoes_dumpEloads_comUmaArvore():
    """Assegurar que as funções pickle.dumps e pickle.loads funcionam como o
    esperado com uma árvore. Funcionar como o esperado significa que é
    possível registrar uma árvore em um arquivo utilizando a função
    pickle.dumps e futuramente recuperá-la utilizando a função pickle.loads.

    É importante salientar que a árvore recuperada deve ser exatamente igual à
    árvore registrada.
    """
    pickle(arvore, 'arvore')
    arv = load('arvore')

    assert arv == arvore
    assert arv.tamanho == arvore.tamanho

    deletar('arvore')


def testesDasFuncoes_dumpEloads_comUmaArvoreVazia():
    pickle(Arvore(), 'arvoreVazia')
    arv = load('arvoreVazia')

    assert arv.vazia
    assert arv.tamanho is 0

    deletar('arvoreVazia')


