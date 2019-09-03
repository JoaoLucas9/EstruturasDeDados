from uteis import executar

def teste_funcao_executar_informarUmCallableQueNaoGeraNenhumErro():
    assert executar(lambda : max(4, 5)) == 5
    assert executar(lambda : 5) == 5


def teste_funcao_executar_informarUmCallableQueGeraNenhumErro():
    def gerarErro():
        raise Exception

    assert executar(gerarErro, -1) == -1
    assert executar(lambda : 1/0, 'erro') == 'erro'