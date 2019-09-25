from arvore import Heap, IGUAIS
from uteis import INDEFINIDO
from pytest import raises
from erros import ItemNaoEncontrado, FalhaNaOperacao
from pyext import naoGeraErro
from iteruteis import vazio
from uteistestes import maior, pickle, load, deletar


def novoHeap(*nums):
    heap = Heap(maior)

    for num in nums:
        heap.inserir(num)

    return heap


heap = novoHeap(0, 1, 2, 3, 4, 5, 6, 7, 8)


def testes_oMetodo_inserir_definiraARaizDaArvoreSeElaEstiverVazia():
    heap = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    heap.inserir(0)

    assert heap.topo == 0


def testes_metodo_inserir():
    heap = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))

    heap.inserir(0)
    heap.inserir(1)
    assegureQueEUmHeap(heap)

    heap.inserir(2)
    assegureQueEUmHeap(heap)

    heap.inserir(3)
    assegureQueEUmHeap(heap)

    heap.inserir(4)
    assegureQueEUmHeap(heap)

    heap.inserir(5)
    assegureQueEUmHeap(heap)

    heap.inserir(6)
    assegureQueEUmHeap(heap)

    heap.inserir(7)
    assegureQueEUmHeap(heap)


def assegureQueEUmHeap(heap):
    assegureQueAPropriedadeDeOrdemEstaSatisfeita(heap)
    assegureQueEUmaArvoreBinariaCompleta(heap)


def assegureQueAPropriedadeDeOrdemEstaSatisfeita(heap):
    """Propriedade de ordem: para cada item i, os filhos de i terão um
    prioridade menor igual a de i."""
    from arvore import _IteradorPosFixado

    for nodo in _IteradorPosFixado(heap._raiz):
        for filho in nodo.filhos:
            assert filho.prioridade <= nodo.prioridade


def assegureQueEUmaArvoreBinariaCompleta(heap):
    """Itera-se pelos nodos do penúltimo nível do heap até encontrar o
    primeiro que possui 0 ou 1 filho, após encontra-lo assegura-se que
    todos os nodos restantes a sua direita não possuem nenhum filho."""
    from arvore import _IteradorPorNivel

    penultimoNivel = heap.niveis -1
    iterador = _IteradorPorNivel(heap._raiz, penultimoNivel)

    for nodo in iterador:
        if len(nodo.filhos) is not 2:
            assert all(n.esquerdo is n.direito is None for n in iterador)


def teste_IteradorPosFixado():
    assert list(heap) == [0, 3, 6, 2, 7, 1, 4, 5, 8]


def teste_IteradorPosFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in Heap(None):
            pass


def teste_IteradorPreFixado():
    assert list(heap.preFixado()) == [8, 7, 6, 0, 3, 2, 5, 1, 4]


def teste_IteradorPreFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in Heap(None).preFixado():
            pass


def teste_IteradorInterFixado():
    assert list(heap.interFixado()) == [0, 6, 3, 7, 2, 8, 1, 5, 4]


def teste_IteradorInterFixado_iterarSobreUmaArvoreVazia():
    with naoGeraErro():
        for n in Heap(None).interFixado():
            pass


def testes_doOperador_in():
    assert 2 in heap
    assert 5 in heap
    assert heap.topo in heap


def testes_metodo_pai():
    assert heap.pai(0) is 6
    assert heap.pai(7) is 8
    assert heap.pai(heap.topo) is INDEFINIDO


def teste_oMetodo_pai_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        heap.pai(-10)


def testes_metodo_filhos():
    assert heap.filhos(7) == (6, 2)
    assert heap.filhos(1) == tuple()
    assert heap.filhos(heap.topo) == (7, 5)


def teste_oMetodo_filhos_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        heap.filhos(-5)


def teste_propriedade_niveis():
    assert heap.niveis == 4
    assert Heap(None).niveis == 0 #vazia


def teste_propriedade_ultimoNivel():
    assert heap.ultimoNivel is 3
    assert Heap(lambda x1, x2: x1).ultimoNivel is INDEFINIDO

    h = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    h.inserir(0)

    assert h.ultimoNivel is 0


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
    assert list(heap.ancestrais(4)) == [5, 8]
    assert list(heap.ancestrais(6)) == [7, 8]
    assert list(heap.ancestrais(8)) == []


