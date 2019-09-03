from arvore import Heap, INDEFINIDO, IGUAIS
from pytest import raises
from erros import ItemNaoEncontrado, FalhaNaOperacao
from pyext import naoGeraErro


def arvorePronta():
    nums = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    nums.inserir(0)
    nums.inserir(1)
    nums.inserir(2)
    nums.inserir(3)
    nums.inserir(4)
    nums.inserir(5)
    nums.inserir(6)
    nums.inserir(7)
    nums.inserir(8)

    return nums


def arvoreVazia():
    return Heap(None)


arvore = arvorePronta()


def testes_oMetodo_inserir_definiraARaizDaArvoreSeElaEstiverVazia():
    heap = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    heap.inserir(0)

    assert heap.topo == 0


def testes_metodo_inserir():
    heap = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))

    heap.inserir(0)
    heap.inserir(1)

    assert heap.pai(0) is 1
    assert heap.filhos(0) == tuple()
    assert heap.filhos(1) == (0,)

    heap.inserir(2)

    assert heap.pai(0) is heap.pai(1) is 2
    assert heap.filhos(0) == heap.filhos(1) == tuple()
    assert heap.filhos(2) == (0, 1)

    heap.inserir(3)

    assert heap.filhos(3) == (2, 1)
    assert heap.filhos(2) == (0, )
    assert heap.filhos(0) == heap.filhos(1) == tuple()
    assert heap.pai(2) is heap.pai(1) is 3
    assert heap.pai(0) is 2

    heap.inserir(4)

    assert heap.filhos(4) == (3, 1)
    assert heap.filhos(3) == (0, 2)
    assert heap.filhos(0) == heap.filhos(2) == heap.filhos(1) == tuple()
    assert heap.pai(3) is heap.pai(1) is 4
    assert heap.pai(0) is heap.pai(2) is 3

    heap.inserir(5)

    assert heap.filhos(5) == (3, 4)
    assert heap.filhos(3) == (0, 2)
    assert heap.filhos(4) == (1,)
    assert heap.filhos(0) == heap.filhos(2) == heap.filhos(1) == tuple()
    assert heap.pai(3) is heap.pai(4) is 5
    assert heap.pai(0) is heap.pai(2) is 3
    assert heap.pai(1) is 4

    heap.inserir(6)

    assert heap.filhos(6) == (3, 5)
    assert heap.filhos(3) == (0, 2)
    assert heap.filhos(5) == (1, 4)
    assert heap.filhos(0) == heap.filhos(2) == heap.filhos(1) == \
           heap.filhos(4) == tuple()
    assert heap.pai(3) is heap.pai(5) is 6
    assert heap.pai(0) is heap.pai(2)is 3
    assert heap.pai(1) is heap.pai(4) is 5

    heap.inserir(7)

    assert heap.filhos(7) == (6, 5)
    assert heap.filhos(6) == (3, 2)
    assert heap.filhos(5) == (1, 4)
    assert heap.filhos(3) == (0,)
    assert heap.filhos(0) == heap.filhos(2) == heap.filhos(1) == \
           heap.filhos(4) == tuple()
    assert heap.pai(6) is heap.pai(5) is 7
    assert heap.pai(3) is heap.pai(2) is 6
    assert heap.pai(1) is heap.pai(4) is 5
    assert heap.pai(0) is 3


def teste_IteradorPosFixado():
    assert list(arvore) == [0, 3, 6, 2, 7, 1, 4, 5, 8]


def teste_IteradorPosFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in Heap(None):
            pass


def teste_IteradorPreFixado():
    assert list(arvore.preFixado()) == [8, 7, 6, 0, 3, 2, 5, 1, 4]


def teste_IteradorPreFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in Heap(None).preFixado():
            pass


def teste_IteradorInterFixado():
    assert list(arvore.interFixado()) == [0, 6, 3, 7, 2, 8, 1, 5, 4]


def teste_IteradorInterFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in Heap(None).interFixado():
            pass


def testes_doOperador_in():
    assert 2 in arvore
    assert 5 in arvore
    assert arvore.topo in arvore


def testes_metodo_pai():
    assert arvore.pai(0) is 6
    assert arvore.pai(7) is 8
    assert arvore.pai(arvore.topo) is INDEFINIDO


def teste_oMetodo_pai_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.pai(-10)


def testes_metodo_filhos():
    assert arvore.filhos(7) == (6, 2)
    assert arvore.filhos(1) == tuple()
    assert arvore.filhos(arvore.topo) == (7, 5)


def teste_oMetodo_filhos_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.filhos(-5)


def teste_propriedade_niveis():
    assert arvore.niveis == 4
    assert Heap(None).niveis == 0 #vazia


def teste_propriedade_ultimoNivel():
    assert arvore.ultimoNivel is 3
    assert arvoreVazia().ultimoNivel is INDEFINIDO


