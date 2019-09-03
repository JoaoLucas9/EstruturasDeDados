from lista import Lista

# TODO refatorar testes

lista = Lista()
lista + 1
lista + 2
lista + 3
lista + 4
lista + 5
lista + 6
lista + None
lista + 1
lista + 1
lista + 2
lista + 6
lista + 6
lista + 6


DUPLICADOS = lista.DUPLICADOS
OU = lista.OU


def testes_assegureQueOMetodo__contains__retorna():
    """Testes do operador in com objetos Lista"""
    trueSeOItemPassadoEstiverNaLista()
    falseSeOItemPassadoNaoEstiverNaLista()
    trueSePassado_None_eEleEstiverNaLista()

    trueSeTodosOsItensDeUm_list_set_tupla_estiveremNaLista()

    falseSeAoMenosUmDosItensDeUm_list_naoEstiverNaLista()
    falseSeInformada_DUPLICADOS_ENaoHouverNenhumItemDuplicado()


def trueSeOItemPassadoEstiverNaLista():
    assert 2 in lista
    assert 6 in lista


def falseSeOItemPassadoNaoEstiverNaLista():
    assert -1 not in lista


def trueSePassado_None_eEleEstiverNaLista():
    assert None in lista


def trueSeTodosOsItensDeUm_list_set_tupla_estiveremNaLista():
    assert [1, 2, 3] in lista
    assert {2, 3, 4} in lista
    assert (4, 5, None) in lista


def falseSeAoMenosUmDosItensDeUm_list_naoEstiverNaLista():
    assert [-1, 2, 4] not in lista


def falseSeInformada_DUPLICADOS_ENaoHouverNenhumItemDuplicado():
    novaLista = Lista()
    novaLista + 1
    novaLista + 2
    novaLista + 3

    assert DUPLICADOS not in novaLista


def testes_assegureQueOMetodo__contains__retornaTrueSe():
    """Testes do operador in com objetos Lista"""
    osItensDoIterableNaoEstiveremNaMesmaOrdemDosItensNaLista()
    oEspacamentoDosItensNoIterableDifiraDoEspacamentoDosItensNaLista()
    aRepeticaoDeUmItemNoIterableSupereAsRepeticoesDoItemNaLista()

    informado_DUPLICADOS_eHouverAoMenosUmItemDuplicado()


def osItensDoIterableNaoEstiveremNaMesmaOrdemDosItensNaLista():
    assert [3, 2, 1] in lista


def oEspacamentoDosItensNoIterableDifiraDoEspacamentoDosItensNaLista():
    assert [1, 3, None] in lista


def aRepeticaoDeUmItemNoIterableSupereAsRepeticoesDoItemNaLista():
    assert [2, 4, 4, 4, 5, 5] in lista


def informado_DUPLICADOS_eHouverAoMenosUmItemDuplicado():
    assert DUPLICADOS in lista


def testes_assegureQueOMetodo_contem_retorna():
    trueSeHouverNaListaUmaSequenciaDeItensIdenticaAoIteravel()
    trueSeOIteravelEstiverVazio()
    trueSeTodasAsCondicoesDoDicioforemSatisfeitas()
    trueSeODicioEstiverVazio()
    trueSeOIteravelEODicioEstiveremVazios()
    trueSeASequenciaDeItensDoIteravelForEncontradaETodasAsCondicoesDoDicioForemSatisfeitas()

    falseSeNaoHouverNaListaUmaSequenciaDeItensIdenticaAoIteravel()
    falseSePeloMenosUmaDasCondicoesDoDicioNaoForSatisfeita()

    trueComOOperadorOuSeASequenciaDoIteravelForEncontradaOuSeAsCondicoesForemSatisfeitas()

    falseComOOperadorOuSeASequenciaDoIteravelNaoForEncontradaEAsCondicoesNaoForemSatisfeitas()

    trueSeTodasAsCondicoesDoDicioForemSatisfeitas()

    falseSeAoMenosUmaDasCondicoesDoDicioNaoForSatisfeita()

    trueSeTodosOsItensDeUmIteravelSatisfizeremACondicao()

    falseSeAoMenosUmDosItensDeUmIteravelNaoSatisfizerACondicao()


def trueSeHouverNaListaUmaSequenciaDeItensIdenticaAoIteravel():

    assert lista.contem([2, 3, 4])

    assert lista.contem((1, 2, 3, 4))


def trueSeOIteravelEstiverVazio():
    assert lista.contem(())


def trueSeTodasAsCondicoesDoDicioforemSatisfeitas():
    assert lista.contem(dicio={3:1, 2:2, 1:None, 4:6})


def trueSeODicioEstiverVazio():
    assert lista.contem(dicio={})


def trueSeOIteravelEODicioEstiveremVazios():
    assert lista.contem([], dicio={})

# TODO alterar nome
def trueSeASequenciaDeItensDoIteravelForEncontradaETodasAsCondicoesDoDicioForemSatisfeitas():
    assert lista.contem([6, None, 1, 1], dicio={1:5, 2:2, 0:10})
    assert lista.contem([6, 6, 6], dicio={4:6, '1+':[1,4], 0:(11, 12)})


def falseSeNaoHouverNaListaUmaSequenciaDeItensIdenticaAoIteravel():
    assert not lista.contem((5, 6, 7))

    assert not lista.contem((5, 6, None, 8))

    assert not lista.contem([4, 6])

    assert not lista.contem([1, 2, 3, 3, 4])

    assert not lista.contem((3, 2, 1))


def falseSePeloMenosUmaDasCondicoesDoDicioNaoForSatisfeita():
    assert not lista.contem(dicio={0:1})
    assert not lista.contem(dicio={3:1, 1: 'Teste'})
    assert not lista.contem(dicio={-1:1})


# TODO alterar nome
def trueComOOperadorOuSeASequenciaDoIteravelForEncontradaOuSeAsCondicoesForemSatisfeitas():
    assert lista.contem([1, 2, 3, 4], OU, {0:1, 3:2})
    assert lista.contem([1, 2, 5], OU, {3:1, 2:2})
    assert lista.contem([1, -2], OU, {'5-':1, 1:{3, 5}})

# TODO alterar nome
def falseComOOperadorOuSeASequenciaDoIteravelNaoForEncontradaEAsCondicoesNaoForemSatisfeitas():
    assert not lista.contem((1, 2, 5), OU, {0:1, 3:2})
    assert not lista.contem((5, 4), OU, {0:[7, 1], 3:1})

# testes do método contem informando o dicio cujas chaves são strings
# contem deve retornar true se todas as condições forem satisfeitas
def trueSeTodasAsCondicoesDoDicioForemSatisfeitas():
    assert lista.contem(dicio={'3+':1, '0+':2, 1:4, '3-':5, '1-':None})


def falseSeAoMenosUmaDasCondicoesDoDicioNaoForSatisfeita():
    assert not lista.contem(dicio={'0+':2, '2-':1})


def trueSeTodosOsItensDeUmIteravelSatisfizeremACondicao():
    assert lista.contem(dicio={1:[4, 5], '0+':(None, 5), '10-':{6}})


def falseSeAoMenosUmDosItensDeUmIteravelNaoSatisfizerACondicao():
    # o 7 não está presente na lista
    assert not lista.contem(dicio={1:[4, 7], '0+':(4, 5), '10-':{6}})
