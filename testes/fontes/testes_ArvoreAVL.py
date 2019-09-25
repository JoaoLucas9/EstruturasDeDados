from arvore import ArvoreAVL, INDEFINIDO, IGUAIS, _IteradorPosFixado
from erros import ItemNaoEncontrado, ColecaoVazia, FalhaNaOperacao
from pytest import raises
from random import sample, randint
from uteis import executar
from pyext import naoGeraErro
from uteistestes import maior, pickle, load, deletar


def arvoreVazia():
    return ArvoreAVL(maior)


def arvoreDeTestes():
    nums = arvoreVazia()
    nums.inserir(4)
    nums.inserir(6)
    nums.inserir(8)
    nums.inserir(3)
    nums.inserir(2)
    nums.inserir(10)
    nums.inserir(9)
    nums.inserir(0)
    nums.inserir(1)

    return nums


def novaArvore(*numeros):
    nums = arvoreVazia()

    for numero in numeros:
        nums.inserir(numero)

    return nums


arvore = arvoreDeTestes()


def teste_metodo_inserir():
    nums = arvoreVazia()
    nums.inserir(40)
    nums.inserir(60)
    nums.inserir(80)

    assert nums.raiz is 60
    assert nums.pai(40) == nums.pai(80) is 60
    assert nums.filhos(60) == (40, 80)
    assert nums.filhos(40) == nums.filhos(80) == tuple()

    nums.inserir(30)
    nums.inserir(20)

    assert nums.raiz is 60
    assert nums.pai(30) == nums.pai(80) is 60
    assert nums.pai(20) == nums.pai(40) is 30
    assert nums.filhos(60) == (30, 80)
    assert nums.filhos(30) == (20, 40)
    assert nums.filhos(20) == nums.filhos(40) == nums.filhos(80) == tuple()

    nums.inserir(100)
    nums.inserir(90)

    assert nums.raiz == 60
    assert nums.pai(30) == nums.pai(90) is 60
    assert nums.pai(20) == nums.pai(40) is 30
    assert nums.pai(80) == nums.pai(100) is 90
    assert nums.filhos(60) == (30, 90)
    assert nums.filhos(30) == (20, 40)
    assert nums.filhos(90) == (80, 100)
    assert nums.filhos(20) == nums.filhos(40) == nums.filhos(80) == \
           nums.filhos(100) == tuple()

    nums.inserir(0)
    nums.inserir(10)

    assert nums.raiz == 60
    assert nums.pai(30) == nums.pai(90) is 60
    assert nums.pai(10) == nums.pai(40) is 30
    assert nums.pai(0) == nums.pai(20) is 10
    assert nums.pai(80) == nums.pai(100) is 90
    assert nums.filhos(60) == (30, 90)
    assert nums.filhos(30) == (10, 40)
    assert nums.filhos(10) == (0, 20)
    assert nums.filhos(90) == (80, 100)
    assert nums.filhos(0) == nums.filhos(20) == nums.filhos(40) == \
                           nums.filhos(80) == nums.filhos(100) == tuple()


def teste_propiedade_tamanho_aposInserirAlgunsItens():
    nums = arvoreVazia()

    nums.inserir(40)
    nums.inserir(60)
    nums.inserir(80)
    assert nums.tamanho == 3

    nums.inserir(30)
    assert nums.tamanho == 4

    nums.inserir(20)
    nums.inserir(100)
    assert nums.tamanho == 6


def teste_metodo_pai():
    assert arvore.pai(8) == 9
    assert arvore.pai(3) == 6
    assert arvore.pai(4) == 3
    assert arvore.pai(6) == INDEFINIDO


def teste_metodo_pai_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.pai(-70)


def teste_metodo_filhos():
    assert arvore.filhos(2) == ()
    assert arvore.filhos(9) == (8, 10)
    assert arvore.filhos(arvore.raiz) == (3, 9)


def teste_metodo_filhos_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhos(-80)


def teste_metodo_menor():
    assert arvore.menor() == 0


def teste_metodo_menor_geraUmErroSeAArvoreEstiverVazia():
    with raises(ColecaoVazia):
        arvoreVazia().menor()


def teste_metodo_maior():
    assert arvore.maior() == 10


