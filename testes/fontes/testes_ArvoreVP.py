from arvore import ArvoreVP
from pyext import naoGeraErro
from arvore import IGUAIS, INDEFINIDO, PRETO, VERMELHO
from pytest import raises
from erros import ItemNaoEncontrado, FalhaNaOperacao
from random import sample
from uteis import executar


def arvoreVazia():
    return ArvoreVP(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))


def arvorePronta(*numeros):
    nums = arvoreVazia()

    for numero in numeros:
        nums.inserir(numero)

    return nums


arvore = arvorePronta(4, 6, 8, 3, 2, 10, 9, 0, 1)


def testes_metodo_inserir():
    nums = arvoreVazia()
    nums.inserir(4)
    nums.inserir(6)
    nums.inserir(8)

    assert nums.raiz is 6
    assert nums.pai(4) is 6
    assert nums.pai(8) is 6
    assert nums.filhos(6) == (4, 8)
    assert nums.filhos(4) == nums.filhos(8) == tuple()
    assert nums.cor(6) is PRETO
    assert nums.cor(4) == nums.cor(8) == VERMELHO

    nums.inserir(3)

    assert nums.raiz is 6
    assert nums.pai(4) is 6
    assert nums.pai(8) is 6
    assert nums.pai(3) is 4
    assert nums.filhos(6) == (4, 8)
    assert nums.filhos(4) == (3, )
    assert nums.filhos(8) == tuple()
    assert nums.cor(6) == nums.cor(4) == nums.cor(8) == PRETO
    assert nums.cor(3) is VERMELHO

    nums.inserir(2)

    assert nums.pai(3) is 6
    assert nums.pai(8) is 6
    assert nums.pai(2) is 3
    assert nums.pai(4) is 3
    assert nums.filhos(6) == (3, 8)
    assert nums.filhos(3) == (2, 4)
    assert nums.filhos(2) == nums.filhos(4) == nums.filhos(8) == tuple()
    assert nums.cor(6) == nums.cor(3) == nums.cor(8) == PRETO
    assert nums.cor(2) == nums.cor(4) == VERMELHO

    nums.inserir(10)
    nums.inserir(9)

    assert nums.raiz is 6
    assert nums.pai(9) is 6
    assert nums.pai(8) is 9
    assert nums.pai(10) is 9
    assert nums.filhos(6) == (3, 9)
    assert nums.filhos(3) == (2, 4)
    assert nums.filhos(9) == (8, 10)
    assert nums.filhos(8) == nums.filhos(10) == tuple()
    assert nums.cor(6) == nums.cor(3) == nums.cor(9) == PRETO
    assert nums.cor(2) == nums.cor(4) == nums.cor(8) == nums.cor(10) == \
           VERMELHO

    nums.inserir(0)

    assert nums.pai(0) is 2
    assert nums.filhos(2) == (0, )
    assert nums.cor(6) == nums.cor(9) == nums.cor(2) == nums.cor(4) == PRETO
    assert nums.cor(3) == nums.cor(0) == nums.cor(8) == nums.cor(10) == \
           VERMELHO

    nums.inserir(1)

    assert nums.raiz is 6
    assert nums.pai(6) is INDEFINIDO
    assert nums.pai(3) is 6
    assert nums.pai(9) is 6
    assert nums.pai(1) is 3
    assert nums.pai(4) is 3
    assert nums.pai(0) is 1
    assert nums.pai(2) is 1
    assert nums.pai(8) is 9
    assert nums.pai(10) is 9
    assert nums.filhos(6) == (3, 9)
    assert nums.filhos(3) == (1, 4)
    assert nums.filhos(1) == (0, 2)
    assert nums.filhos(9) == (8, 10)
    assert nums.filhos(0) == nums.filhos(2) ==nums.filhos(8) == \
           nums.filhos(10) == tuple()
    assert nums.cor(6) == nums.cor(9) == nums.cor(1) == nums.cor(4) is PRETO
    assert nums.cor(3) == nums.cor(8) == nums.cor(10) == nums.cor(0) == \
           nums.cor(2) is VERMELHO


