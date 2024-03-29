from arvore import ArvoreAVL, INDEFINIDO, IGUAIS
from erros import ItemNaoEncontrado, ColecaoVazia, FalhaNaOperacao
from pytest import raises
from random import sample
from uteis import executar
from pyext import naoGeraErro


def arvoreVazia():
    return ArvoreAVL(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))


def arvorePronta():
    nums = arvoreVazia()
    nums.inserir(40)
    nums.inserir(60)
    nums.inserir(80)
    nums.inserir(30)
    nums.inserir(20)
    nums.inserir(100)
    nums.inserir(90)
    nums.inserir(0)
    nums.inserir(10)

    return nums


def novaArvore(*numeros):
    nums = arvoreVazia()

    for numero in numeros:
        nums.inserir(numero)

    return nums


arvore = arvorePronta()


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
    assert arvore.pai(80) == 90
    assert arvore.pai(30) == 60
    assert arvore.pai(40) == 30
    assert arvore.pai(60) == INDEFINIDO


def teste_metodo_pai_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.pai(-70)


def teste_metodo_filhos():
    assert arvore.filhos(20) == ()
    assert arvore.filhos(90) == (80, 100)
    assert arvore.filhos(arvore.raiz) == (30, 90)


def teste_metodo_filhos_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhos(-80)


def teste_metodo_menor():
    assert arvore.menor() == 0


def teste_metodo_menor_geraUmErroSeAArvoreEstiverVazia():
    with raises(ColecaoVazia):
        arvoreVazia().menor()


def teste_metodo_maior():
    assert arvore.maior() == 100


def teste_metodo_maior_geraUmErroSeAArvoreEstiverVazia():
    with raises(ColecaoVazia):
        arvoreVazia().maior()


def teste_operador_in():
    assert 100 in arvore
    assert 10 in arvore
    assert arvore.raiz in arvore

    assert -70 not in arvore


def teste_iterador():
    assert list(arvore) == [0, 20, 10, 40, 30, 80, 100, 90, 60]


def teste_IteradorPosFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in ArvoreAVL(None):
            pass


def teste_iterador_prefixado():
    assert list(arvore.preFixado()) == [60, 30, 10, 0, 20, 40, 90, 80, 100]


def teste_IteradorPreFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in ArvoreAVL(None).preFixado():
            pass


def teste_iterador_interfixado():
    assert list(arvore.interFixado()) == [0, 10, 20, 30, 40, 60, 80, 90,
                                          100]


def teste_IteradorInterFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in ArvoreAVL(None).interFixado():
            pass


def teste_metodo_ancestrais():
    assert list(arvore.ancestrais(20)) == [10, 30, 60]
    assert list(arvore.ancestrais(90)) == [60]
    assert list(arvore.ancestrais(arvore.raiz)) == []


def teste_metodo_ancestrais_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.ancestrais(-80)