def testes_propriedade_tamanho_aposInserirItens():
    nums = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))

    assert nums.tamanho == 0

    nums.inserir(0)
    assert nums.tamanho == 1

    nums.inserir(1)
    nums.inserir(2)
    assert nums.tamanho == 3

    nums.inserir(3)
    nums.inserir(4)
    nums.inserir(5)
    assert nums.tamanho == 6

    nums.inserir(6)
    nums.inserir(7)
    assert nums.tamanho == 8


def testes_metodo_inserir_informandoOParametroPrioridade():
    mat = 'matemática'
    psico = 'psicologia'
    neuro = 'neurociência'
    fis = 'física'
    comp = 'computação'
    geo = 'geografia'
    prog = 'programação'

    estudos = Heap(lambda x1, x2: IGUAIS if x1 == x2 else min(x1, x2))

    estudos.inserir(mat, 1)
    estudos.inserir(psico, 3)
    estudos.inserir(neuro, 2)

    assert estudos.filhos(mat) == (psico, neuro)
    assert estudos.filhos(psico) == estudos.filhos(neuro) == tuple()
    assert estudos.pai(psico) is estudos.pai(neuro) is mat

    estudos.inserir(fis, 2)

    assert estudos.filhos(mat) == (fis, neuro)
    assert estudos.filhos(fis) == (psico, )
    assert estudos.filhos(psico) == estudos.filhos(neuro) == tuple()
    assert estudos.pai(fis) is estudos.pai(neuro) is mat
    assert estudos.pai(psico) is fis

    estudos.inserir(comp, 0)

    assert estudos.topo is comp
    assert estudos.filhos(comp) == (mat, neuro)
    assert estudos.filhos(mat) == (psico, fis)
    assert estudos.filhos(psico) == estudos.filhos(fis) == \
           estudos.filhos(neuro) == tuple()
    assert estudos.pai(mat) is estudos.pai(neuro) is comp
    assert estudos.pai(psico) is estudos.pai(fis) is mat

    estudos.inserir(geo, 4)

    assert estudos.filhos(comp) == (mat, neuro)
    assert estudos.filhos(mat) == (psico, fis)
    assert estudos.filhos(psico) == estudos.filhos(fis) == tuple()
    assert estudos.filhos(neuro) == (geo, )
    assert estudos.pai(mat) is estudos.pai(neuro) is comp
    assert estudos.pai(psico) is estudos.pai(fis) is mat
    assert estudos.pai(geo) is neuro

    estudos.inserir(prog, 1) # originalmente a prioridade era 0, mas será
    # alterad p/ 1 momentaneamente

    assert estudos.topo is comp
    assert estudos.filhos(comp) == (mat, prog)
    assert estudos.filhos(mat) == (psico, fis)
    assert estudos.filhos(prog) == (geo, neuro)
    assert estudos.filhos(psico) == estudos.filhos(fis) == \
           estudos.filhos(geo) == estudos.filhos(neuro) == tuple()
    assert estudos.pai(mat) is estudos.pai(prog) is comp
    assert estudos.pai(psico) is estudos.pai(fis) is mat
    assert estudos.pai(geo) is estudos.pai(neuro) is prog


def testes_metodo_ancestrais():
    assert list(arvore.ancestrais(4)) == [5, 8]
    assert list(arvore.ancestrais(6)) == [7, 8]
    assert list(arvore.ancestrais(8)) == []


def teste_oMetodo_ancestrais_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.ancestrais(-5)


def testes_metodo_remover():
    nums = arvorePronta()

    assert nums.remover() == 8
    assert nums.topo is 7
    assert nums.filhos(7) == (6, 5)
    assert nums.filhos(6) == (3, 2)
    assert nums.filhos(5) == (1, 4)
    assert nums.filhos(3) == (0, )
    assert nums.filhos(0) == nums.filhos(2) == nums.filhos(1) == \
           nums.filhos(4) == tuple()
    assert nums.pai(6) is nums.pai(5) is 7
    assert nums.pai(3) is nums.pai(2) is 6
    assert nums.pai(1) is nums.pai(4) is 5
    assert nums.pai(0) is 3

    assert nums.remover() == 7
    assert nums.topo is 6
    assert nums.filhos(6) == (3, 5)
    assert nums.filhos(3) == (0, 2)
    assert nums.filhos(5) == (1, 4)
    assert nums.filhos(0) == nums.filhos(2) == nums.filhos(1) == \
           nums.filhos(4) == tuple()
    assert nums.pai(3) == nums.pai(5) is 6
    assert nums.pai(0) == nums.pai(2) is 3
    assert nums.pai(1) == nums.pai(4) is 5

    assert nums.remover() == 6
    assert nums.topo is 5
    assert nums.filhos(5) == (3, 4)
    assert nums.filhos(3) == (0, 2)
    assert nums.filhos(4) == (1, )
    assert nums.filhos(0) == nums.filhos(2) == nums.filhos(1) == tuple()
    assert nums.pai(3) == nums.pai(4) is 5
    assert nums.pai(0) == nums.pai(2) is 3
    assert nums.pai(1) is 4

    assert nums.remover() == 5
    assert nums.topo is 4
    assert nums.filhos(4) == (3, 1)
    assert nums.filhos(3) == (0, 2)
    assert nums.filhos(0) == nums.filhos(2) == nums.filhos(1) == tuple()
    assert nums.pai(3) == nums.pai(1) is 4
    assert nums.pai(0) == nums.pai(2) is 3

    assert nums.remover() == 4
    assert nums.topo is 3
    assert nums.filhos(3) == (2, 1)
    assert nums.filhos(2) == (0, )
    assert nums.filhos(0) == nums.filhos(1) == tuple()
    assert nums.pai(2) == nums.pai(1) is 3
    assert nums.pai(0) is 2

    assert nums.remover() == 3
    assert nums.topo is 2
    assert nums.filhos(2) == (0, 1)
    assert nums.filhos(0) == nums.filhos(1) == tuple()
    assert nums.pai(0) == nums.pai(1) is 2

    assert nums.remover() == 2
    assert nums.topo is 1
    assert nums.filhos(1) == (0, )
    assert nums.filhos(0) == tuple()
    assert nums.pai(0) is 1

    assert nums.remover() == 1
    assert nums.topo is 0
    assert nums.filhos(0) == tuple()

    assert nums.remover() == 0
    assert nums.vazio