def testes_metodo_inserir2():
    nums = arvoreVazia()
    nums.inserir(10)
    nums.inserir(9)
    nums.inserir(8)
    nums.inserir(7)
    nums.inserir(6)
    nums.inserir(5)
    nums.inserir(4)
    nums.inserir(3)

    assert nums.raiz is 7
    assert nums.pai(5) is 7
    assert nums.pai(9) is 7
    assert nums.pai(4) is 5
    assert nums.pai(6) is 5
    assert nums.pai(3) is 4
    assert nums.pai(8) is 9
    assert nums.pai(10) is 9
    assert nums.filhos(7) == (5, 9)
    assert nums.filhos(5) == (4, 6)
    assert nums.filhos(4) == (3, )
    assert nums.filhos(9) == (8, 10)
    assert nums.filhos(3) == nums.filhos(6) == nums.filhos(8) == \
           nums.filhos(10) == tuple()
    assert nums.cor(7) == nums.cor(4) == nums.cor(6) == nums.cor(8) == \
           nums.cor(10) is PRETO
    assert nums.cor(5) == nums.cor(9) == nums.cor(3) == VERMELHO


def testes_propiedade_tamanho_aposInserirAlgunsItens():
    nums = arvoreVazia()
    nums.inserir(0)

    assert nums.tamanho is 1

    nums.inserir(1)
    nums.inserir(2)

    assert nums.tamanho is 3
    
    nums.inserir(3)
    nums.inserir(4)
    nums.inserir(5)

    assert nums.tamanho is 6


def teste_iterador():
    assert list(arvore) == [0, 2, 1, 4, 3, 8, 10, 9, 6]


def teste_IteradorPosFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in arvoreVazia():
            pass


def teste_iterador_preFixado():
    assert list(arvore.preFixado()) == [6, 3, 1, 0, 2, 4, 9, 8, 10]


def teste_IteradorPreFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in arvoreVazia().preFixado():
            pass


def teste_iterador_interFixado():
    assert list(arvore.interFixado()) == [0, 1, 2, 3, 4, 6, 8, 9, 10]


def teste_IteradorInterFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in arvoreVazia().interFixado():
            pass


def testes_metodo_pai():
    assert arvore.pai(9) is 6
    assert arvore.pai(2) is 1
    assert arvore.pai(arvore.raiz) is INDEFINIDO


def testes_oMetodo_pai_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.pai(-10)


def testes_operador_in():
    assert 4 in arvore
    assert 9 in arvore
    assert 6 in arvore

    assert -5 not in arvore


def testes_metodo_filhos():
    assert arvore.filhos(1) == (0, 2)
    assert arvore.filhos(4) == tuple()
    assert arvore.filhos(arvore.raiz) == (3, 9)


def testes_metodo_filhos_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhos(-7)


def testes_metodo_filhoEsquerdo():
    assert arvore.filhoEsquerdo(3) == 1
    assert arvore.filhoEsquerdo(arvore.raiz) == 3


def testes_metodo_filhoEsquerdo_iraGerarUmErroSeOItemNaoPossuirFilhoAEsquerda():
    with raises(FalhaNaOperacao):
        arvore.filhoEsquerdo(0)


def testes_metodo_filhoEsquerdo_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhoEsquerdo(-13)


def testes_metodo_filhoDireito():
    assert arvore.filhoDireito(1) == 2
    assert arvore.filhoDireito(arvore.raiz) == 9


def testes_metodo_filhoDireito_iraGerarUmErroSeOItemNaoPossuirFilhoADireita():
    with raises(FalhaNaOperacao):
        arvore.filhoDireito(10)


def testes_metodo_filhoDireito_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhoDireito(-13)


def testes_propiedade_itensSemFilhos():
    assert list(arvore.itensSemFilhos) == [0, 2, 4, 8, 10]
    assert list(arvorePronta(*range(10, 2, -1)).itensSemFilhos) == [3, 6, 8, 10]
    assert list(arvorePronta(1).itensSemFilhos) == [1]
    assert list(arvoreVazia().itensSemFilhos) == []


def testes_metodo_profundidadePreta():
    assert arvore.profundidadePreta(2) is 1
    assert arvore.profundidadePreta(9) is 1
    assert arvore.profundidadePreta(arvore.raiz) is 0