def teste_oMetodo_ancestrais_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        heap.ancestrais(-5)


def testes_metodo_remover():
    nums = novoHeap(0, 1, 2, 3, 4, 5, 6, 7, 8)

    assert nums.remover() == 8
    assegureQueEUmHeap(nums)

    assert nums.remover() == 7
    assegureQueEUmHeap(nums)

    assert nums.remover() == 6
    assegureQueEUmHeap(nums)

    assert nums.remover() == 5
    assegureQueEUmHeap(nums)

    assert nums.remover() == 4
    assegureQueEUmHeap(nums)

    assert nums.remover() == 3
    assegureQueEUmHeap(nums)

    assert nums.remover() == 2
    assegureQueEUmHeap(nums)

    assert nums.remover() == 1
    assegureQueEUmHeap(nums)

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

    estudos = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    estudos.inserir(mat, 3)
    estudos.inserir(psico, 1)
    estudos.inserir(neuro, 2)
    estudos.inserir(fis, 2)
    estudos.inserir(comp, 4)
    estudos.inserir(geo, 0)
    estudos.inserir(prog, 3)

    assert estudos.remover() == comp
    assegureQueEUmHeap(estudos)

    assert estudos.remover() == mat
    assegureQueEUmHeap(estudos)

    assert estudos.remover() == prog
    assegureQueEUmHeap(estudos)

    assert estudos.remover() == fis
    assegureQueEUmHeap(estudos)

    assert estudos.remover() == neuro
    assegureQueEUmHeap(estudos)

    assert estudos.remover() == psico
    assegureQueEUmHeap(estudos)

    assert estudos.remover() == geo
    assert estudos.vazio


def testes_propriedade_tamanho_aposRemoverItens():
    nums = novoHeap(0, 1, 2, 3, 4, 5, 6, 7, 8)
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
    assert heap.quantidadeDeFilhos(7) is 2
    assert heap.quantidadeDeFilhos(1) is 0
    assert heap.quantidadeDeFilhos(heap.topo) is 2


def teste_oMetodo_quantidadeDeFilhos_geraUmErroSeOItemNaoForLocalizado():
    with raises(ItemNaoEncontrado):
        heap.quantidadeDeFilhos(-5)


def teste_oMetodo_quantidadeDeFilhos_iraGerarUmErroSeOHeapEstiverVazio():
    with raises(FalhaNaOperacao):
        Heap(None).remover()


def teste_oPropriedade_topt_iraGerarUmErroSeOHeapEstiverVazio():
    with raises(FalhaNaOperacao):
        Heap(None).topo


def testes_metodo_nivel():
    assert tuple(heap.nivel(2)) == (6, 2, 1, 4)
    assert tuple(heap.nivel(heap.ultimoNivel)) == (0, 3)


def testes_oMetodo_nivel_retornaUmIteradorVazioSeOHeapNaoPossuirONivelInformado():
    assert vazio(heap.nivel(10))
    assert vazio(heap.nivel(-10))


def testes_metodo_inserir_inserirItensComPrioridadesIguais():
    """Verificar se o heap funciona corretamente ao inserir itens com
    prioridades iguais"""
    heap = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    heap.inserir('tarefa1', 3)
    heap.inserir('tarefa2', 5)
    assegureQueEUmHeap(heap)

    heap.inserir('tarefa3', 1)
    heap.inserir('tarefa4', 2)
    assegureQueEUmHeap(heap)

    heap.inserir('tarefa5', 1)
    heap.inserir('tarefa6', 3)
    assegureQueEUmHeap(heap)

    heap.inserir('tarefa7', 1)
    heap.inserir('tarefa8', 5)
    assegureQueEUmHeap(heap)


def testes_metodo_inserir_inserirItensDuplicados():
    """Verificar se o heap funciona corretamente ao inserir itens duplicados,
    este teste é ligeiramente diferente do teste acima pois este não informa o
    segundo parâmetro para o método inserir."""
    heap = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    heap.inserir(3)
    heap.inserir(5)
    assegureQueEUmHeap(heap)

    heap.inserir(1)
    heap.inserir(2)
    assegureQueEUmHeap(heap)

    heap.inserir(1)
    heap.inserir(3)
    assegureQueEUmHeap(heap)

    heap.inserir(1)
    heap.inserir(5)
    assegureQueEUmHeap(heap)