def teste_metodo_altura():
    assert arvore.altura(0) == 0
    assert arvore.altura(90) == 1
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
    nums = arvorePronta()
    nums.remover(30)

    assert nums.raiz is 60
    assert nums.pai(10) == nums.pai(90) == 60
    assert nums.pai(0) == nums.pai(40) == 10
    assert nums.pai(20) == 40
    assert nums.pai(80) == nums.pai(100) == 90
    assert nums.filhos(60) == (10, 90)
    assert nums.filhos(10) == (0, 40)
    assert nums.filhos(40) == (20, )
    assert nums.filhos(90) == (80, 100)
    assert nums.filhos(0) == nums.filhos(20) == nums.filhos(80) ==\
           nums.filhos(100) == tuple()

    nums.remover(0)

    assert nums.raiz is 60
    assert nums.pai(20) == nums.pai(90) == 60
    assert nums.pai(10) == nums.pai(40) == 20
    assert nums.pai(80) == nums.pai(100) == 90
    assert nums.filhos(60) == (20, 90)
    assert nums.filhos(20) == (10, 40)
    assert nums.filhos(90) == (80, 100)
    assert nums.filhos(10) == nums.filhos(40) == nums.filhos(80) == \
           nums.filhos(100) == tuple()

    nums.remover(80)
    nums.remover(40)

    assert nums.raiz is 60
    assert nums.pai(20) == nums.pai(90) == 60
    assert nums.pai(10) == 20
    assert nums.pai(100) == 90
    assert nums.filhos(60) == (20, 90)
    assert nums.filhos(20) == (10, )
    assert nums.filhos(90) == (100, )
    assert nums.filhos(10) == nums.filhos(100) == tuple()

    nums.remover(20)

    assert nums.raiz is 60
    assert nums.pai(10) == nums.pai(90) == 60
    assert nums.pai(100) == 90
    assert nums.filhos(60) == (10, 90)
    assert nums.filhos(90) == (100,)
    assert nums.filhos(10) == nums.filhos(100) == tuple()

    nums.remover(10)

    assert nums.raiz is 90
    assert nums.pai(60) == nums.pai(100) == 90
    assert nums.filhos(90) == (60, 100)
    assert nums.filhos(60) == nums.filhos(100) == tuple()

    nums.inserir(80)
    nums.remover(90)

    assert nums.raiz is 80
    assert nums.pai(60) == nums.pai(100) == 80
    assert nums.filhos(80) == (60, 100)
    assert nums.filhos(60) == nums.filhos(100) == tuple()

    nums.remover(nums.raiz)

    assert nums.raiz == 100
    assert nums.pai(60) == 100
    assert nums.filhos(100) == (60, )
    assert nums.filhos(60) == tuple()

    nums.remover(60)

    assert nums.raiz == 100
    assert nums.filhos(100) == tuple()

    nums.remover(100)


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
    nums = arvorePronta()
    nums.inserir(50)
    nums.remover(30)

    assert nums.raiz == 60
    assert nums.pai(40) == 60
    assert nums.pai(90) == 60
    assert nums.pai(10) == nums.pai(50) == 40
    assert nums.pai(0) == nums.pai(20) == 10
    assert nums.pai(80) == nums.pai(100) == 90
    assert nums.filhos(60) == (40, 90)
    assert nums.filhos(40) == (10, 50)
    assert nums.filhos(10) == (0, 20)
    assert nums.filhos(90) == (80, 100)
    assert nums.filhos(0) == nums.filhos(20) == nums.filhos(50) == \
           nums.filhos(80) == nums.filhos(100) == tuple()


def teste_metodo_remover5():
    nums = arvorePronta()
    nums.inserir(35)
    nums.inserir(50)
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
    nums = arvoreVazia()
    nums.inserir(100)
    nums.inserir(60)
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
    nums = arvorePronta()

    nums.remover(40)
    assert nums.tamanho == 8

    nums.remover(60)
    nums.remover(80)
    assert nums.tamanho == 6

    nums.remover(30)
    nums.remover(20)
    nums.remover(100)
    assert nums.tamanho == 3

    nums.remover(90)
    nums.remover(0)
    nums.remover(10)
    assert nums.tamanho == 0


def teste_metodo_remover_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.remover(-50)


def teste_metodo_filhoEsquerdo():
    assert arvore.filhoEsquerdo(arvore.raiz) is 30
    assert arvore.filhoEsquerdo(90) is 80


def teste_metodo_filhoEsquerdo_geraUmErroSeOItemNaoPossuirUmFilhoAEsquerda():
    with raises(FalhaNaOperacao):
        arvore.filhoEsquerdo(40)


def teste_metodo_filhoEsquerdo_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhoEsquerdo(-40)


def teste_metodo_filhoDireito():
    assert arvore.filhoDireito(arvore.raiz) is 90
    assert arvore.filhoDireito(10) is 20


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