def testes_metodo_profundidadePreta_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.profundidadePreta(-5)


def desativar_testeSuperArvoreVP():
    numeros = sample(range(3000), 3000)
    # print(numeros)
    arvore = arvoreVazia()

    for numero in numeros:
        arvore.inserir(numero)

        if arvore.tamanho % 10 is 0:
            assegureEUmaArvoreVP(arvore)

    for numero in numeros:
        # print(numero)
        arvore.remover(numero)
        if arvore.tamanho % 5 is 0 and not arvore.vazia:
            assegureEUmaArvoreVP(arvore)


def assegureEUmaArvoreVP(arvore):
    assegurarQueTodosOsItensVermelhosPossuemFilhosPretosApenas(arvore)
    assegurarQueTodosOsNodosExternosPossuemAMesmaProfundidadePreta(arvore)


def assegurarQueTodosOsItensVermelhosPossuemFilhosPretosApenas(arvore):
    for item in itensVermelhos(arvore):
        assert not possuiFilhosVermelhos(item, arvore)


def itensVermelhos(arvore):
    return (item for item in arvore if arvore.cor(item) is VERMELHO)


def possuiFilhosVermelhos(item, arvore):
    for filho in arvore.filhos(item):
        if arvore.cor(filho) is VERMELHO:
            return True
    return False


def assegurarQueTodosOsNodosExternosPossuemAMesmaProfundidadePreta(arvore: ArvoreVP):
    iter = arvore.itensSemFilhos
    p = arvore.profundidadePreta(next(iter))
    
    for item in iter:
        assert arvore.profundidadePreta(item) == p


def testes_metodo_remover():
    nums = arvorePronta(4, 6, 8, 3, 2, 10, 9, 0, 1)
    nums.remover(2)
    nums.remover(1)

    assert nums.pai(0) is 3
    assert nums.filhos(3) == (0, 4)
    assert nums.cor(0) is PRETO

    nums.remover(4)

    assert nums.filhos(3) == (0, )
    assert nums.cor(3) is PRETO
    assert nums.cor(0) is VERMELHO

    nums.inserir(4)
    nums.inserir(5)
    nums.remover(0)

    assert nums.pai(4) is 6
    assert nums.pai(3) is 4
    assert nums.pai(5) is 4
    assert nums.filhos(6) == (4, 9)
    assert nums.filhos(4) == (3, 5)
    assert nums.filhos(3) == nums.filhos(5) == tuple()
    assert nums.cor(4) is VERMELHO
    assert nums.cor(3) == nums.cor(5) == PRETO

    nums.remover(8)
    nums.remover(10)
    nums.remover(9)

    assert nums.raiz is 4
    assert nums.pai(3) is 4
    assert nums.pai(6) is 4
    assert nums.pai(5) is 6
    assert nums.filhos(4) == (3, 6)
    assert nums.filhos(6) == (5, )
    assert nums.filhos(3) == nums.filhos(5) == tuple()
    assert nums.cor(4) is PRETO
    assert nums.cor(3) is PRETO
    assert nums.cor(6) is PRETO
    assert nums.cor(5) is VERMELHO

    nums.remover(4)

    assert nums.raiz is 5
    assert nums.pai(3) is 5
    assert nums.pai(6) is 5
    assert nums.filhos(5) == (3, 6)
    assert nums.filhos(3) == nums.filhos(6) == tuple()
    assert nums.cor(3) is PRETO
    assert nums.cor(5) is PRETO

    nums.remover(6)

    assert nums.filhos(5) == (3, )
    assert nums.cor(3) is VERMELHO

    nums.remover(5)

    assert nums.raiz is 3
    assert nums.cor(3) is PRETO

    nums.remover(3)


def testes_metodo_remover2():
    nums = arvorePronta(1, 2, 0, 3, 4)
    nums.remover(1)
    nums.remover(2)

    assert nums.raiz is 3
    assert nums.pai(3) is INDEFINIDO
    assert nums.pai(0) is 3
    assert nums.pai(4) is 3
    assert nums.filhos(3) == (0, 4)
    assert nums.cor(4) is PRETO


