def _apenasUmDelesEOrdenado(obj1, obj2):
    """Determina se apenas uma das coleções é ordenada.

       List e tuple são consideradas ordenadas, set não.
       Parâmetros:
          obj1 : [list | tuple | set] -> uma coleção
          obj2 : [list | tuple | set] -> uma coleção

       Retorno: true se apenas uma das coleções for ordenada, false caso
       contrário.
    """

    return ((isinstance(obj1, set) and not isinstance(obj1, set)) or
            (isinstance(obj2, set) and not isinstance(obj1, set)))


def _naoSaoOrdenadas(obj1, obj2):
    """Determina se ambas as coleções não são ordenadas.
       Parâmetros:

       Retorno: true se ambas as coleções não forem ordenadas,
       false caso contrário..

    """
    return isinstance(obj1, set) and isinstance(obj2, set)


def _asColecoesNaoOrdenadasSaoIguais(obj1, obj2):
    # considera que a coleção 2 implementa o met __contains__
    for item in obj1:
        if item not in obj2:
            return False

    return True


def _asColecoesOrdenadasSaoIguais(obj1, obj2):
    # considera q ambas as coleções implementam o método __iter__
    for item1, item2 in zip(obj1, obj2):
        if item1 != item2:
            return False

    return True


def iguais(obj1, obj2, ordenadas=None):
    if _apenasUmDelesEOrdenado(obj1,  obj2) or len(obj1) != len(obj2):
        return False

    if _naoSaoOrdenadas(obj1, obj2):
        return _asColecoesNaoOrdenadasSaoIguais(obj1, obj2)
    return _asColecoesOrdenadasSaoIguais(obj1, obj2)


# como descobrir se um obj é uma coleção ?
# como descobrir se a coleção é ordenada ?