def testes_metodo_remover_deUmHeapComItensDePrioridadesIguais():
    """Verifica se o heap funciona corretamente ao remover seus itens que
    possuem prioridades iguais"""
    heap = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    heap.inserir('tarefa1', 3)
    heap.inserir('tarefa2', 5)
    heap.inserir('tarefa3', 1)
    heap.inserir('tarefa4', 2)
    heap.inserir('tarefa5', 1)
    heap.inserir('tarefa6', 3)
    heap.inserir('tarefa7', 1)
    heap.inserir('tarefa8', 5)

    assert heap.remover() is 'tarefa2'
    assert heap.remover() is 'tarefa8'
    assegureQueEUmHeap(heap)

    assert heap.remover() is 'tarefa1'
    assert heap.remover() is 'tarefa6'
    assegureQueEUmHeap(heap)

    assert heap.remover() is 'tarefa4'
    assert heap.remover() is 'tarefa7'
    assegureQueEUmHeap(heap)

    assert heap.remover() is 'tarefa3'
    assert heap.remover() is 'tarefa5'
    assert heap.vazio


def testes_metodo_remover_deUmHeapComItensDuplicados():
    """remover itens de um heap que possui itens duplicados, este teste é
    ligeiramente diferente do teste acima pois os itens foram inseridos sem
    informar o segundo parâmetro, a prioridade do item"""
    heap = Heap(lambda x1, x2: IGUAIS if x1 == x2 else max(x1, x2))
    heap.inserir(5)
    heap.inserir(3)
    heap.inserir(5)
    heap.inserir(3)
    heap.inserir(4)
    heap.inserir(5)
    heap.inserir(5)
    heap.inserir(3)

    assert heap.remover() is 5
    assert heap.remover() is 5
    assegureQueEUmHeap(heap)

    assert heap.remover() is 5
    assert heap.remover() is 5
    assegureQueEUmHeap(heap)

    assert heap.remover() is 4
    assert heap.remover() is 3
    assegureQueEUmHeap(heap)

    assert heap.remover() is 3
    assert heap.remover() is 3
    assert heap.vazio


# dois heaps serão iguais se a prioridade de qualquer um dos itens no heap A
# for igual a prioridade do mesmo item no heap B, isto implica que todos os
# itens de um dos heaps devem estar presentes no outro também.
def testes_operadorDe_igualdade_retornaTrueSe():
    osHeapsPossuiremOsMesmosItensComAsMesmasPrioridades()
    osHeapsEstiveremVazios()


def osHeapsPossuiremOsMesmosItensComAsMesmasPrioridades():
    heap1 = novoHeap(0, 1, 2, 3, 4, 5, 6, 7, 8)
    heap2 = novoHeap(0, 3, 8, 4, 7, 2, 1, 5, 6)

    assert heap1 == heap2


def osHeapsEstiveremVazios():
    assert Heap(None) == Heap(None)


def testes_operadorDe_igualdade_retornaFalseSe():
    osHeapsPossuiremOsMesmosItensComPrioridadesDiferentes()
    osHeapsPossuiremItensDiferentes()
    apenasUmDosHeapsEstiverVazio()
    oObjetoInformadoNaoForUmHeap()
    asRaizesForemDiferentes()
    osHeapsPossuiremOsMesmosItensEmQuantidadesDiferentes()


def osHeapsPossuiremOsMesmosItensComPrioridadesDiferentes():
    heap1 = Heap(lambda p1, p2: IGUAIS if p1 == p2 else max(p1, p2))
    heap1.inserir('t1', 5)
    heap1.inserir('t2', 3)
    heap1.inserir('t3', 5)
    heap1.inserir('t4', 4)
    heap1.inserir('t5', 2)

    heap2 = Heap(lambda p1, p2: IGUAIS if p1 == p2 else max(p1, p2))
    heap2.inserir('t1', 5)
    heap2.inserir('t2', 3)
    heap2.inserir('t3', 5)
    heap2.inserir('t4', 3) # a prioridade da t4 é diferente
    heap2.inserir('t5', 2)

    assert heap1 != heap2