def testes_metodo_remover3():
    nums = [3, 4, 0, 2, 1]
    nums.remove(3)
    nums.remove(4)
    nums.remove(0)


def testes_metodo_remover4():
    nums = arvorePronta(1, 0, 2, 3)
    nums.remover(3)
    nums.remover(1)

    assert nums.raiz is 2
    assert nums.pai(2) is INDEFINIDO
    assert nums.pai(0) is 2
    assert nums.filhos(2) == (0, )
    assert nums.cor(0) is VERMELHO
    assert nums.cor(2) is PRETO
    # todo remover mais profundo


def testes_metodo_remover5():
    """Remover 10, vermelho: 10 possui 2 filhos pretos, 5, e 15, e o 15 por
    sua vez possui 1 filho vermelho a esquerda, o 13.

    Remover 13, vermelho: 13 possui 2 filhos pretos externos, 5 e 15."""
    nums = arvorePronta(20, 10, 30, 5, 15, 13)
    nums.remover(10)

    assert nums.pai(5) is 13
    assert nums.pai(15) is 13
    assert nums.filhos(13) == (5, 15)
    assert nums.filhos(15) == tuple()
    assert nums.cor(13) is VERMELHO

    nums.remover(13)

    assert nums.pai(15) is 20
    assert nums.pai(5) is 15
    assert nums.filhos(15) == (5, )
    assert nums.cor(5) is VERMELHO
    assert nums.cor(15) is PRETO


def testes_metodo_remover6():
    """Remover 10, vermelho: 10 possui 2 filhos pretos, 5, e 15, e o 15 por
    sua vez possui 2 filhos vermelhos, 13 e 16.

    Remover 13, vermelho: 13 possui 2 filhos pretos, 5, e 15, e o 15 por
    sua vez possui 1 filho vermelho a direita, o 16.
    """
    nums = arvorePronta(20, 10, 30, 5, 15, 13, 16)
    nums.remover(10)

    assert nums.pai(13) is 20
    assert nums.pai(5) is 13
    assert nums.pai(15) is 13
    assert nums.filhos(13) == (5, 15)
    assert nums.filhos(15) == (16, )
    assert nums.cor(13) is VERMELHO

    nums.remover(13)

    assert nums.pai(15) is 20
    assert nums.pai(5) is 15
    assert nums.pai(16) is 15
    assert nums.filhos(15) == (5, 16)
    assert nums.cor(15) is VERMELHO
    assert nums.cor(16) is PRETO


def testes_metodo_remover1_0():
    nums = remover(50, arvorePronta(50))

    assert nums.vazia
    assert 50 not in nums


def remover(numero, nums):
    nums.remover(numero)
    return nums


def testes_metodo_remover2_0():
    nums = remover(50, arvorePronta(50, 25))

    assert nums.raiz is 25
    assert nums.cor(25) is PRETO
    assert 50 not in nums


def testes_metodo_remover2_1():
    nums = remover(25, arvorePronta(50, 25))

    assert nums.raiz is 50
    assert 25 not in nums


def testes_metodo_remover3_0():
    nums = remover(50, arvorePronta(50, 100))

    assert nums.raiz is 100
    assert nums.cor(100) is PRETO
    assert 50 not in nums


def testes_metodo_remover3_1():
    nums = remover(100, arvorePronta(50, 100))

    assert nums.raiz is 50
    assert 100 not in nums


def testes_metodo_remover4_0():
    nums = remover(50, arvorePronta(50, 25, 100))

    assert nums.raiz is 100
    assert nums.pai(100) is INDEFINIDO
    assert nums.pai(25) is 100
    assert nums.filhos(100) == (25, )
    assert nums.cor(100) is PRETO


def testes_metodo_remover4_1():
    nums = remover(25, arvorePronta(50, 25, 100))

    assert nums.filhos(50) == (100, )
    assert 25 not in nums


def testes_metodo_remover4_2():
    nums = remover(100, arvorePronta(50, 25, 100))

    assert nums.filhos(50) == (25, )
    assert 100 not in nums