def teste_metodo_maior_geraUmErroSeAArvoreEstiverVazia():
    with raises(ColecaoVazia):
        arvoreVazia().maior()


def teste_operador_in():
    assert 10 in arvore
    assert 1 in arvore
    assert arvore.raiz in arvore

    assert -70 not in arvore


def teste_iterador():
    assert list(arvore) == [0, 2, 1, 4, 3, 8, 10, 9, 6]


def teste_IteradorPosFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in ArvoreAVL(None):
            pass


def teste_iterador_prefixado():
    assert list(arvore.preFixado()) == [6, 3, 1, 0, 2, 4, 9, 8, 10]


def teste_IteradorPreFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in ArvoreAVL(None).preFixado():
            pass


def teste_iterador_interfixado():
    assert list(arvore.interFixado()) == [0, 1, 2, 3, 4, 6, 8, 9, 10]


def teste_IteradorInterFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in ArvoreAVL(None).interFixado():
            pass


def teste_metodo_ancestrais():
    assert list(arvore.ancestrais(2)) == [1, 3, 6]
    assert list(arvore.ancestrais(9)) == [6]
    assert list(arvore.ancestrais(arvore.raiz)) == []


def teste_metodo_ancestrais_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.ancestrais(-80)


def teste_metodo_altura():
    assert arvore.altura(0) == 0
    assert arvore.altura(9) == 1
    assert arvore.altura() == arvore.altura(arvore.raiz) == 3


def teste_metodo_altura_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.altura(-10)


def teste_metodo_remover():
    """Primeiro(s) caso(s) de testes de remoção.
    Casos de remoção:
    30 - nodo interno 2 filhos, rebalanceamento ✓
    0 - nodo externo, rebalanceamento ✓
    80, 40 - nodos externos, rebalanceamento ✗
    20 - nodo interno 1 filho a esquerda, rebalanceamneto ✗
    10 - nodo externo, rebalanceamento ✓
    Inserir 80
    90 (raiz) - nodo interno 2 filhos, rebalanceamento ✓
    """
    nums = arvoreDeTestes()
    nums.remover(3)

    assert nums.raiz is 6
    assert nums.pai(1) == nums.pai(9) == 6
    assert nums.pai(0) == nums.pai(4) == 1
    assert nums.pai(2) == 4
    assert nums.pai(8) == nums.pai(10) == 9
    assert nums.filhos(6) == (1, 9)
    assert nums.filhos(1) == (0, 4)
    assert nums.filhos(4) == (2, )
    assert nums.filhos(9) == (8, 10)
    assert nums.filhos(0) == nums.filhos(2) == nums.filhos(8) ==\
           nums.filhos(10) == tuple()

    nums.remover(0)

    assert nums.raiz is 6
    assert nums.pai(2) == nums.pai(9) == 6
    assert nums.pai(1) == nums.pai(4) == 2
    assert nums.pai(8) == nums.pai(10) == 9
    assert nums.filhos(6) == (2, 9)
    assert nums.filhos(2) == (1, 4)
    assert nums.filhos(9) == (8, 10)
    assert nums.filhos(1) == nums.filhos(4) == nums.filhos(8) == \
           nums.filhos(10) == tuple()

    nums.remover(8)
    nums.remover(4)

    assert nums.raiz is 6
    assert nums.pai(2) == nums.pai(9) == 6
    assert nums.pai(1) == 2
    assert nums.pai(10) == 9
    assert nums.filhos(6) == (2, 9)
    assert nums.filhos(2) == (1, )
    assert nums.filhos(9) == (10, )
    assert nums.filhos(1) == nums.filhos(10) == tuple()

    nums.remover(2)

    assert nums.raiz is 6
    assert nums.pai(1) == nums.pai(9) == 6
    assert nums.pai(10) == 9
    assert nums.filhos(6) == (1, 9)
    assert nums.filhos(9) == (10,)
    assert nums.filhos(1) == nums.filhos(10) == tuple()

    nums.remover(1)

    assert nums.raiz is 9
    assert nums.pai(6) == nums.pai(10) == 9
    assert nums.filhos(9) == (6, 10)
    assert nums.filhos(6) == nums.filhos(10) == tuple()

    nums.inserir(8)
    nums.remover(9)

    assert nums.raiz is 8
    assert nums.pai(6) == nums.pai(10) == 8
    assert nums.filhos(8) == (6, 10)
    assert nums.filhos(6) == nums.filhos(10) == tuple()

    nums.remover(nums.raiz)

    assert nums.raiz == 10
    assert nums.pai(6) == 10
    assert nums.filhos(10) == (6, )
    assert nums.filhos(6) == tuple()

    nums.remover(6)

    assert nums.raiz == 10
    assert nums.filhos(10) == tuple()

    nums.remover(10)


