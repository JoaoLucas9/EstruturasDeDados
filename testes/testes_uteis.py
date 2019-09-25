from uteistestes import executar, iguais

def teste_funcao_executar_informarUmCallableQueNaoGeraNenhumErro():
    assert executar(lambda : max(4, 5)) == 5
    assert executar(lambda : 5) == 5


def teste_funcao_executar_informarUmCallableQueGeraNenhumErro():
    def gerarErro():
        raise Exception

    assert executar(gerarErro, -1) == -1
    assert executar(lambda : 1/0, 'erro') == 'erro'


def testes_funcao_iguais_doisObjetosNaoIteraveisIguais():
    assert iguais(50, 50)


def testes_funcao_iguais_doisObjetosNaoIteraveisDiferentes():
    assert not iguais('1', 1)


def testes_funcao_iguais_doisIteraveisIguais():
    assert iguais((1, 2, 3), [1, 2, 3])


def testes_funcao_iguais_doisIteraveisDiferentes():
    assert not iguais((1, 2, 3), [1, 2])
    assert not iguais((1, 2, None), [1, 2])
    assert not iguais((1, 2, 3), (3, 1, 2))