def testes_metodo_remover5_0():
    nums = remover(50, arvorePronta(50, 25, 100, 15))

    assert nums.raiz is 25
    assert nums.pai(15) is 25
    assert nums.pai(100) is 25
    assert nums.filhos(25) == (15, 100)
    assert nums.cor(15) is PRETO


def testes_metodo_remover5_1():
    nums = remover(25, arvorePronta(50, 25, 100, 15))

    assert nums.pai(15) is 50
    assert nums.filhos(50) == (15, 100)
    assert nums.cor(15) is PRETO


def testes_metodo_remover5_2():
    nums = remover(100, arvorePronta(50, 25, 100, 15))

    assert nums.raiz is 25
    assert nums.pai(25) is INDEFINIDO
    assert nums.pai(15) is 25
    assert nums.pai(50) is 25
    assert nums.filhos(25) == (15, 50)
    assert nums.cor(15) is PRETO


def testes_metodo_remover6_0():
    nums = remover(50, arvorePronta(50, 25, 100, 150))

    assert nums.raiz is 100
    assert nums.pai(100) is INDEFINIDO
    assert nums.pai(25) is 100
    assert nums.pai(150) is 100
    assert nums.filhos(100) == (25, 150)
    assert nums.cor(150) is PRETO


def testes_metodo_remover6_1():
    nums = remover(25, arvorePronta(50, 25, 100, 150))

    assert nums.raiz is 100
    assert nums.pai(100) is INDEFINIDO
    assert nums.pai(50) is 100
    assert nums.filhos(100) == (50, 150)
    assert nums.filhos(50) == tuple()
    assert nums.cor(150) is PRETO

    nums.remover(50)

    assert nums.filhos(100) == (150, )
    assert nums.cor(150) is VERMELHO
    assert 50 not in nums


def testes_metodo_remover6_2():
    nums = remover(100, arvorePronta(50, 25, 100, 150))

    assert nums.pai(150) is 50
    assert nums.filhos(50) == (25, 150)
    assert nums.cor(150) is PRETO


def testes_metodo_remover7_0():
    """Este é um caso especial pois existem 2 possíveis estados finais para
    a árvore. Este teste visa verificar que a árvore encontra-se em um
    destes estados."""
    nums = remover(100, arvorePronta(50, 25, 100, 15, 37))

    assert nums.raiz is 37
    assert nums.pai(37) is INDEFINIDO
    assert nums.pai(25) is 37
    assert nums.pai(50) is 37
    assert nums.filhos(37) == (25, 50)
    assert nums.filhos(25) == (15, )
    assert nums.filhos(50) == tuple()
    assert nums.cor(37) is PRETO


def testes_metodo_remover8_0():
    """Semelhante ao caso 7.0"""
    nums = remover(25, arvorePronta(50, 25, 100, 75, 150))

    assert nums.raiz is 100
    assert nums.pai(100) is INDEFINIDO
    assert nums.pai(50) is 100
    assert nums.pai(75) is 50
    assert nums.filhos(100) ==(50, 150)
    assert nums.filhos(50) == (75, )
    assert nums.cor(150) is PRETO


def testes_metodo_remover8_1():
    nums = remover(75, arvorePronta(50, 25, 100, 75, 150))

    assert nums.filhos(100) == (150, )


def testes_metodo_remover8_2():
    nums = remover(150, arvorePronta(50, 25, 100, 75, 150))

    assert nums.filhos(100) == (75, )


def testes_metodo_remover8_3():
    nums = remover(100, arvorePronta(50, 25, 100, 75, 150))

    assert nums.pai(150) is 50
    assert nums.pai(75) is 150
    assert nums.filhos(150) == (75, )
    assert nums.cor(150) is PRETO


def testes_metodo_remover9_0():
    nums = remover(50, arvorePronta(50, 25, 100, 37))

    assert nums.raiz is 37
    assert nums.pai(37) is INDEFINIDO
    assert nums.pai(25) is 37
    assert nums.pai(100) is 37
    assert nums.filhos(37) == (25, 100)
    assert nums.filhos(25) == tuple()
    assert nums.cor(37) is PRETO

    nums.remover(100)

    assert nums.raiz is 37
    assert nums.cor(25) is VERMELHO