def teste_metodo_remover2():
    nums = novaArvore(50, 25, 100, 12, 38, 75, 125, 6, 30, 45, 70, 40)

    nums.remover(25)

    assert nums.raiz == 50
    assert nums.pai(30) == nums.pai(100) == 50
    assert nums.pai(12) == nums.pai(40) == 30
    assert nums.pai(38) == nums.pai(45) == 40
    assert nums.pai(75) == nums.pai(125) == 100
    assert nums.pai(70) == 75
    assert nums.filhos(50) == (30, 100)
    assert nums.filhos(30) == (12, 40)
    assert nums.filhos(40) == (38, 45)
    assert nums.filhos(100) == (75, 125)
    assert nums.filhos(75) == (70, )
    assert nums.filhos(12) == (6, )
    assert nums.filhos(38) == nums.filhos(45) ==  nums.filhos(70) == \
           nums.filhos(125) == tuple()


def teste_metodo_remover3():
    nums = novaArvore(50, 30, 100, 15, 45, 75, 125, 10, 70, 80, 120, 90)

    nums.remover(50)

    assert nums.raiz == 70
    assert nums.pai(30) == nums.pai(100) == 70
    assert nums.pai(15) == nums.pai(45) == 30
    assert nums.pai(10) == 15
    assert nums.pai(80) == 100
    assert nums.pai(125) == 100
    assert nums.pai(75) == nums.pai(90) == 80
    assert nums.pai(120) == 125
    assert nums.filhos(70) == (30, 100)
    assert nums.filhos(30) == (15, 45)
    assert nums.filhos(15) == (10, )
    assert nums.filhos(100) == (80, 125)
    assert nums.filhos(80) == (75, 90)
    assert nums.filhos(125) == (120, )
    assert nums.filhos(10) == nums.filhos(45) == nums.filhos(75) == \
           nums.filhos(90) == nums.filhos(120) == tuple()


def teste_metodo_remover4():
    nums = arvoreDeTestes()
    nums.inserir(5)
    nums.remover(3)

    assert nums.raiz == 6
    assert nums.pai(4) == 6
    assert nums.pai(9) == 6
    assert nums.pai(1) == nums.pai(5) == 4
    assert nums.pai(0) == nums.pai(2) == 1
    assert nums.pai(8) == nums.pai(10) == 9
    assert nums.filhos(6) == (4, 9)
    assert nums.filhos(4) == (1, 5)
    assert nums.filhos(1) == (0, 2)
    assert nums.filhos(9) == (8, 10)
    assert nums.filhos(0) == nums.filhos(2) == nums.filhos(5) == \
           nums.filhos(8) == nums.filhos(10) == tuple()


def teste_metodo_remover5():
    nums = novaArvore(40, 60, 80, 30, 20, 100, 90, 0, 10, 35, 50)
    nums.remover(30)

    assert nums.raiz == 60
    assert nums.pai(35) == 60
    assert nums.pai(90) == 60
    assert nums.pai(10) == 35
    assert nums.pai(40) == 35
    assert nums.pai(0) == 10
    assert nums.pai(20) == 10
    assert nums.pai(50) == 40
    assert nums.pai(80) == 90
    assert nums.pai(100) == 90
    assert nums.filhos(60) == (35, 90)
    assert nums.filhos(10) == (0, 20)
    assert nums.filhos(40) == (50, )
    assert nums.filhos(90) == (80, 100)
    assert nums.filhos(0) == nums.filhos(20) == nums.filhos(50) == \
           nums.filhos(80) == nums.filhos(100) == tuple()


def teste_metodo_remover6():
    """A árvore possui apenas 2 itens, a raiz e seu filho a esquerda,
    quero remover a raiz"""
    nums = novaArvore(100, 60)
    nums.remover(100)

    assert nums.raiz == 60
    assert nums.pai(60) == INDEFINIDO
    assert nums.filhos(60) == tuple()


