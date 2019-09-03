from collections.abc import Collection
from collections.abc import Iterable

# TODO uma col ordenada e uma ñ ordenada vazias iguais ? 1 boa idéia ?
def iguais(obj1, obj2, ordenadas:bool=None) -> bool:
    """Determina se dois objetos são iguais.

       Cenários:
       1) os dois objetos são duas coleções:

         1.1) as duas coleções são ordenadas: para serem consideradas
         iguais ambas devem possuir os mesmos itens na mesma ordem, ou seja o
         nº item da coleção 1 deve ser igual ao nº item da coleção 2, para
         todos os itens contidos nas coleções 1 e 2. Observação: considera-se
         que o iterador das coleções retornam os itens na ordem na qual eles
         se encontram nas coleções.

         1.2) as duas coleções não são ordenadas: para serem consideradas
         iguais ambas devem possuir os mesmos itens

         1.3) uma é ordenada e a outra não:
            1.3.1) ambas estão vazias: serão consideradas iguais

            1.3.2) ao menos uma delas não está vazia: serão consideradas
            diferentes


       As comparações entre os objetos das coleções serão realizadas com o
       operador '=='.

       2) nenhum dos dois objetos é uma coleção: retorna o resultado do
       operador '==' comparando os objetos.

       3) um dos objetos é uma coleção e o outro não: retorna o resultado do
       operador '==' comparando os objetos.

       Parâmetros:
          obj1, obj2 : [? | Collection] -> os dois objetos que serão
          comparados.

          ordenadas -> esta variável deve ser informada se ao menos uma
          das coleções não for do tipo list, tuple ou set, ela irá
          categorizar a(s) coleção(ões) como ordenadas ou não.
          Os tipos list e tuple, são considerados ordenados, independendemente
          do boleano informado, enquanto que sets são considerados não
          ordenados. Se ambas as coleções forem list e/ou tuple e/ou set
          esta variável não precisa ser informada


       Retorno: true se os objetos forem considerados iguais, false caso
       contrário.

    """
    if isinstance(obj1, Collection) and isinstance(obj2, Collection):
        return _asColecoesSaoIguais(obj1, obj2, ordenadas)
    return obj1 == obj2


def _asColecoesSaoIguais(c1: Collection, c2: Collection, ordenadas: bool):
    # as duas coleções não são ordenadas ?
    if not _eOrdenada(c1, ordenadas) and not _eOrdenada(c2, ordenadas):
        return _colecoesNaoOrdenadasIguais(c1, c2)

    # as duas coleções são ordenadas ?
    if _eOrdenada(c1, ordenadas) and _eOrdenada(c2, ordenadas):
        return _colecoesOrdenadasIguais(c1, c2)

    return estaVazia(c1) and estaVazia(c2)


def _eOrdenada(colecao: Collection, ordenada: bool) -> bool:
    if not isinstance(colecao, (list, tuple, set)):
        return ordenada
    return isinstance(colecao, (list, tuple))


def _colecoesNaoOrdenadasIguais(obj1: Collection, obj2: Collection) -> bool:
    if len(obj1) != len(obj2):
        return False
    return _contarItens(obj1) == _contarItens(obj2)


def _contarItens(iteravel: Iterable) -> dict:
    """Computa quantas vezes um item é encontrado no iterável.

       Parâmetros:
          iteravel

       Retorno: um dict cujas chaves são os itens do iteravel e os valores
       representam quantas vezes o item foi encontrado.

       Cuidado, se os itens do iteravel forem mutáveis e se um ou mais for
       alterado enquanto a função calcula as ocorrências ou até mesmo após
       elas já terem sido calculadas, o resultado retornado pode tornar-se
       incorreto e/ou inesperado, estranho.

    """
    ocorrencias = dict()

    for item in iteravel:
        ocorrencias[item] = ocorrencias.get(item, 0) + 1

    return ocorrencias


def estaVazia(colecao: Collection):
    return len(colecao) == 0


def _colecoesOrdenadasIguais(obj1: Collection, obj2: Collection) -> bool:
    if len(obj1) != len(obj2):
        return False

    for item1, item2 in zip(obj1, obj2):
        if item1 != item2:
            return False

    return True


def ocorrencias(obj, iteravel:Iterable) -> Iterable:
    """
       Parâmetros:
          obj -> o objeto que será procurado no iterável

          iteravel -> os objetos que serão percorridos à procura do obj.

       Retorno: um iterável com todos os índices onde o obj foi encontrado.
       Considera-se que o 1º objeto do iterável está no índice 0, o 2º no
       índice 1 e assim por diante, semelhante a uma list.

    """
    indices = []

    for indice, item in enumerate(iteravel):
        if obj == item:
            indices.append(indice)

    return indices


def contemDuplicados(iteravel: Iterable):
    """
       Parâmetros:
          iteravel

       Retorna: true se for encontrado um objeto que se repete uma ou mais
       vezes no iterável, falso caso não seja encontrado nenhum.

    """
    encontrados = []

    for obj in iteravel:
        if obj in encontrados:
            return True

        encontrados.append(obj)

    return False