def testes_metodo_remover10_0():
    nums = remover(150, arvorePronta(50, 25, 100, 75, 150, 88))

    assert nums.pai(88) is 50
    assert nums.pai(75) is 88
    assert nums.pai(100) is 88
    assert nums.filhos(50) == (25, 88)
    assert nums.filhos(88) == (75, 100)
    assert nums.filhos(75) == nums.filhos(100) == tuple()
    assert nums.cor(100) is PRETO
    assert nums.cor(88) is VERMELHO

    nums.remover(25)

    assert nums.raiz is 88
    assert nums.pai(88) is INDEFINIDO
    assert nums.pai(50) is 88
    assert nums.pai(75) is 50
    assert nums.filhos(88) == (50, 100)
    assert nums.filhos(50) == (75, )
    assert nums.cor(88) is PRETO
    assert nums.cor(75) == VERMELHO


def testes_metodo_remover10_1():
    nums = remover(25, arvorePronta(50, 25, 100, 75, 150, 88))

    assert nums.raiz is 100
    assert nums.pai(100) is INDEFINIDO
    assert nums.pai(50) is 75
    assert nums.filhos(100) == (75, 150)
    assert nums.filhos(75) == (50, 88)
    assert nums.filhos(50) == tuple()
    assert nums.cor(100) == nums.cor(88) == PRETO
    assert nums.cor(75) is VERMELHO

    nums.remover(150)

    assert nums.raiz is 75
    assert nums.pai(75) is INDEFINIDO
    assert nums.pai(100) is 75
    assert nums.pai(88) is 100
    assert nums.filhos(75) == (50, 100)
    assert nums.filhos(100) == (88, )
    assert nums.cor(75) is PRETO
    assert nums.cor(88) is VERMELHO


def testes_metodo_remover10_2():
    nums = remover(50, arvorePronta(50, 25, 100, 75, 150, 88))

    assert nums.raiz is 75
    assert nums.pai(75) is INDEFINIDO
    assert nums.pai(25) is 75
    assert nums.pai(100) is 75
    assert nums.pai(88) is 100
    assert nums.filhos(75) == (25, 100)
    assert nums.filhos(100) == (88, 150)
    assert nums.cor(88) is PRETO

    nums.remover(75)

    assert nums.raiz is 88
    assert nums.pai(25) is 88
    assert nums.pai(100) is 88
    assert nums.filhos(88) == (25, 100)
    assert nums.filhos(100) == (150, )
    assert nums.cor(100) is PRETO
    assert nums.cor(150) is VERMELHO


def testes_metodo_remover10_3():
    nums = remover(100, arvorePronta(50, 25, 100, 75, 150, 88))

    assert nums.pai(88) is 50
    assert nums.pai(75) is 88
    assert nums.pai(150) is 88
    assert nums.filhos(50) == (25, 88)
    assert nums.filhos(88) == (75, 150)
    assert nums.filhos(75) == tuple()
    assert nums.cor(88) is VERMELHO


def testes_metodo_remover11_0():
    nums = remover(100, arvorePronta(50, 25, 100, 10, 37, 5))

    assert nums.raiz is 25
    assert nums.pai(50) is 25
    assert nums.pai(37) is 50
    assert nums.filhos(25) == (10, 50)
    assert nums.filhos(50) == (37, )
    assert nums.cor(25) is PRETO
    assert nums.cor(37) is VERMELHO

    nums.remover(37)

    assert nums.filhos(50) == tuple()


def testes_metodo_remover11_1():
    nums = remover(25, arvorePronta(50, 25, 100, 10, 37, 5))

    assert nums.pai(10) is 50
    assert nums.pai(37) is 10
    assert nums.filhos(50) == (10, 100)
    assert nums.filhos(10) ==(5, 37)
    assert nums.cor(10) is VERMELHO
    assert nums.cor(5) is PRETO

    nums.remover(10)

    assert nums.pai(37) is 50
    assert nums.pai(5) is 37
    assert nums.filhos(50) == (37, 100)
    assert nums.filhos(37) == (5, )
    assert nums.cor(5) is VERMELHO


