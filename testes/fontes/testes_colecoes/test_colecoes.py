from colecoes.colecoes import iguais
from colecoes.colecoes import ocorrencias
from colecoes.colecoes import contemDuplicados


class Colecao:

    def __init__(self, *args):
        self.lista = [x for x in args]

    def __iter__(self):
        return self.lista.__iter__()

    def __contains__(self, item):
        return item in self.lista

    def __len__(self):
        return self.lista.__len__()


def testes_assegureQueOMetodo_iguais_retorna():
    trueSePassar_list_e_tuple_comOsMesmosItensNaMesmaOrdem()
    trueSePassar_list_e_list_comOsMesmosItensNaMesmaOrdem()
    trueSePassar_set_e_set_comOsMesmosItens()
    trueSePassar_tuple_e_tuple_comOsMesmosItensNaMesmaOrdem()

    falseSePassar_set_e_set_comOItensDiferentes()
    falseSePassarUmaColecao_ordenada_eOutra_naoOrdenada_contendoOsMesmosItens()
    falseSePassarColecoesOrdenadasComItensDiferentes()
    falseSePassarColecoesOrdenadasComOsMesmosItensEmOrdensDiferentes()

    trueSePassar_Colecao_Colecao_e_true_comOsMesmosItensNaMesmaOrdem()
    trueSePassar_Colecao_Colecao_e_false_comOsMesmosItensEmOrdensDiferentes()
    trueSePassarDuasColecoesVaziasUmaOrdenadaEAOutraNao()

    falseSePassar_Colecao_tupla_e_true_comOsMesmosItensEmOrdensDiferentes()
    falseSePassar_list_Colecao_true_comItensDiferentes()
    falseSePassar_Colecao_Colecao_e_false_comItensRepetidosEmUmaENaoNaOutra()
    falseSePassar_Colecao_Colecao_e_false_comItensDiferentes()

    trueSePassar_int_int_iguais()
    trueSePassar_None_None_iguais()

    falseSePassar_int_int_diferentes()
    falseSePassarUmaColecaoEUmOutroObjetoQueNaoEUmaColecao()

def trueSePassar_list_e_tuple_comOsMesmosItensNaMesmaOrdem():
    assert iguais([1, 2, 3], (1, 2, 3))


def trueSePassar_list_e_list_comOsMesmosItensNaMesmaOrdem():
    assert iguais([1, 2, 3], [1, 2, 3])

# conceito de ordem não se aplica a sets
def trueSePassar_set_e_set_comOsMesmosItens():
    assert iguais({3, -5.21, 2, 1, 'str'}, {-5.21, 1, 'str', 2, 3})


def trueSePassar_tuple_e_tuple_comOsMesmosItensNaMesmaOrdem():
    assert iguais((1, 2, 3), (1, 2, 3))


def trueSePassarDoisIteraveisVazios():
    assert iguais((), [])

    # assert iguais((), {})


def falseSePassar_set_e_set_comOItensDiferentes():
    assert not iguais({1, 2, 3, 4}, {1, 2, 3})


def falseSePassarUmaColecao_ordenada_eOutra_naoOrdenada_contendoOsMesmosItens():
    assert not iguais((1, 2, 3), {1, 2, 3})


def falseSePassarColecoesOrdenadasComItensDiferentes():
    assert not iguais([1, 2, 3, 4], [1, 2, 3])


def falseSePassarColecoesOrdenadasComOsMesmosItensEmOrdensDiferentes():
    assert not iguais([1, 3, 2], [1, 2, 3])


def trueSePassar_Colecao_Colecao_e_true_comOsMesmosItensNaMesmaOrdem():
    assert iguais(Colecao(1, 2, 3), Colecao(1, 2, 3), True)


def trueSePassar_Colecao_Colecao_e_false_comOsMesmosItensEmOrdensDiferentes():
    assert iguais(Colecao(1, 2, 3), Colecao(3, 2, 1), False)


def trueSePassarDuasColecoesVaziasUmaOrdenadaEAOutraNao():
    assert iguais([], set())

    assert iguais(set(), Colecao(), True)


def falseSePassar_Colecao_tupla_e_true_comOsMesmosItensEmOrdensDiferentes():
    assert not iguais(Colecao(1, 2, 3), (3, 2, 1), True)


def falseSePassar_list_Colecao_true_comItensDiferentes():
    assert not iguais([1, 2, 3], Colecao(1, 2, 3, 4), True)


def falseSePassar_Colecao_Colecao_e_false_comItensRepetidosEmUmaENaoNaOutra():
    assert not iguais(Colecao(1, 1, 1, 2, 3), Colecao(1, 2, 3), False)
    assert not iguais(Colecao(1, 1, 1, 2, 3), Colecao(1, 2, 3, 3, 3), False)


def falseSePassar_Colecao_Colecao_e_false_comItensDiferentes():
    assert not iguais(Colecao(4, 1, 1, 2, 3), Colecao(1, 2, 3, 3, 3), False)


def trueSePassar_int_int_iguais():
    assert iguais(5, 5)


def trueSePassar_None_None_iguais():
    assert iguais(None, None)


def falseSePassar_int_int_diferentes():
    assert not iguais(5, 6)


def falseSePassarUmaColecaoEUmOutroObjetoQueNaoEUmaColecao():
    assert not iguais([1], 1)
    assert not iguais(1, [1])


def testes_assegureQueAFuncao_ocorrencias_retorna():
    umIteravelContendoTodosOsIndicesOndeOObjetoFoiEncontrado()
    umIteravelVazioSeOIteravelInformadoEstiverVazio()
    umIteravelVazioSeOObjetoNaoForEncontrado()


def umIteravelContendoTodosOsIndicesOndeOObjetoFoiEncontrado():
    assert iguais((0, 4), ocorrencias(2, [2, 1, 1, 3, 2]))

    assert iguais((1, 2), ocorrencias(1, [2, 1, 1, 3, 2]))


def umIteravelVazioSeOIteravelInformadoEstiverVazio():
    assert iguais([], ocorrencias(2, ()))


def umIteravelVazioSeOObjetoNaoForEncontrado():
    assert iguais([], ocorrencias(5, [2, 1, 1, 3, 2]))


def testes_assegureQueAFuncao_contemDuplicados_retorna():
    trueSeOIteravelPossuirPeloMenosUmObjetoDuplicado()

    falseSeOIteravelNaoPossuirNenhumObjetoDuplicado()
    falseSeOIteravelEstiverVazio()


def trueSeOIteravelPossuirPeloMenosUmObjetoDuplicado():
    assert contemDuplicados((1, 2, 3, 4, 5, 1))



def falseSeOIteravelNaoPossuirNenhumObjetoDuplicado():
    assert not contemDuplicados({1, 2, 3, 4, 5})


def falseSeOIteravelEstiverVazio():
    assert not contemDuplicados([])