def teste_metodo_remover7():
    nums = novaArvore(50, 25, 100, 12, 38, 75, 125, 6, 30, 45, 70, 35)

    nums.remover(25)

    assert nums.raiz == 50
    assert nums.pai(30) == 50
    assert nums.pai(100) == 50
    assert nums.pai(12) == 30
    assert nums.pai(38) == 30
    assert nums.pai(6) == 12
    assert nums.pai(35) == 38
    assert nums.pai(45) == 38
    assert nums.pai(75) == 100
    assert nums.pai(125) == 100
    assert nums.pai(70) == 75
    assert nums.filhos(50) == (30, 100)
    assert nums.filhos(30) == (12, 38)
    assert nums.filhos(12) == (6, )
    assert nums.filhos(38) == (35, 45)
    assert nums.filhos(100) == (75, 125)
    assert nums.filhos(75) == (70, )
    assert nums.filhos(6) == nums.filhos(35) == nums.filhos(45) == \
           nums.filhos(70) == nums.filhos(125) == tuple()


def teste_metodo_remover8():
    """Remover um numero que possui um único filho e a árvore precisa ser
    rebalanceada."""
    nums = novaArvore(50, 25, 80, 12, 30, 100, 10)

    nums.remover(80)

    assert nums.raiz == 25
    assert nums.pai(12) == 25
    assert nums.pai(50) == 25
    assert nums.pai(10) == 12
    assert nums.pai(30) == 50
    assert nums.pai(100) == 50
    assert nums.filhos(25) == (12, 50)
    assert nums.filhos(12) == (10, )
    assert nums.filhos(50) == (30, 100)
    assert nums.filhos(10) == nums.filhos(30) == nums.filhos(100) == tuple()


def teste_metodo_remover9():
    nums = novaArvore(4, 3, 0, 1, 2)

    nums.remover(4)

    assert nums.raiz == 1
    assert nums.pai(0) == 1
    assert nums.pai(3) == 1
    assert nums.pai(2) == 3
    assert nums.filhos(1) == (0, 3)
    assert nums.filhos(3) == (2, )
    assert nums.filhos(0) == nums.filhos(2) == tuple()


def teste_metodo_remover_multiplosRebalanceamentos():
    """O elemento removido é externo"""
    nums = novaArvore(50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55, 1)

    nums.remover(80)

    assert nums.raiz == 25
    assert nums.pai(10) == 25
    assert nums.pai(50) == 25
    assert nums.pai(5) == 10
    assert nums.pai(15) == 10
    assert nums.pai(1) == 5
    assert nums.pai(30) == 50
    assert nums.pai(60) == 50
    assert nums.pai(27) == 30
    assert nums.pai(55) == 60
    assert nums.pai(75) == 60
    assert nums.filhos(25) == (10, 50)
    assert nums.filhos(10) == (5, 15)
    assert nums.filhos(5) == (1, )
    assert nums.filhos(50) == (30, 60)
    assert nums.filhos(30) == (27, )
    assert nums.filhos(60) == (55, 75)
    assert nums.filhos(1) == nums.filhos(15) == nums.filhos(27) == \
           nums.filhos(55) == nums.filhos(75) == tuple()


def teste_metodo_remover_multiplosRebalanceamentos2():
    """O elemento removido possui 1 filho a esquerda"""
    nums = novaArvore(50, 25, 75, 12, 40, 60, 90, 8, 18, 35, 45,
                      55, 70, 80, 4, 9, 17, 30, 54, 2)

    nums.remover(90)

    assert nums.raiz == 25
    assert nums.pai(12) == 25
    assert nums.pai(50) == 25
    assert nums.pai(8) == 12
    assert nums.pai(18) == 12
    assert nums.pai(4) == 8
    assert nums.pai(9) == 8
    assert nums.pai(2) == 4
    assert nums.pai(17) == 18
    assert nums.pai(40) == 50
    assert nums.pai(60) == 50
    assert nums.pai(35) == 40
    assert nums.pai(45) == 40
    assert nums.pai(30) == 35
    assert nums.pai(55) == 60
    assert nums.pai(75) == 60
    assert nums.pai(54) == 55
    assert nums.pai(70) == 75
    assert nums.pai(80) == 75
    assert nums.filhos(25) == (12, 50)
    assert nums.filhos(12) == (8, 18)
    assert nums.filhos(8) == (4, 9)
    assert nums.filhos(4) == (2, )
    assert nums.filhos(18) == (17, )
    assert nums.filhos(50) == (40, 60)
    assert nums.filhos(40) == (35, 45)
    assert nums.filhos(35) == (30, )
    assert nums.filhos(60) == (55, 75)

    assert nums.filhos(55) == (54, )
    assert nums.filhos(75) == (70, 80)
    assert nums.filhos(2) == nums.filhos(9) == nums.filhos(17) == \
           nums.filhos(30) == nums.filhos(45) == nums.filhos(54) == \
           nums.filhos(70) == nums.filhos(80) == tuple()


