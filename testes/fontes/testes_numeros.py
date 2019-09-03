from numeros import primeiroPrimoMaiorQue

def testes_primeiroPrimoMaiorQue():
    assert primeiroPrimoMaiorQue(1) == 2
    assert primeiroPrimoMaiorQue(2) == 3
    assert primeiroPrimoMaiorQue(20) == 23
    assert primeiroPrimoMaiorQue(292) == 293
    assert primeiroPrimoMaiorQue(293) == 307
    assert primeiroPrimoMaiorQue(300) == 307
    assert primeiroPrimoMaiorQue(307) == 311
    assert primeiroPrimoMaiorQue(598) == 599
    assert primeiroPrimoMaiorQue(599) == 601
    assert primeiroPrimoMaiorQue(600) == 601
    assert primeiroPrimoMaiorQue(601) == 607
    assert primeiroPrimoMaiorQue(993) == 997