def osHeapsPossuiremItensDiferentes():
    heap1 = Heap(lambda p1, p2: IGUAIS if p1 == p2 else max(p1, p2))
    heap1.inserir('t1', 5)
    heap1.inserir('t2', 3)
    heap1.inserir('t3', 5)
    heap1.inserir('t4', 4)
    heap1.inserir('t5', 2)

    heap2 = Heap(lambda p1, p2: IGUAIS if p1 == p2 else max(p1, p2))
    heap2.inserir('t1', 5)
    heap2.inserir('t2', 3)
    heap2.inserir('t4', 4)
    heap2.inserir('t5', 2)

    assert heap1 != heap2


def apenasUmDosHeapsEstiverVazio():
    assert heap != Heap(None)
    assert Heap(None) != heap


def oObjetoInformadoNaoForUmHeap():
    # a estrutura da arvore binária é exatamente igual a estrutura do Heap
    from arvore import ArvoreBinaria
    arvore = ArvoreBinaria()
    arvore.inserir(8)
    arvore.inserir(7, 8)
    arvore.inserir(5, 8)
    arvore.inserir(6, 7)
    arvore.inserir(2, 7)
    arvore.inserir(1, 5)
    arvore.inserir(4, 5)
    arvore.inserir(0, 6)
    arvore.inserir(3, 6)

    assert heap != arvore
    assert heap != (1, 2)


def asRaizesForemDiferentes():
    assert novoHeap(0) != novoHeap(1)


def osHeapsPossuiremOsMesmosItensEmQuantidadesDiferentes():
    assert novoHeap(0, 1, 2) != novoHeap(0, 1, 2, 1)
    assert novoHeap(0, 1, 2, 2) != novoHeap(0, 1, 2, 1)
    assert novoHeap(0, 1, 2, 2) != novoHeap(0, 1, 2)
    assert novoHeap(0, 1, 2) != novoHeap(0, 1, 2, 2)


def testesDasFuncoes_dumpEloads_comUmHeap():
    """Assegurar que as funções pickle.dumps e pickle.loads funcionam como o
    esperado com um Heap. Funcionar como o esperado significa que é
    possível registrar um Heap em um arquivo utilizando a função
    pickle.dumps e futuramente recuperá-lo utilizando a função pickle.loads.
    """
    pickle(heap, 'heap')
    h = load('heap')

    assegurarQueOsHeapsPossuemAMesmaEstrutura(h, heap)
    assert h.tamanho == heap.tamanho

    deletar('heap')


def assegurarQueOsHeapsPossuemAMesmaEstrutura(h1, h2):
    from arvore import _IteradorPreFixado as Iterador

    for n1, n2 in zip(Iterador(h1._raiz), Iterador(h2._raiz)):
        assert n1 == n2
        assert n1.prioridade == n2.prioridade


def testesDasFuncoes_dumpEloads_comUmHeapVazio():
    pickle(Heap(None), 'heapVazio')
    h = load('heapVazio')

    assert h.vazio
    assert h.tamanho is 0

    deletar('heapVazio')


def teste_metodo_eq_comparaAsPrioridadesUtilizandoOComparador():
    """o teste visa garantir que o método __eq__ compara as prioridades dos
    itens utilizando o comparador do Heap ao invés do operador ==.

    lógica do teste: dois números, x e y estão no mesmo nível de prioridade,
    portanto itens com a prioridade x ou y possuem prioridades iguais mesmo
    que x != y, se as prioridades dos itens forem comparadas uitlizando ==
    dois Heaps com os mesmos itens e com as mesmas prioridades serão
    considerados diferentes quando deveriam ser considerados iguais."""
    branca = [0, 1] # prioridade branca
    h1 = Heap(lambda x1, x2: IGUAIS if x1 in branca and x2 in branca else x2)
    h1.inserir('tarefa1', 0)

    h2 = Heap(lambda x1, x2: IGUAIS if x1 in branca and x2 in branca else x2)
    h2.inserir('tarefa1', 1)

    assert h1 == h2, 'As prioridades devem estar sendo comparadas com =='