def teste_metodo_remover_multiplosRebalanceamentos3():
    """O elemento removido possui 1 filho a direita"""
    nums = novaArvore(50, 25, 75, 12, 40, 60, 90, 8, 18, 35, 45,
                      55, 70, 100, 4, 9, 17, 30, 54, 2)

    nums.remover(90)

    assert nums.raiz == 25
    assert nums.pai(12) == 25
    assert nums.pai(50) == 25
    assert nums.pai(8) == 12
    assert nums.pai(18) == 12
    assert nums.pai(4) == 8
    assert nums.pai(9) == 8
    assert nums.pai(2) == 4
    assert nums.pai(17) == 18
    assert nums.pai(40) == 50
    assert nums.pai(60) == 50
    assert nums.pai(35) == 40
    assert nums.pai(45) == 40
    assert nums.pai(30) == 35
    assert nums.pai(55) == 60
    assert nums.pai(75) == 60
    assert nums.pai(54) == 55
    assert nums.pai(70) == 75
    assert nums.pai(100) == 75
    assert nums.filhos(25) == (12, 50)
    assert nums.filhos(12) == (8, 18)
    assert nums.filhos(8) == (4, 9)
    assert nums.filhos(4) == (2, )
    assert nums.filhos(18) == (17,)
    assert nums.filhos(50) == (40, 60)
    assert nums.filhos(40) == (35, 45)
    assert nums.filhos(35) == (30, )

    assert nums.filhos(60) == (55, 75)
    assert nums.filhos(55) == (54, )
    assert nums.filhos(75) == (70, 100)
    assert nums.filhos(2) == nums.filhos(9) == nums.filhos(17) == \
           nums.filhos(30) == nums.filhos(45) == nums.filhos(54) == \
           nums.filhos(70) == nums.filhos(100) == tuple()


def teste_metodo_remover_multiplosRebalanceamentos4():
    """O elemento removido possui 2 filhos."""
    nums = novaArvore(40, 20, 60, 10, 30, 50, 80, 5, 15, 25, 35, 45, 55, 70,
                      90, 2, 7,  13, 17, 27, 33, 37, 42, 47, 52, 85, 1, 3,
                      6, 14, 36, 41, 0)

    nums.remover(80)

    assert nums.raiz == 20
    assert nums.pai(40) == 20
    assert nums.pai(30) == 40
    assert nums.pai(85) == 60
    assert nums.pai(70) == 85
    assert nums.pai(90) == 85
    assert nums.filhos(20) == (10, 40)
    assert nums.filhos(40) == (30, 50)
    assert nums.filhos(60) == (55, 85)
    assert nums.filhos(85) == (70, 90)


def teste_propiedade_tamanho_aposRemoverAlgunsItens():
    nums = arvoreDeTestes()

    nums.remover(4)
    assert nums.tamanho == 8

    nums.remover(6)
    nums.remover(8)
    assert nums.tamanho == 6

    nums.remover(3)
    nums.remover(2)
    nums.remover(10)
    assert nums.tamanho == 3

    nums.remover(9)
    nums.remover(0)
    nums.remover(1)
    assert nums.tamanho == 0


def teste_metodo_remover_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.remover(-50)


def teste_metodo_filhoEsquerdo():
    assert arvore.filhoEsquerdo(arvore.raiz) is 3
    assert arvore.filhoEsquerdo(9) is 8


def teste_metodo_filhoEsquerdo_geraUmErroSeOItemNaoPossuirUmFilhoAEsquerda():
    with raises(FalhaNaOperacao):
        arvore.filhoEsquerdo(40)