# a árvore neste caso foi criada informando o parâmtero prioridades
def testes_metodo_remover_comPrioridades():
    mat = 'matemática'
    psico = 'psicologia'
    neuro = 'neurociência'
    fis = 'física'
    comp = 'computação'
    geo = 'geografia'
    prog = 'programação'

    estudos = Heap(lambda x1, x2: IGUAIS if x1 == x2 else min(x1, x2))
    estudos.inserir(mat, 1)
    estudos.inserir(psico, 3)
    estudos.inserir(neuro, 2)
    estudos.inserir(fis, 2)
    estudos.inserir(comp, 0)
    estudos.inserir(geo, 4)
    estudos.inserir(prog, 1)

    assert estudos.remover() == comp
    assert estudos.topo is mat
    assert estudos.filhos(mat) == (neuro, prog)
    assert estudos.filhos(neuro) == (psico, fis)
    assert estudos.filhos(prog) == (geo, )
    assert estudos.filhos(psico) == estudos.filhos(fis) == \
           estudos.filhos(geo) == tuple()
    assert estudos.pai(neuro) == estudos.pai(prog) is mat
    assert estudos.pai(psico) == estudos.pai(fis) is neuro
    assert estudos.pai(geo) is prog

    assert estudos.remover() == mat
    assert estudos.topo is prog
    assert estudos.filhos(prog) == (neuro, geo)
    assert estudos.filhos(neuro) == (psico, fis)
    assert estudos.filhos(psico) == estudos.filhos(fis) == \
           estudos.filhos(geo) == tuple()
    assert estudos.pai(neuro) == estudos.pai(geo) is prog
    assert estudos.pai(psico) == estudos.pai(fis) is neuro

    assert estudos.remover() == prog
    assert estudos.topo is fis
    assert estudos.filhos(fis) == (neuro, geo)
    assert estudos.filhos(neuro) == (psico, )
    assert estudos.filhos(psico) == estudos.filhos(geo) == tuple()
    assert estudos.pai(neuro) == estudos.pai(geo) is fis
    assert estudos.pai(psico) is neuro

    assert estudos.remover() == fis
    assert estudos.topo is neuro
    assert estudos.filhos(neuro) == (psico, geo)
    assert estudos.filhos(psico) == estudos.filhos(geo) == tuple()
    assert estudos.pai(psico) == estudos.pai(geo) is neuro

    assert estudos.remover() == neuro
    assert estudos.topo is psico
    assert estudos.filhos(psico) == (geo, )
    assert estudos.filhos(geo) == tuple()
    assert estudos.pai(geo) is psico

    assert estudos.remover() == psico
    assert estudos.topo is geo
    assert estudos.filhos(geo) == tuple()

    assert estudos.remover() == geo
    assert estudos.vazio


def testes_propriedade_tamanho_aposRemoverItens():
    nums = arvorePronta()
    nums.remover()
    nums.remover()
    nums.remover()

    assert nums.tamanho is 6

    nums.remover()
    nums.remover()

    assert nums.tamanho is 4

    nums.remover()
    nums.remover()
    nums.remover()
    nums.remover()

    assert nums.tamanho is 0


def testes_metodo_quantidadeDeFilhos():
    assert arvore.quantidadeDeFilhos(7) is 2
    assert arvore.quantidadeDeFilhos(1) is 0
    assert arvore.quantidadeDeFilhos(arvore.topo) is 2


def teste_oMetodo_quantidadeDeFilhos_iraGerarUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        arvore.quantidadeDeFilhos(-5)


def teste_oMetodo_quantidadeDeFilhos_iraGerarUmErroSeOHeapEstiverVazio():
    with raises(FalhaNaOperacao):
        Heap(None).remover()


def teste_oPropriedade_topt_iraGerarUmErroSeOHeapEstiverVazio():
    with raises(FalhaNaOperacao):
        Heap(None).topo