def testes_metodo_remover12_0():
    nums = remover(0, arvorePronta(0, 1, 3, 2, 5, 7, 4, 9, 6, 8))

    assert nums.raiz is 5
    assert nums.pai(3) is 5
    assert nums.pai(7) is 5
    assert nums.pai(4) is 3
    assert nums.filhos(5) == (3, 7)
    assert nums.filhos(3) == (1, 4)
    assert nums.cor(2) is VERMELHO
    assert nums.cor(7) == nums.cor(5) is PRETO

    nums.remover(8)
    nums.remover(9)

    assert nums.cor(6) == nums.cor(3) is VERMELHO


def testes_metodo_remover12_1():
    nums = remover(0, arvorePronta(0, 1, 3, 2, 5, 7, 4, 9, 6, 8))
    nums.remover(2)
    nums.remover(4)

    assert nums.cor(1) == nums.cor(7) == VERMELHO


def testes_metodo_remover7():
    nums = remover(0, arvorePronta(0, 1, 3, 2, 5, 7, 4, 9, 6, 8))
    nums.remover(1)
    nums.remover(3)

    assert nums.pai(4) is 5
    assert nums.pai(2) is 4
    assert nums.filhos(4) == (2, )
    assert nums.cor(7) is VERMELHO

    nums.remover(2)
    nums.remover(5)

    assert nums.raiz is 6
    assert nums.pai(6) is INDEFINIDO
    assert nums.pai(4) is 6
    assert nums.pai(8) is 6
    assert nums.pai(7) is 8
    assert nums.pai(9) is 8
    assert nums.filhos(6) == (4, 8)
    assert nums.filhos(8) == (7, 9)
    assert nums.filhos(7) == nums.filhos(9) == tuple()
    assert nums.cor(6) == nums.cor(4) == nums.cor(7) == nums.cor(9) == PRETO
    assert nums.cor(8) is VERMELHO


def testes_metodo_remover8():
    nums = remover(5, arvorePronta(5, 13, 4, 12, 10, 8, 1, 9, 2, 7, 3, 6,
                                   11, 0 , 14))
    nums.remover(13)
    nums.remover(4)
    nums.remover(12)

    assert nums.pai(11) is 9
    assert nums.pai(10) is 11
    assert nums.pai(14) is 11
    assert nums.filhos(9) == (6, 11)
    assert nums.filhos(11) == (10, 14)
    assert nums.filhos(10) == nums.filhos(14) == tuple()
    assert nums.cor(11) is PRETO

    nums.remover(10)

    assert nums.raiz is 6
    assert nums.pai(9) is 6
    assert nums.pai(7) is 9
    assert nums.filhos(6) == (2, 9)
    assert nums.filhos(9) == (7, 11)
    assert nums.filhos(11) == (14, )
    assert nums.cor(2) is PRETO
    assert nums.cor(14) is  VERMELHO


def testes_propiedade_tamanho_aposRemoverAlgunsItens():
    nums = arvorePronta(0, 1, 2, 3, 4, 5, 6, 7, 8)
    nums.remover(0)

    assert nums.tamanho is 8

    nums.remover(1)
    nums.remover(2)

    assert nums.tamanho is 6

    nums.remover(3)
    nums.remover(4)
    nums.remover(5)

    assert nums.tamanho is 3

    nums.remover(6)
    nums.remover(7)
    nums.remover(8)

    assert nums.tamanho is 0


def testes_oMetodo_remover_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.remover(-5)

# trabalhei muito duro para testar o método remover em diversas situações,
# por exemplo, remover um item externo (preto ou vermelho), um item com um
# filho, um item com dois filhos (ambos pretos ou ambos vermelhos) etc.
# contudo é possível que ainda hajam casos que não testados, o método
# remover foi um grande desafio.
# Não tenho muita certeza se a árvore é confiável, além do mais o código de
# produção ficou bem medíocre, bem longe de ser bom), contudo, mesmo assim
# julgo que já seja hora para prossegir para uma nova estrutura de dados.
# Mas certamente eu ainda voltarei para aprimorar o código, o trabalho não
# foi finalizado.