def teste_metodo_filhoEsquerdo_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhoEsquerdo(-40)


def teste_metodo_filhoDireito():
    assert arvore.filhoDireito(arvore.raiz) is 9
    assert arvore.filhoDireito(1) is 2


def teste_metodo_filhoDireito_geraUmErroSeOItemNaoPossuirUmFilhoADireita():
    with raises(FalhaNaOperacao):
        arvore.filhoDireito(80)


def teste_metodo_filhoDireito_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhoDireito(-40)


# super teste de carga da árvore avl, selecionar 5000 números aleatórios,
# inseri-los, a cada 3, 5 ou x (sendo x um número aleatório qualquer),
# assegurar que a árvore continua sendo avl.

# após a inserção, remover um por um e a cada 3, 5 ou x (sendo x um número
# aleatório qualquer) assegurar que a árvore continua sendo avl.
def desativar_testeSuperArvoreAVL():
    # permanece desativado devido ao seu longo tempo de execução
    # números de 0 a 5000 em uma ordem aleatória
    numeros = sample(range(8000), 8000)
    arvore = arvoreVazia()

    for numero in numeros:
        arvore.inserir(numero)

        if arvore.tamanho % 10 == 0:
            assert eUmaArvoreAVL(arvore)

    for numero in numeros:
        arvore.remover(numero)

        if arvore.tamanho % 5 == 0:
            assert eUmaArvoreAVL(arvore)


def eUmaArvoreAVL(arvore):
    for numero in arvore:
        esquerdo = executar(lambda :arvore.filhoEsquerdo(numero))
        alturaEsquerdo = -1 if esquerdo is None else arvore.altura(esquerdo)

        direito = executar(lambda :arvore.filhoDireito(numero))
        alturaDireito = -1 if direito is None else arvore.altura(direito)

        if esquerdo is not None and esquerdo > numero:
            return False

        if direito is not None and direito < numero:
            return False

        return abs(alturaEsquerdo - alturaDireito) <= 1

    return True


def assegurarQueEUmaArvoreAVL(arvore):
    for nodo in _IteradorPosFixado(arvore._raiz):
        esquerdo = nodo.esquerdo
        alturaEsquerdo = -1 if esquerdo is None else arvore._altura(esquerdo)

        direito = nodo.direito
        alturaDireito = -1 if direito is None else arvore._altura(direito)

        if esquerdo is not None:
            assert esquerdo.item <= nodo.item

        if direito is not None:
            assert direito.item >= nodo.item
        assert abs(alturaEsquerdo - alturaDireito) <= 1


def desativar_testeSuperArvoreAVLComDuplicados():
    numeros = []
    arvore = arvoreVazia()

    for x in range(3000):
        x = randint(0, 2000)
        numeros.append(x)
        arvore.inserir(x)

        if arvore.tamanho % 5 == 0:
            assegurarQueEUmaArvoreAVL(arvore)

    for x in numeros:
        arvore.remover(x)

        if arvore.tamanho % 5 == 0 and arvore.tamanho > 0:
            assegurarQueEUmaArvoreAVL(arvore)


def teste_metodo_inserir_duplicados1():
    arvore = ArvoreAVL(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    arvore.inserir(4)
    arvore.inserir(5)
    arvore.inserir(4)
    arvore.inserir(4)

    assegurarQueEUmaArvoreAVL(arvore)


def teste_metodo_inserir_duplicados2():
    arvore = ArvoreAVL(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    arvore.inserir(4)
    arvore.inserir(4)
    arvore.inserir(4)
    arvore.inserir(4)
    arvore.inserir(4)
    arvore.inserir(4)
    arvore.inserir(4)
    arvore.inserir(4)
    arvore.inserir(4)
    assegurarQueEUmaArvoreAVL(arvore)


def teste_metodo_remover_duplicados1():
    arvore = novaArvore(2, 3, 1, 2, 2)
    arvore.remover(2)
    raiz = arvore._raiz

    assert raiz.item is 2
    assert raiz.esquerdo.item is 1

    arvore.remover(3)

    assert arvore._raiz is raiz
    assert raiz.item is 2
    assert raiz.esquerdo.item is 1
    assert raiz.direito.item is 2

    arvore.remover(1)

    assert arvore._raiz is raiz
    assert raiz.item is 2
    assert raiz.esquerdo is None
    assert raiz.direito.item is 2


def teste_metodo_remover_duplicados2():
    arvore = novaArvore(4, 2, 3, 3, 2, 0, 1, 3, 3)
    arvore.remover(4)
    arvore.remover(2)
    arvore.remover(2)
    
    assegurarQueEUmaArvoreAVL(arvore)


def testes_operadorDe_igualdade_retornaTrueSe():
    asArvoresPossuiremOsMesmosItensNasMesmasQuantidade()
    asArvoresEstiveremVazias()
    aArvoreGenericaPossuirOsMesmosItensQueAArvoreAVL()
    aArvoreVPPossuirOsMesmosItensQueAArvoreAVL()


def asArvoresPossuiremOsMesmosItensNasMesmasQuantidade():
    arvore1 = novaArvore(4, 6, 8, 3, 2, 10, 9, 0, 1)
    arvore2 = novaArvore(3, 10, 6, 4, 9, 1, 8, 2, 0)

    assert arvore1 == arvore2


def asArvoresEstiveremVazias():
    assert arvoreVazia() == arvoreVazia()


def aArvoreGenericaPossuirOsMesmosItensQueAArvoreAVL():
    from testes_arvore import arvore as arvoreG
    arvore = ArvoreAVL(maior)
    arvore.inserir(0)
    arvore.inserir(1)
    arvore.inserir(2)
    arvore.inserir(3)
    arvore.inserir(4)
    arvore.inserir(5)
    arvore.inserir(6)
    arvore.inserir(7)
    arvore.inserir(None)
    arvore.inserir(8)

    assert arvore == arvoreG


def aArvoreVPPossuirOsMesmosItensQueAArvoreAVL():
    from testes_ArvoreVP import arvore as arvoreVP

    assert arvore == arvoreVP


def testes_operadorDe_igualdade_retornaFalseSe():
    asArvoresNaoPossuiremOsMesmosItens()
    asArvoresPossuiremOsMesmosItensEmQuantidadesDiferentes()
    apenasUmaDasArvoresEstiverVazia()
    asRaizesForemDiferentes()
    oObjetoInformadoNaoForUmaArvoreValida()


def asArvoresNaoPossuiremOsMesmosItens():
    assert arvore != novaArvore(6, 8, 3, 2, 10, 9, 0, 1)
    assert arvore != novaArvore(5, 4, 6, 8, 3, 2, 10, 9, 0, 1)


def asArvoresPossuiremOsMesmosItensEmQuantidadesDiferentes():
    assert arvore != novaArvore(4, 4, 8, 3, 2, 10, 9, 0, 1)
    assert novaArvore(4, 4, 0, 1) != novaArvore(4, 9, 0, 1)
    assert novaArvore(4, 9, 0, 1) != novaArvore(4, 4, 0, 1)


def apenasUmaDasArvoresEstiverVazia():
    assert arvore != ArvoreAVL(None)
    assert ArvoreAVL(None) != arvore


def asRaizesForemDiferentes():
    assert novaArvore(0) != novaArvore(1)


def oObjetoInformadoNaoForUmaArvoreValida():
    """árvore válida pode ser uma árvore genêrica, binária, avl ou vp."""
    assert arvore != [4, 6, 8, 3, 2, 10, 9, 0, 1]


def testesDasFuncoes_dumpEloads_comUmaArvoreAVL():
    pickle(arvore, 'avl')
    arv = load('avl')

    assegurarQueAsArvoresAVLPossuemAMesmaEstrutura(arv, arvore)
    assert arv.tamanho == arvore.tamanho

    deletar('avl')


def assegurarQueAsArvoresAVLPossuemAMesmaEstrutura(a1, a2):
    from arvore import _IteradorPreFixado as Iterador

    for n1, n2 in zip(Iterador(a1._raiz), Iterador(a2._raiz)):
        assert n1 == n2


def testesDasFuncoes_dumpE1loads_comUmaArvoreAVLVazia():
    pickle(arvoreVazia(), 'avlVazia')
    arv = load('avlVazia')

    assert arv.vazia
    assert arv.tamanho is 0

    deletar('avlVazia')
